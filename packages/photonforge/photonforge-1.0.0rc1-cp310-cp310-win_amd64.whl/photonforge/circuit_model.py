from .extension import Component, Port, Model, SMatrix, register_model_class, _connect_s_matrices
from .tidy3d_model import (
    _Tidy3DModeSolverRunner,
    _align_and_overlap,
    _align_and_overlap_analytical,
)
from .cache import _Cache

import numpy
import tidy3d

import re
import struct
from typing import Any, Optional
from collections.abc import Sequence


CACHE_SIZE = 20


def _gather_status(*runners):
    """Create an overall status based on a collection of Tidy3D runners."""
    num_tasks = 0
    progress = 0
    message = "success"
    tasks = []
    for task in runners:
        task_status = task.status
        inner_tasks = task_status.get("tasks", None)
        if inner_tasks is not None:
            tasks.extend(inner_tasks)
            task_weight = max(1, len(inner_tasks))
        else:
            task_weight = 1
        num_tasks += task_weight
        if message != "error":
            if task_status["message"] == "error":
                message = "error"
            elif task_status["message"] == "running":
                message = "running"
                progress += task_weight * task_status["progress"]
            elif task_status["message"] == "success":
                progress += task_weight * 100
    if message == "running":
        progress /= num_tasks
    else:
        progress = 100
    return {"progress": progress, "message": message, "tasks": tasks}


class _CircuitModelRunner:
    # Cache for port coefficients
    cache = _Cache(CACHE_SIZE)

    def __init__(self, netlist, runners, frequencies, component_name, ports):
        self.netlist = netlist
        self.runners = runners
        self.frequencies = frequencies
        self.component_name = component_name
        self.ports = ports
        self._s_matrix = None

    @property
    def status(self):
        return _gather_status(*self.runners.values())

    @property
    def s_matrix(self):
        if self._s_matrix is None:
            s_dict = {}
            for index, (reference, phase_correction) in enumerate(
                zip(self.netlist["instances"], self.netlist["phase corrections"])
            ):
                # Check if reference is needed
                if reference.component.active_model is None:
                    continue

                s_matrix = self.runners[index].s_matrix
                if s_matrix is None:
                    return None

                # Fix port phases if a rotation is applied
                mode_factor = {
                    f"{port_name}@{mode}": 1.0
                    for port_name, port in reference.component.ports.items()
                    for mode in range(port.num_modes)
                }

                if phase_correction:
                    for port_name, port in reference.component.ports.items():
                        if isinstance(port, Port):
                            key = (
                                reference.component.technology.as_bytes,
                                port.spec.as_bytes,
                                port.input_direction % 360,
                                port.inverted,
                                reference.rotation % 360,
                            )
                            overlap = _CircuitModelRunner.cache[key]
                            if overlap is None:
                                overlap = _align_and_overlap(
                                    self.runners[(index, port_name, 0)].data,
                                    self.runners[(index, port_name, 1)].data,
                                )[0]
                                _CircuitModelRunner.cache[key] = overlap
                        else:
                            overlap = numpy.array(
                                [_align_and_overlap_analytical(port, reference[port_name])]
                            )

                        for mode in range(port.num_modes):
                            mode_factor[f"{port_name}@{mode}"] = overlap[mode]

                for (i, j), s_ji in s_matrix.elements.items():
                    s_dict[(index, i), (index, j)] = s_ji * mode_factor[i] / mode_factor[j]

            s_dict = _connect_s_matrices(
                s_dict, self.netlist["connections"], len(self.netlist["instances"])
            )

            # Build S matrix with desired ports
            ports = {
                (index, f"{ref_name}@{n}"): f"{port_name}@{n}"
                for (index, ref_name, modes), port_name in self.netlist["ports"].items()
                for n in range(modes)
            }

            elements = {
                (ports[i], ports[j]): s_ji
                for (i, j), s_ji in s_dict.items()
                if i in ports and j in ports
            }
            self._s_matrix = SMatrix(self.frequencies, elements, self.ports)

        return self._s_matrix


def _compare_angles(a, b):
    r = (a - b) % 360
    return r <= 1e-12 or 360 - r <= 1e-12


def _analyse_transform(reference):
    if reference.x_reflection:
        return True, False

    rotation = reference.rotation
    rotation_fraction = rotation % 90
    manhattan = rotation_fraction < 1e-12 or (90 - rotation_fraction < 1e-12)

    if not manhattan:
        return True, False

    translated = not numpy.allclose(reference.origin, (0, 0), atol=1e-12)
    rotated = not _compare_angles(rotation, 0)

    technology = reference.component.technology
    uniform = technology.background_medium.is_spatially_uniform and all(
        e.medium.is_spatially_uniform for e in technology.extrusion_specs
    )
    fully_anisotropic = technology.background_medium.is_fully_anisotropic or any(
        e.medium.is_fully_anisotropic for e in technology.extrusion_specs
    )
    in_plane_isotropic = (
        not fully_anisotropic
        and (
            not isinstance(technology.background_medium, tidy3d.AnisotropicMedium)
            or technology.background_medium.xx == technology.background_medium.yy
        )
        and all(
            (not isinstance(e.medium, tidy3d.AnisotropicMedium) or e.medium.xx == e.medium.yy)
            for e in technology.extrusion_specs
        )
    )

    requires_flattening = (
        (fully_anisotropic and rotated)
        or (not in_plane_isotropic and rotated and not _compare_angles(rotation, 180))
        or (not uniform and (translated or rotated))
    )

    requires_phase_correction = not requires_flattening and rotated
    return requires_flattening, requires_phase_correction


class CircuitModel(Model):
    """Model based on circuit-level S-parameter calculation.

    The component is expected to be composed of interconnected references.
    Scattering parameters are computed based on the S matrices from all
    references and their interconnections.

    The S matrix of each reference is calculated based on the active model
    of the reference's component. Each calculation is preceded by an update
    to the componoent's technology, the component itself, and its active
    model by calling :attr:`Reference.update`. They are reset to their
    original state after the :func:`CircuitModel.start` function is called.
    Keyword arguents in :attr:`Reference.s_matrix_kwargs` will be passed on
    to :func:`CircuitModel.start`.

    If a reference includes repetitions, it is flattened so that each
    instance is called separatelly.

    Args:
        mesh_refinement: Minimal number of mesh elements per wavelength used
          for mode solving.
        verbose: Flag setting the verbosity of mode solver runs.

    See also:
        `Circuit Model guide <../guides/Circuit_Model.ipynb>`__
    """

    def __init__(
        self,
        mesh_refinement: Optional[float] = None,
        verbose: bool = True,
    ):
        super().__init__(mesh_refinement=mesh_refinement, verbose=verbose)
        self.mesh_refinement = mesh_refinement
        self.verbose = verbose

    def __copy__(self):
        return CircuitModel(self.mesh_refinement, self.verbose)

    def __deepcopy__(self, memo=None):
        return CircuitModel(self.mesh_refinement, self.verbose)

    def __str__(self):
        return "CircuitModel"

    def __repr__(self):
        return "CircuitModel()"

    @staticmethod
    def clear_cache():
        """Clear the runtime cache for mode overlaps, but not the file cache."""
        _CircuitModelRunner.cache.clear()

    @staticmethod
    def cache_size(size: int = None):
        """Get/set the runtime cache size for mode overlaps.

        Args:
            size: Set a new cache size. A negative value removes the size limit.

        Returns:
            Current cache size.
        """
        if size is None:
            size = _CircuitModelRunner.cache.size
        else:
            _CircuitModelRunner.cache.size = size
        return size

    def start(
        self,
        component: Component,
        frequencies: Sequence[float],
        updates: dict = {},
        chain_technology_updates=True,
        **kwargs,
    ) -> Any:
        """Start computing the S matrix response from a component.

        Args:
            component: Component from which to compute the S matrix.
            frequencies: Sequence of frequencies at which to perform the
              computation.
            updates: Dictionary of parameter updates to be applied to
              components, technologies, and models for references within the
              main component. See below for further information.
            chain_technology_updates: if set, a technology update will trigger
              an update for all components using that technology.
            **kwargs: Keyword arguments passed to reference models.

        Returns:
            Result object with attributes ``status`` and ``s_matrix``.

        The ``'updates'`` dictionary contains keyword arguments for the
        :func:`Reference.update` function for the references in the component
        dependency tree, such that, when the S parameter of a specific reference
        are computed, that reference can be updated without affecting others
        using the same component.

        Each key in the dictionary is used as a reference specification. It must
        be a tuple with any number of the following:

        - ``name: str|re.Pattern``: selects any reference whose component name
          matches the given regex.

        - ``i: int``, directly following ``name``: limits the selection to
          ``reference[i]`` from the list of references matching the name. A
          negative value will match all list items.

        - ``j: int``, directly following ``i``: filter the previous list of
          references to only those with repetition index ``j`` in a reference
          array.

        - ``None``: matches any reference at any depth.

        Examples:
            >>> updates = {
            ...     # Apply component updates to the first "ARM" reference in
            ...     # the main component
            ...     ("ARM", 0): {"component_updates": {"radius": 10}}
            ...     # Apply model updates to the second "BEND" reference under
            ...     # any "ARM" references in the main component
            ...     ("SUB", "BEND", 1): {"model_updates": {"verbose": False}}
            ...     # Apply model updates to references with component name
            ...     # starting with "COMP_" prefix, at any subcomponent depth
            ...     (None, "COMP.*"): {"technology_updates": {"thickness": 0.3}}
            ... }
            >>> s_matrix = component.s_matrix(
            ...     frequencies, model_kwargs={"updates": updates}
            ... )

        See also:
            - `Circuit Model guide <../guides/Circuit_Model.ipynb>`__
            - `Cascaded Rings Filter example
              <../examples/Cascaded_Rings_Filter.ipynb>`__
        """
        frequencies = numpy.array(frequencies, dtype=float, ndmin=1)
        netlist = component.get_netlist()
        # In the circuit model, virtual connections behave like real connections
        netlist["connections"].extend(netlist["virtual connections"])

        _, reference_index_map = component.get_instance_maps()

        # 'inputs' is not supported in CircuitModel
        kwargs = dict(kwargs)
        if "inputs" in kwargs:
            del kwargs["inputs"]

        # Check that all keys are valid
        valid_updates = []
        for key, value in updates.items():
            if len(key) == 0:
                raise KeyError("Empty key in 'updates' is not allowed.")
            valid_key = []
            last_is_none = False
            valid_ints = 0
            for i, k in enumerate(key):
                if k is None:
                    if not last_is_none:
                        valid_key.append(None)
                    last_is_none = True
                    valid_ints = 0
                elif isinstance(k, str):
                    valid_key.append(re.compile(k))
                    last_is_none = False
                    valid_ints = 2
                elif isinstance(k, re.Pattern):
                    valid_key.append(k)
                    last_is_none = False
                    valid_ints = 2
                elif isinstance(k, int) and valid_ints > 0:
                    valid_key.append(k)
                    last_is_none = False
                    valid_ints -= 1
                else:
                    raise RuntimeError(
                        f"Invalid value in position {i} in key {tuple(key)}: {k}. Expected a "
                        "string, a compiled regular expression pattern, "
                        + ("an integer, " if valid_ints > 0 else "")
                        + "or 'None'."
                    )
            valid_updates.append((tuple(valid_key), value))

        runners = {}
        match_counts = {}
        netlist["phase corrections"] = [False] * len(netlist["instances"])

        for index, reference in enumerate(netlist["instances"]):
            ref_component = reference.component

            if ref_component.active_model is None:
                # Check if the model is really needed
                if any(
                    index0 == index or index1 == index
                    for (index0, _, _), (index1, _, _) in netlist["connections"]
                ) or any(i == index for i, _, _ in netlist["ports"]):
                    raise RuntimeError(f"Component '{ref_component.name}' has no active model.")
                continue

            # Match updates with current reference
            reference_updates = {}
            technology_updates = {}
            component_updates = {}
            model_updates = {}
            for update_index, (key, value) in enumerate(valid_updates):
                if key[0] is None:
                    reference_updates[key] = value
                    key = key[1:]
                if len(key) == 0:
                    technology_updates.update(value.get("technology_updates", {}))
                    component_updates.update(value.get("component_updates", {}))
                    model_updates.update(value.get("model_updates", {}))
                else:
                    spec_len = 1
                    reference_index = -1
                    if len(key) > 1 and isinstance(key[1], int):
                        reference_index = key[1]
                        spec_len = 2
                        if len(key) > 2 and isinstance(key[2], int):
                            spec_len = 3
                    if key[0].match(ref_component.name) and (
                        spec_len < 3 or key[2] == reference_index_map[index][1]
                    ):
                        if reference_index >= 0:
                            match_counts[key] = match_counts.get(key, -1) + 1
                            if reference_index == match_counts[key]:
                                reference_index = -1
                        if reference_index < 0:
                            if len(key) == spec_len:
                                technology_updates.update(value.get("technology_updates", {}))
                                component_updates.update(value.get("component_updates", {}))
                                model_updates.update(value.get("model_updates", {}))
                            else:
                                reference_updates[key[spec_len:]] = value

            # Apply required updates
            reset_list = reference.update(
                technology_updates=technology_updates,
                component_updates=component_updates,
                model_updates=model_updates,
                chain_technology_updates=chain_technology_updates,
            )

            # Account for reference transformations
            inner_component = ref_component
            requires_flattening, requires_phase_correction = _analyse_transform(reference)
            if requires_flattening:
                inner_component = reference.transformed_component(ref_component.name + "-X")
            elif requires_phase_correction:
                # S matrix correction factor depends on the mode solver for transformed ports
                netlist["phase corrections"][index] = True
                for port_name, port in ref_component.ports.items():
                    if isinstance(port, Port):
                        runners[(index, port_name, 0)] = _Tidy3DModeSolverRunner(
                            port,
                            frequencies[:1],
                            self.mesh_refinement,
                            ref_component.technology,
                            verbose=self.verbose,
                        )
                        runners[(index, port_name, 1)] = _Tidy3DModeSolverRunner(
                            reference[port_name],
                            frequencies[:1],
                            self.mesh_refinement,
                            ref_component.technology,
                            verbose=self.verbose,
                        )

            s_matrix_kwargs = {"updates": {}, "chain_technology_updates": chain_technology_updates}
            s_matrix_kwargs.update(kwargs)
            s_matrix_kwargs.update(reference_updates.pop("s_matrix_kwargs", {}))
            if reference.s_matrix_kwargs is not None:
                s_matrix_kwargs.update(reference.s_matrix_kwargs)
            s_matrix_kwargs["updates"].update(reference_updates)

            runners[index] = reference.component.active_model.start(
                inner_component, frequencies, **s_matrix_kwargs
            )

            # Reset all updates
            for item, kwds in reset_list:
                item.parametric_kwargs = kwds
                item.update()

        return _CircuitModelRunner(netlist, runners, frequencies, component.name, component.ports)

    @property
    def as_bytes(self) -> bytes:
        """Serialize this model."""
        version = 0
        return struct.pack(
            "<B?d",
            version,
            self.verbose,
            0 if self.mesh_refinement is None else self.mesh_refinement,
        )

    @classmethod
    def from_bytes(cls, byte_repr: bytes) -> Model:
        """De-serialize this model."""
        (version, verbose, mesh_refinement) = struct.unpack("<B?d", byte_repr)
        if version != 0:
            raise RuntimeError("Unsuported CircuitModel version.")

        if mesh_refinement <= 0:
            mesh_refinement = None
        return cls(mesh_refinement, verbose)


register_model_class(CircuitModel)
