# __version__= "034200.3.0"
# __version_imas_dd__= "3.42.0"
# __imas_dd_git_commit__= "a3964a20fdef534f4a3803a74d91e87fa8f3070b"
# __imas_dd_git_branch__= "(master/3)"
#
from idspy_dictionaries.dataclasses_idsschema import idspy_dataclass, IdsBaseClass, StructArray
from dataclasses import field
import numpy as np
from typing import Optional


@idspy_dataclass(repr=False, slots=True)
class GenericGridDynamicSpaceDimensionObjectBoundary(IdsBaseClass):
    """

    :ivar index : Index of this (n-1)-dimensional boundary object
    :ivar neighbours : List of indices of the n-dimensional objects adjacent to the given n-dimensional object. An object can possibly have multiple neighbours on a boundary
    """

    class Meta:
        name = "generic_grid_dynamic_space_dimension_object_boundary"
        is_root_ids = False

    index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    neighbours: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=int),
        metadata={
            "imas_type": "INT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridDynamicSpaceDimensionObject(IdsBaseClass):
    """

    :ivar boundary : Set of  (n-1)-dimensional objects defining the boundary of this n-dimensional object
    :ivar geometry : Geometry data associated with the object, its detailed content is defined by ../../geometry_content. Its dimension depends on the type of object, geometry and coordinate considered.
    :ivar nodes : List of nodes forming this object (indices to objects_per_dimension(1)%object(:) in Fortran notation)
    :ivar measure : Measure of the space object, i.e. physical size (length for 1d, area for 2d, volume for 3d objects,...)
    :ivar geometry_2d : 2D geometry data associated with the object. Its dimension depends on the type of object, geometry and coordinate considered. Typically, the first dimension represents the object coordinates, while the second dimension would represent the values of the various degrees of freedom of the finite element attached to the object.
    """

    class Meta:
        name = "generic_grid_dynamic_space_dimension_object"
        is_root_ids = False

    boundary: Optional[GenericGridDynamicSpaceDimensionObjectBoundary] = field(
        default_factory=lambda: StructArray(
            type=GenericGridDynamicSpaceDimensionObjectBoundary
        ),
        metadata={
            "imas_type": "generic_grid_dynamic_space_dimension_object_boundary",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": GenericGridDynamicSpaceDimensionObjectBoundary,
        },
    )
    geometry: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": np.ndarray,
        },
    )
    nodes: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=int),
        metadata={
            "imas_type": "INT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": np.ndarray,
        },
    )
    measure: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    geometry_2d: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 2, dtype=float),
        metadata={
            "imas_type": "FLT_2D",
            "ndims": 2,
            "coordinates": {"coordinate1": "1...N", "coordinate2": "1...N"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridDynamicGridSubsetElementObject(IdsBaseClass):
    """

    :ivar space : Index of the space from which that object is taken
    :ivar dimension : Dimension of the object - using the convention  1=nodes, 2=edges, 3=faces, 4=cells/volumes
    :ivar index : Object index
    """

    class Meta:
        name = "generic_grid_dynamic_grid_subset_element_object"
        is_root_ids = False

    space: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    dimension: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridDynamicSpaceDimension(IdsBaseClass):
    """

    :ivar object : Set of objects for a given dimension
    :ivar geometry_content : Content of the ../object/geometry node for this dimension
    """

    class Meta:
        name = "generic_grid_dynamic_space_dimension"
        is_root_ids = False

    object: Optional[GenericGridDynamicSpaceDimensionObject] = field(
        default_factory=lambda: StructArray(
            type=GenericGridDynamicSpaceDimensionObject
        ),
        metadata={
            "imas_type": "generic_grid_dynamic_space_dimension_object",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": GenericGridDynamicSpaceDimensionObject,
        },
    )
    geometry_content: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridDynamicGridSubsetMetric(IdsBaseClass):
    """

    :ivar jacobian : Metric Jacobian
    :ivar tensor_covariant : Covariant metric tensor, given on each element of the subgrid (first dimension)
    :ivar tensor_contravariant : Contravariant metric tensor, given on each element of the subgrid (first dimension)
    """

    class Meta:
        name = "generic_grid_dynamic_grid_subset_metric"
        is_root_ids = False

    jacobian: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../element"},
            "field_type": np.ndarray,
        },
    )
    tensor_covariant: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 3, dtype=float),
        metadata={
            "imas_type": "FLT_3D",
            "ndims": 3,
            "coordinates": {
                "coordinate1": "../../element",
                "coordinate2": "1...N",
                "coordinate3": "1...N",
            },
            "field_type": np.ndarray,
        },
    )
    tensor_contravariant: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 5, dtype=float),
        metadata={
            "imas_type": "FLT_3D",
            "ndims": 5,
            "coordinates": {
                "coordinate1": "../../element",
                "coordinate2": "1...N",
                "coordinate2_same_as": "../tensor_covariant",
                "coordinate3": "1...N",
                "coordinate3_same_as": "../tensor_covariant",
            },
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridDynamicGridSubsetElement(IdsBaseClass):
    """

    :ivar object : Set of objects defining the element
    """

    class Meta:
        name = "generic_grid_dynamic_grid_subset_element"
        is_root_ids = False

    object: Optional[GenericGridDynamicGridSubsetElementObject] = field(
        default_factory=lambda: StructArray(
            type=GenericGridDynamicGridSubsetElementObject
        ),
        metadata={
            "imas_type": "generic_grid_dynamic_grid_subset_element_object",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": GenericGridDynamicGridSubsetElementObject,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridDynamicSpace(IdsBaseClass):
    """

    :ivar identifier : Space identifier
    :ivar geometry_type : Type of space geometry (0: standard, 1:Fourier, &gt;1: Fourier with periodicity)
    :ivar coordinates_type : Type of coordinates describing the physical space, for every coordinate of the space. The size of this node therefore defines the dimension of the space. The meaning of these predefined integer constants can be found in the Data Dictionary under utilities/coordinate_identifier.xml
    :ivar objects_per_dimension : Definition of the space objects for every dimension (from one to the dimension of the highest-dimensional objects). The index correspond to 1=nodes, 2=edges, 3=faces, 4=cells/volumes, .... For every index, a collection of objects of that dimension is described.
    """

    class Meta:
        name = "generic_grid_dynamic_space"
        is_root_ids = False

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    geometry_type: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    coordinates_type: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=int),
        metadata={
            "imas_type": "INT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": np.ndarray,
        },
    )
    objects_per_dimension: Optional[GenericGridDynamicSpaceDimension] = field(
        default_factory=lambda: StructArray(
            type=GenericGridDynamicSpaceDimension
        ),
        metadata={
            "imas_type": "generic_grid_dynamic_space_dimension",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": GenericGridDynamicSpaceDimension,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridDynamicGridSubset(IdsBaseClass):
    """

    :ivar identifier : Grid subset identifier
    :ivar dimension : Space dimension of the grid subset elements, using the convention 1=nodes, 2=edges, 3=faces, 4=cells/volumes
    :ivar element : Set of elements defining the grid subset. An element is defined by a combination of objects from potentially all spaces
    :ivar base : Set of bases for the grid subset. For each base, the structure describes the projection of the base vectors on the canonical frame of the grid.
    :ivar metric : Metric of the canonical frame onto Cartesian coordinates
    """

    class Meta:
        name = "generic_grid_dynamic_grid_subset"
        is_root_ids = False

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    dimension: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    element: Optional[GenericGridDynamicGridSubsetElement] = field(
        default_factory=lambda: StructArray(
            type=GenericGridDynamicGridSubsetElement
        ),
        metadata={
            "imas_type": "generic_grid_dynamic_grid_subset_element",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": GenericGridDynamicGridSubsetElement,
        },
    )
    base: Optional[GenericGridDynamicGridSubsetMetric] = field(
        default_factory=lambda: StructArray(
            type=GenericGridDynamicGridSubsetMetric
        ),
        metadata={
            "imas_type": "generic_grid_dynamic_grid_subset_metric",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": GenericGridDynamicGridSubsetMetric,
        },
    )
    metric: Optional[GenericGridDynamicGridSubsetMetric] = field(
        default=None,
        metadata={
            "imas_type": "generic_grid_dynamic_grid_subset_metric",
            "field_type": GenericGridDynamicGridSubsetMetric,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class GenericGridDynamic(IdsBaseClass):
    """

    :ivar identifier : Grid identifier
    :ivar path : Path of the grid, including the IDS name, in case of implicit reference to a grid_ggd node described in another IDS. To be filled only if the grid is not described explicitly in this grid_ggd structure. Example syntax: &#39;wall:0/description_ggd(1)/grid_ggd&#39;, means that the grid is located in the wall IDS, occurrence 0, with ids path &#39;description_ggd(1)/grid_ggd&#39;. See the link below for more details about IDS paths
    :ivar space : Set of grid spaces
    :ivar grid_subset : Grid subsets
    """

    class Meta:
        name = "generic_grid_dynamic"
        is_root_ids = False

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    path: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    space: Optional[GenericGridDynamicSpace] = field(
        default_factory=lambda: StructArray(type=GenericGridDynamicSpace),
        metadata={
            "imas_type": "generic_grid_dynamic_space",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": GenericGridDynamicSpace,
        },
    )
    grid_subset: Optional[GenericGridDynamicGridSubset] = field(
        default_factory=lambda: StructArray(type=GenericGridDynamicGridSubset),
        metadata={
            "imas_type": "generic_grid_dynamic_grid_subset",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": GenericGridDynamicGridSubset,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class BTorVacuum1(IdsBaseClass):
    """

    :ivar r0 : Reference major radius where the vacuum toroidal magnetic field is given (usually a fixed position such as the middle of the vessel at the equatorial midplane)
    :ivar b0 : Vacuum toroidal field at R0 [T]; Positive sign means anti-clockwise when viewing from above. The product R0B0 must be consistent with the b_tor_vacuum_r field of the tf IDS.
    """

    class Meta:
        name = "b_tor_vacuum_1"
        is_root_ids = False

    r0: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    b0: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "/time"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class IdentifierDynamicAos3(IdsBaseClass):
    """

    :ivar name : Short string identifier
    :ivar index : Integer identifier (enumeration index within a list). Private identifier values must be indicated by a negative index.
    :ivar description : Verbose description
    """

    class Meta:
        name = "identifier_dynamic_aos3"
        is_root_ids = False

    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    description: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )


@idspy_dataclass(repr=False, slots=True)
class CoreRadialGrid(IdsBaseClass):
    """

    :ivar rho_tor_norm : Normalised toroidal flux coordinate. The normalizing value for rho_tor_norm, is the toroidal flux coordinate at the equilibrium boundary (LCFS or 99.x % of the LCFS in case of a fixed boundary equilibium calculation, see time_slice/boundary/b_flux_pol_norm in the equilibrium IDS)
    :ivar rho_tor : Toroidal flux coordinate = sqrt(phi/(pi*b0)), where the toroidal magnetic field, b0, corresponds to that stored in vacuum_toroidal_field/b0 and pi can be found in the IMAS constants
    :ivar rho_pol_norm : Normalised poloidal flux coordinate = sqrt((psi(rho)-psi(magnetic_axis)) / (psi(LCFS)-psi(magnetic_axis)))
    :ivar psi : Poloidal magnetic flux
    :ivar volume : Volume enclosed inside the magnetic surface
    :ivar area : Cross-sectional area of the flux surface
    :ivar surface : Surface area of the toroidal flux surface
    :ivar psi_magnetic_axis : Value of the poloidal magnetic flux at the magnetic axis (useful to normalize the psi array values when the radial grid doesn&#39;t go from the magnetic axis to the plasma boundary)
    :ivar psi_boundary : Value of the poloidal magnetic flux at the plasma boundary (useful to normalize the psi array values when the radial grid doesn&#39;t go from the magnetic axis to the plasma boundary)
    """

    class Meta:
        name = "core_radial_grid"
        is_root_ids = False

    rho_tor_norm: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": np.ndarray,
        },
    )
    rho_tor: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    rho_pol_norm: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    psi: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    volume: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    area: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    surface: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    psi_magnetic_axis: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    psi_boundary: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class SignalFlt1D(IdsBaseClass):
    """

    :ivar data : Data
    :ivar time : Time
    """

    class Meta:
        name = "signal_flt_1d"
        is_root_ids = False

    data: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../time"},
            "field_type": np.ndarray,
        },
    )
    time: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "flt_1d_type",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class IdsProvenanceNodeReference(IdsBaseClass):
    """

    :ivar name : Reference name
    :ivar timestamp : Date and time (UTC) at which the reference was created, expressed in a human readable form (ISO 8601) : the format of the string shall be : YYYY-MM-DDTHH:MM:SSZ. Example : 2020-07-24T14:19:00Z
    """

    class Meta:
        name = "ids_provenance_node_reference"
        is_root_ids = False

    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    timestamp: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )


@idspy_dataclass(repr=False, slots=True)
class IdsProvenanceNode(IdsBaseClass):
    """

    :ivar path : Path of the node within the IDS, following the syntax given in the link below. If empty, means the provenance information applies to the whole IDS.
    :ivar reference : List of references used to populate or calculate this node, identified as explained below. In case the node is the result of of a calculation / data processing, the reference is an input to the process described in the &#34;code&#34; structure at the root of the IDS. The reference can be an IDS (identified by a URI or a persitent identifier, see syntax in the link below) or non-IDS data imported directly from an non-IMAS database (identified by the command used to import the reference, or the persistent identifier of the data reference). Often data are obtained by a chain of processes, however only the last process input are recorded here. The full chain of provenance has then to be reconstructed recursively from the provenance information contained in the data references.
    """

    class Meta:
        name = "ids_provenance_node"
        is_root_ids = False

    path: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    reference: Optional[IdsProvenanceNodeReference] = field(
        default_factory=lambda: StructArray(type=IdsProvenanceNodeReference),
        metadata={
            "imas_type": "ids_provenance_node_reference",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": IdsProvenanceNodeReference,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class Library(IdsBaseClass):
    """

    :ivar name : Name of software
    :ivar description : Short description of the software (type, purpose)
    :ivar commit : Unique commit reference of software
    :ivar version : Unique version (tag) of software
    :ivar repository : URL of software repository
    :ivar parameters : List of the code specific parameters in XML format
    """

    class Meta:
        name = "library"
        is_root_ids = False

    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    description: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    commit: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    version: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    repository: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    parameters: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )


@idspy_dataclass(repr=False, slots=True)
class IdsProvenance(IdsBaseClass):
    """

    :ivar node : Set of IDS nodes for which the provenance is given. The provenance information applies to the whole structure below the IDS node. For documenting provenance information for the whole IDS, set the size of this array of structure to 1 and leave the child &#34;path&#34; node empty
    """

    class Meta:
        name = "ids_provenance"
        is_root_ids = False

    node: Optional[IdsProvenanceNode] = field(
        default_factory=lambda: StructArray(type=IdsProvenanceNode),
        metadata={
            "imas_type": "ids_provenance_node",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": IdsProvenanceNode,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class IdsProperties(IdsBaseClass):
    """

    :ivar comment : Any comment describing the content of this IDS
    :ivar name : User-defined name for this IDS occurrence
    :ivar homogeneous_time : This node must be filled (with 0, 1, or 2) for the IDS to be valid. If 1, the time of this IDS is homogeneous, i.e. the time values for this IDS are stored in the time node just below the root of this IDS. If 0, the time values are stored in the various time fields at lower levels in the tree. In the case only constant or static nodes are filled within the IDS, homogeneous_time must be set to 2
    :ivar source : Source of the data (any comment describing the origin of the data : code, path to diagnostic signals, processing method, ...). Superseeded by the new provenance structure.
    :ivar provider : Name of the person in charge of producing this data
    :ivar creation_date : Date at which this data has been produced
    :ivar provenance : Provenance information about this IDS
    """

    class Meta:
        name = "ids_properties"
        is_root_ids = False

    comment: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    homogeneous_time: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    source: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    provider: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    creation_date: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    provenance: Optional[IdsProvenance] = field(
        default=None,
        metadata={"imas_type": "ids_provenance", "field_type": IdsProvenance},
    )


@idspy_dataclass(repr=False, slots=True)
class Code(IdsBaseClass):
    """

    :ivar name : Name of software generating IDS
    :ivar description : Short description of the software (type, purpose)
    :ivar commit : Unique commit reference of software
    :ivar version : Unique version (tag) of software
    :ivar repository : URL of software repository
    :ivar parameters : List of the code specific parameters in XML format
    :ivar output_flag : Output flag : 0 means the run is successful, other values mean some difficulty has been encountered, the exact meaning is then code specific. Negative values mean the result shall not be used.
    :ivar library : List of external libraries used by the code that has produced this IDS
    """

    class Meta:
        name = "code"
        is_root_ids = False

    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    description: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    commit: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    version: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    repository: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    parameters: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    output_flag: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=int),
        metadata={
            "imas_type": "INT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "/time"},
            "field_type": np.ndarray,
        },
    )
    library: Optional[Library] = field(
        default_factory=lambda: StructArray(type=Library),
        metadata={
            "imas_type": "library",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": Library,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesChargeStateD(IdsBaseClass):
    """

    :ivar temperature : Temperature
    :ivar density : Density (thermal+non-thermal)
    :ivar density_fast : Density of fast (non-thermal) particles
    :ivar pressure : Pressure
    :ivar pressure_fast_perpendicular : Fast (non-thermal) perpendicular pressure
    :ivar pressure_fast_parallel : Fast (non-thermal) parallel pressure
    :ivar velocity_tor : Toroidal velocity
    :ivar velocity_phi : Toroidal velocity
    :ivar velocity_pol : Poloidal velocity
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_charge_state_d"
        is_root_ids = False

    temperature: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    density: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    density_fast: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure_fast_perpendicular: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure_fast_parallel: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    velocity_tor: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    velocity_phi: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    velocity_pol: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesChargeState(IdsBaseClass):
    """

    :ivar z_min : Minimum Z of the charge state bundle
    :ivar z_max : Maximum Z of the charge state bundle
    :ivar label : String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)
    :ivar name : String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)
    :ivar vibrational_level : Vibrational level (can be bundled)
    :ivar vibrational_mode : Vibrational mode of this state, e.g. &#34;A_g&#34;. Need to define, or adopt a standard nomenclature.
    :ivar is_neutral : Flag specifying if this state corresponds to a neutral (1) or not (0)
    :ivar neutral_type : Neutral type (if the considered state is a neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast; 4: NBI
    :ivar electron_configuration : Configuration of atomic orbitals of this state, e.g. 1s2-2s1
    :ivar d_drho_tor_norm : Derivatives with respect to the normalised toroidal flux
    :ivar d2_drho_tor_norm2 : Second derivatives with respect to the normalised toroidal flux
    :ivar d_dt : Derivatives with respect to time
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_charge_state"
        is_root_ids = False

    z_min: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_max: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    label: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    vibrational_level: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    vibrational_mode: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    is_neutral: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    electron_configuration: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    d_drho_tor_norm: Optional[NumericsProfiles1DDerivativesChargeStateD] = (
        field(
            default=None,
            metadata={
                "imas_type": "numerics_profiles_1d_derivatives_charge_state_d",
                "field_type": NumericsProfiles1DDerivativesChargeStateD,
            },
        )
    )
    d2_drho_tor_norm2: Optional[NumericsProfiles1DDerivativesChargeStateD] = (
        field(
            default=None,
            metadata={
                "imas_type": "numerics_profiles_1d_derivatives_charge_state_d",
                "field_type": NumericsProfiles1DDerivativesChargeStateD,
            },
        )
    )
    d_dt: Optional[NumericsProfiles1DDerivativesChargeStateD] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_charge_state_d",
            "field_type": NumericsProfiles1DDerivativesChargeStateD,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesIonD(IdsBaseClass):
    """

    :ivar temperature : Temperature (average over charge states when multiple charge states are considered)
    :ivar density : Density (thermal+non-thermal) (sum over charge states when multiple charge states are considered)
    :ivar density_fast : Density of fast (non-thermal) particles (sum over charge states when multiple charge states are considered)
    :ivar pressure : Pressure (average over charge states when multiple charge states are considered)
    :ivar pressure_fast_perpendicular : Fast (non-thermal) perpendicular pressure  (average over charge states when multiple charge states are considered)
    :ivar pressure_fast_parallel : Fast (non-thermal) parallel pressure  (average over charge states when multiple charge states are considered)
    :ivar velocity_tor : Toroidal velocity (average over charge states when multiple charge states are considered)
    :ivar velocity_phi : Toroidal velocity (average over charge states when multiple charge states are considered)
    :ivar velocity_pol : Poloidal velocity (average over charge states when multiple charge states are considered)
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_ion_d"
        is_root_ids = False

    temperature: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    density: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    density_fast: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure_fast_perpendicular: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure_fast_parallel: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    velocity_tor: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    velocity_phi: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    velocity_pol: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesIon(IdsBaseClass):
    """

    :ivar a : Mass of atom
    :ivar z_ion : Ion charge (of the dominant ionisation state; lumped ions are allowed)
    :ivar z_n : Nuclear charge
    :ivar label : String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar name : String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar d_drho_tor_norm : Derivatives with respect to the normalised toroidal flux
    :ivar d2_drho_tor_norm2 : Second derivatives with respect to the normalised toroidal flux
    :ivar d_dt : Derivatives with respect to time
    :ivar multiple_states_flag : Multiple state calculation flag : 0-Only one state is considered; 1-Multiple states are considered and are described in the state structure
    :ivar state : Quantities related to the different states of the species (ionisation, energy, excitation, ...)
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_ion"
        is_root_ids = False

    a: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_ion: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_n: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    label: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    d_drho_tor_norm: Optional[NumericsProfiles1DDerivativesIonD] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_ion_d",
            "field_type": NumericsProfiles1DDerivativesIonD,
        },
    )
    d2_drho_tor_norm2: Optional[NumericsProfiles1DDerivativesIonD] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_ion_d",
            "field_type": NumericsProfiles1DDerivativesIonD,
        },
    )
    d_dt: Optional[NumericsProfiles1DDerivativesIonD] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_ion_d",
            "field_type": NumericsProfiles1DDerivativesIonD,
        },
    )
    multiple_states_flag: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    state: Optional[NumericsProfiles1DDerivativesChargeState] = field(
        default_factory=lambda: StructArray(
            type=NumericsProfiles1DDerivativesChargeState
        ),
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_charge_state",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsProfiles1DDerivativesChargeState,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DCurrentDerivatives(IdsBaseClass):
    """

    :ivar d_dt : Time derivative
    :ivar d_drho_tor_norm : Derivative with respect to the normalised toroidal flux
    :ivar d2_drho_tor_norm2 : Second derivative with respect to the normalised toroidal flux
    :ivar d_drho_tor : Derivative with respect to the toroidal flux
    :ivar d2_drho_tor2 : Second derivative with respect to the toroidal flux
    :ivar d_dt_cphi : Derivative with respect to time, at constant toroidal flux
    :ivar d_dt_crho_tor_norm : Derivative with respect to time, at constant normalised toroidal flux coordinate
    """

    class Meta:
        name = "numerics_profiles_1d_current_derivatives"
        is_root_ids = False

    d_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_drho_tor_norm: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2_drho_tor_norm2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_drho_tor: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2_drho_tor2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_dt_cphi: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_dt_crho_tor_norm: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesDepth5(IdsBaseClass):
    """

    :ivar d_dt : Time derivative
    :ivar d_drho_tor_norm : Derivative with respect to the normalised toroidal flux
    :ivar d2_drho_tor_norm2 : Second derivative with respect to the normalised toroidal flux
    :ivar d_drho_tor : Derivative with respect to the toroidal flux
    :ivar d2_drho_tor2 : Second derivative with respect to the toroidal flux
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_depth5"
        is_root_ids = False

    d_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_drho_tor_norm: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2_drho_tor_norm2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_drho_tor: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2_drho_tor2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesDepth4(IdsBaseClass):
    """

    :ivar d_dt : Time derivative
    :ivar d_drho_tor_norm : Derivative with respect to the normalised toroidal flux
    :ivar d2_drho_tor_norm2 : Second derivative with respect to the normalised toroidal flux
    :ivar d_drho_tor : Derivative with respect to the toroidal flux
    :ivar d2_drho_tor2 : Second derivative with respect to the toroidal flux
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_depth4"
        is_root_ids = False

    d_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_drho_tor_norm: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2_drho_tor_norm2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_drho_tor: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2_drho_tor2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesDepth3(IdsBaseClass):
    """

    :ivar d_dt : Time derivative
    :ivar d_drho_tor_norm : Derivative with respect to the normalised toroidal flux
    :ivar d2_drho_tor_norm2 : Second derivative with respect to the normalised toroidal flux
    :ivar d_drho_tor : Derivative with respect to the toroidal flux
    :ivar d2_drho_tor2 : Second derivative with respect to the toroidal flux
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_depth3"
        is_root_ids = False

    d_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_drho_tor_norm: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2_drho_tor_norm2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_drho_tor: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2_drho_tor2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesElectronsD(IdsBaseClass):
    """

    :ivar temperature : Temperature
    :ivar density : Density (thermal+non-thermal)
    :ivar density_fast : Density of fast (non-thermal) particles
    :ivar pressure : Pressure
    :ivar pressure_fast_perpendicular : Fast (non-thermal) perpendicular pressure
    :ivar pressure_fast_parallel : Fast (non-thermal) parallel pressure
    :ivar velocity_tor : Toroidal velocity
    :ivar velocity_phi : Toroidal velocity
    :ivar velocity_pol : Poloidal velocity
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_electrons_d"
        is_root_ids = False

    temperature: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    density: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    density_fast: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure_fast_perpendicular: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure_fast_parallel: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    velocity_tor: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    velocity_phi: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    velocity_pol: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesElectrons(IdsBaseClass):
    """

    :ivar d_drho_tor_norm : Derivatives with respect to the normalised toroidal flux
    :ivar d2_drho_tor_norm2 : Second derivatives with respect to the normalised toroidal flux
    :ivar d_dt : Derivatives with respect to time
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_electrons"
        is_root_ids = False

    d_drho_tor_norm: Optional[NumericsProfiles1DDerivativesElectronsD] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_electrons_d",
            "field_type": NumericsProfiles1DDerivativesElectronsD,
        },
    )
    d2_drho_tor_norm2: Optional[NumericsProfiles1DDerivativesElectronsD] = (
        field(
            default=None,
            metadata={
                "imas_type": "numerics_profiles_1d_derivatives_electrons_d",
                "field_type": NumericsProfiles1DDerivativesElectronsD,
            },
        )
    )
    d_dt: Optional[NumericsProfiles1DDerivativesElectronsD] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_electrons_d",
            "field_type": NumericsProfiles1DDerivativesElectronsD,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivativesTotalIons(IdsBaseClass):
    """

    :ivar n_i_total_over_n_e : Ratio of total ion density (sum over species and charge states) over electron density. (thermal+non-thermal)
    :ivar pressure_ion_total : Total thermal ion pressure
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives_total_ions"
        is_root_ids = False

    n_i_total_over_n_e: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    pressure_ion_total: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsProfiles1DDerivatives(IdsBaseClass):
    """

    :ivar grid : Radial grid
    :ivar electrons : Quantities related to the electrons
    :ivar ion : Quantities related to the different ion species
    :ivar d_drho_tor_norm : Derivatives of total ion quantities with respect to the normalised toroidal flux
    :ivar d2_drho_tor_norm2 : Second derivatives of total ion quantities with respect to the normalised toroidal flux
    :ivar d_dt : Derivatives of total ion quantities with respect to time
    :ivar dpsi_dt : Derivative of the poloidal flux profile with respect to time
    :ivar dpsi_dt_cphi : Derivative of the poloidal flux profile with respect to time, at constant toroidal flux
    :ivar dpsi_dt_crho_tor_norm : Derivative of the poloidal flux profile with respect to time, at constant normalised toroidal flux coordinate
    :ivar drho_tor_dt : Partial derivative of the toroidal flux coordinate profile with respect to time
    :ivar d_dvolume_drho_tor_dt : Partial derivative with respect to time of the derivative of the volume with respect to the toroidal flux coordinate
    :ivar dpsi_drho_tor : Derivative of the poloidal flux profile with respect to the toroidal flux coordinate
    :ivar d2psi_drho_tor2 : Second derivative of the poloidal flux profile with respect to the toroidal flux coordinate
    :ivar time : Time
    """

    class Meta:
        name = "numerics_profiles_1d_derivatives"
        is_root_ids = False

    grid: Optional[CoreRadialGrid] = field(
        default=None,
        metadata={
            "imas_type": "core_radial_grid",
            "field_type": CoreRadialGrid,
        },
    )
    electrons: Optional[NumericsProfiles1DDerivativesElectrons] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_electrons",
            "field_type": NumericsProfiles1DDerivativesElectrons,
        },
    )
    ion: Optional[NumericsProfiles1DDerivativesIon] = field(
        default_factory=lambda: StructArray(
            type=NumericsProfiles1DDerivativesIon
        ),
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_ion",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsProfiles1DDerivativesIon,
        },
    )
    d_drho_tor_norm: Optional[NumericsProfiles1DDerivativesTotalIons] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_total_ions",
            "field_type": NumericsProfiles1DDerivativesTotalIons,
        },
    )
    d2_drho_tor_norm2: Optional[NumericsProfiles1DDerivativesTotalIons] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_total_ions",
            "field_type": NumericsProfiles1DDerivativesTotalIons,
        },
    )
    d_dt: Optional[NumericsProfiles1DDerivativesTotalIons] = field(
        default=None,
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives_total_ions",
            "field_type": NumericsProfiles1DDerivativesTotalIons,
        },
    )
    dpsi_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    dpsi_dt_cphi: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    dpsi_dt_crho_tor_norm: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    drho_tor_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_dvolume_drho_tor_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    dpsi_drho_tor: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2psi_drho_tor2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    time: Optional[float] = field(
        default=9e40, metadata={"imas_type": "flt_type", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsRestart(IdsBaseClass):
    """

    :ivar names : Names of the restart files
    :ivar descriptions : Descriptions of the restart files
    :ivar time : Time
    """

    class Meta:
        name = "numerics_restart"
        is_root_ids = False

    names: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=str),
        metadata={
            "imas_type": "STR_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": np.ndarray,
        },
    )
    descriptions: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=str),
        metadata={
            "imas_type": "STR_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../names"},
            "field_type": np.ndarray,
        },
    )
    time: Optional[float] = field(
        default=9e40, metadata={"imas_type": "flt_type", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBc1DCurrentNew(IdsBaseClass):
    """

    :ivar identifier : Identifier of the boundary condition type. ID = 1: poloidal flux; 2: ip; 3: loop voltage; 4: undefined; 5: generic boundary condition y expressed as a1y&#39;+a2y=a3. 6: equation not solved;
    :ivar value : Value of the boundary condition. For ID = 1 to 3, only the first position in the vector is used. For ID = 5, all three positions are used, meaning respectively a1, a2, a3.
    :ivar rho_tor_norm : Position, in normalised toroidal flux, at which the boundary condition is imposed. Outside this position, the value of the data are considered to be prescribed.
    :ivar rho_tor : Position, in toroidal flux, at which the boundary condition is imposed. Outside this position, the value of the data are considered to be prescribed.
    """

    class Meta:
        name = "numerics_bc_1d_current_new"
        is_root_ids = False

    identifier: Optional[IdentifierDynamicAos3] = field(
        default_factory=lambda: StructArray(type=IdentifierDynamicAos3),
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": IdentifierDynamicAos3,
        },
    )
    value: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...3"},
            "field_type": np.ndarray,
        },
    )
    rho_tor_norm: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    rho_tor: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBc1DCurrent(IdsBaseClass):
    """

    :ivar identifier : Identifier of the boundary condition type. ID = 1: poloidal flux; 2: ip; 3: loop voltage; 4: undefined; 5: generic boundary condition y expressed as a1y&#39;+a2y=a3. 6: equation not solved;
    :ivar value : Value of the boundary condition. For ID = 1 to 3, only the first position in the vector is used. For ID = 5, all three positions are used, meaning respectively a1, a2, a3.
    :ivar rho_tor_norm : Position, in normalised toroidal flux, at which the boundary condition is imposed. Outside this position, the value of the data are considered to be prescribed.
    """

    class Meta:
        name = "numerics_bc_1d_current"
        is_root_ids = False

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    value: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...3"},
            "field_type": np.ndarray,
        },
    )
    rho_tor_norm: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBcGgdCurrent(IdsBaseClass):
    """

    :ivar identifier : Identifier of the boundary condition type. List of options TBD.
    :ivar grid_index : Index of the grid used to represent this quantity
    :ivar grid_subset_index : Index of the grid subset the data is provided on
    :ivar values : List of vector components, one list per element in the grid subset. First dimenstion: element index. Second dimension: vector component index (for ID = 1 to 3, only the first position in the vector is used. For ID = 5, all three positions are used, meaning respectively a1, a2, a3)
    """

    class Meta:
        name = "numerics_bc_ggd_current"
        is_root_ids = False

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    grid_index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    grid_subset_index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    values: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 2, dtype=float),
        metadata={
            "imas_type": "FLT_2D",
            "ndims": 2,
            "coordinates": {"coordinate1": "1...N", "coordinate2": "1...N"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBcGgdBc(IdsBaseClass):
    """

    :ivar identifier : Identifier of the boundary condition type. List of options TBD.
    :ivar grid_index : Index of the grid used to represent this quantity
    :ivar grid_subset_index : Index of the grid subset the data is provided on
    :ivar values : List of vector components, one list per element in the grid subset. First dimenstion: element index. Second dimension: vector component index (for ID = 1 to 3, only the first position in the vector is used. For ID = 5, all three positions are used, meaning respectively a1, a2, a3)
    """

    class Meta:
        name = "numerics_bc_ggd_bc"
        is_root_ids = False

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    grid_index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    grid_subset_index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    values: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 2, dtype=float),
        metadata={
            "imas_type": "FLT_2D",
            "ndims": 2,
            "coordinates": {"coordinate1": "1...N", "coordinate2": "1...N"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBc1DBc(IdsBaseClass):
    """

    :ivar identifier : Identifier of the boundary condition type. ID = 1: value of the field y; 2: radial derivative of the field (-dy/drho_tor); 3: scale length of the field y/(-dy/drho_tor); 4: flux; 5: generic boundary condition y expressed as a1y&#39;+a2y=a3. 6: equation not solved;
    :ivar value : Value of the boundary condition. For ID = 1 to 4, only the first position in the vector is used. For ID = 5, all three positions are used, meaning respectively a1, a2, a3.
    :ivar rho_tor_norm : Position, in normalised toroidal flux, at which the boundary condition is imposed. Outside this position, the value of the data are considered to be prescribed.
    """

    class Meta:
        name = "numerics_bc_1d_bc"
        is_root_ids = False

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    value: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...3"},
            "field_type": np.ndarray,
        },
    )
    rho_tor_norm: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBc1DElectrons(IdsBaseClass):
    """

    :ivar particles : Boundary condition for the electron density equation (density if ID = 1)
    :ivar energy : Boundary condition for the electron energy equation (temperature if ID = 1)
    """

    class Meta:
        name = "numerics_bc_1d_electrons"
        is_root_ids = False

    particles: Optional[NumericsBc1DBc] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_bc",
            "field_type": NumericsBc1DBc,
        },
    )
    energy: Optional[NumericsBc1DBc] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_bc",
            "field_type": NumericsBc1DBc,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBcGgdElectrons(IdsBaseClass):
    """

    :ivar particles : Boundary condition for the electron density equation (density if ID = 1), on various grid subsets
    :ivar energy : Boundary condition for the electron energy equation (temperature if ID = 1), on various grid subsets
    """

    class Meta:
        name = "numerics_bc_ggd_electrons"
        is_root_ids = False

    particles: Optional[NumericsBcGgdBc] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgdBc),
        metadata={
            "imas_type": "numerics_bc_ggd_bc",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBcGgdBc,
        },
    )
    energy: Optional[NumericsBcGgdBc] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgdBc),
        metadata={
            "imas_type": "numerics_bc_ggd_bc",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBcGgdBc,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBc1DIonChargeState(IdsBaseClass):
    """

    :ivar z_min : Minimum Z of the charge state bundle
    :ivar z_max : Maximum Z of the charge state bundle
    :ivar label : String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)
    :ivar name : String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)
    :ivar vibrational_level : Vibrational level (can be bundled)
    :ivar vibrational_mode : Vibrational mode of this state, e.g. &#34;A_g&#34;. Need to define, or adopt a standard nomenclature.
    :ivar is_neutral : Flag specifying if this state corresponds to a neutral (1) or not (0)
    :ivar neutral_type : Neutral type (if the considered state is a neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast; 4: NBI
    :ivar electron_configuration : Configuration of atomic orbitals of this state, e.g. 1s2-2s1
    :ivar particles : Boundary condition for the charge state density equation (density if ID = 1)
    :ivar energy : Boundary condition for the charge state energy equation (temperature if ID = 1)
    """

    class Meta:
        name = "numerics_bc_1d_ion_charge_state"
        is_root_ids = False

    z_min: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_max: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    label: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    vibrational_level: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    vibrational_mode: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    is_neutral: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    electron_configuration: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    particles: Optional[NumericsBc1DBc] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_bc",
            "field_type": NumericsBc1DBc,
        },
    )
    energy: Optional[NumericsBc1DBc] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_bc",
            "field_type": NumericsBc1DBc,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBcGgdIonChargeState(IdsBaseClass):
    """

    :ivar z_min : Minimum Z of the charge state bundle
    :ivar z_max : Maximum Z of the charge state bundle
    :ivar label : String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)
    :ivar name : String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)
    :ivar vibrational_level : Vibrational level (can be bundled)
    :ivar vibrational_mode : Vibrational mode of this state, e.g. &#34;A_g&#34;. Need to define, or adopt a standard nomenclature.
    :ivar is_neutral : Flag specifying if this state corresponds to a neutral (1) or not (0)
    :ivar neutral_type : Neutral type (if the considered state is a neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast; 4: NBI
    :ivar electron_configuration : Configuration of atomic orbitals of this state, e.g. 1s2-2s1
    :ivar particles : Boundary condition for the charge state density equation (density if ID = 1), on various grid subsets
    :ivar energy : Boundary condition for the charge state energy equation (temperature if ID = 1), on various grid subsets
    """

    class Meta:
        name = "numerics_bc_ggd_ion_charge_state"
        is_root_ids = False

    z_min: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_max: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    label: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    vibrational_level: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    vibrational_mode: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    is_neutral: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    electron_configuration: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    particles: Optional[NumericsBcGgdBc] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgdBc),
        metadata={
            "imas_type": "numerics_bc_ggd_bc",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBcGgdBc,
        },
    )
    energy: Optional[NumericsBcGgdBc] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgdBc),
        metadata={
            "imas_type": "numerics_bc_ggd_bc",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBcGgdBc,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBc1DIon(IdsBaseClass):
    """

    :ivar a : Mass of atom
    :ivar z_ion : Ion charge (of the dominant ionisation state; lumped ions are allowed)
    :ivar z_n : Nuclear charge
    :ivar label : String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar name : String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar particles : Boundary condition for the ion density equation (density if ID = 1)
    :ivar energy : Boundary condition for the ion energy equation (temperature if ID = 1)
    :ivar multiple_states_flag : Multiple states calculation flag : 0-Only one state is considered; 1-Multiple states are considered and are described in the state structure
    :ivar state : Quantities related to the different states of the species (ionisation, energy, excitation, ...)
    """

    class Meta:
        name = "numerics_bc_1d_ion"
        is_root_ids = False

    a: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_ion: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_n: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    label: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    particles: Optional[NumericsBc1DBc] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_bc",
            "field_type": NumericsBc1DBc,
        },
    )
    energy: Optional[NumericsBc1DBc] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_bc",
            "field_type": NumericsBc1DBc,
        },
    )
    multiple_states_flag: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    state: Optional[NumericsBc1DIonChargeState] = field(
        default_factory=lambda: StructArray(type=NumericsBc1DIonChargeState),
        metadata={
            "imas_type": "numerics_bc_1d_ion_charge_state",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBc1DIonChargeState,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBcGgdIon(IdsBaseClass):
    """

    :ivar a : Mass of atom
    :ivar z_ion : Ion charge (of the dominant ionisation state; lumped ions are allowed)
    :ivar z_n : Nuclear charge
    :ivar label : String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar name : String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar particles : Boundary condition for the ion density equation (density if ID = 1), on various grid subsets
    :ivar energy : Boundary condition for the ion energy equation (temperature if ID = 1), on various grid subsets
    :ivar multiple_states_flag : Multiple states calculation flag : 0-Only one state is considered; 1-Multiple states are considered and are described in the state structure
    :ivar state : Quantities related to the different states of the species (ionisation, energy, excitation, ...)
    """

    class Meta:
        name = "numerics_bc_ggd_ion"
        is_root_ids = False

    a: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_ion: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_n: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    label: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    particles: Optional[NumericsBcGgdBc] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgdBc),
        metadata={
            "imas_type": "numerics_bc_ggd_bc",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBcGgdBc,
        },
    )
    energy: Optional[NumericsBcGgdBc] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgdBc),
        metadata={
            "imas_type": "numerics_bc_ggd_bc",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBcGgdBc,
        },
    )
    multiple_states_flag: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    state: Optional[NumericsBcGgdIonChargeState] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgdIonChargeState),
        metadata={
            "imas_type": "numerics_bc_ggd_ion_charge_state",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBcGgdIonChargeState,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBc1D(IdsBaseClass):
    """

    :ivar current : Boundary condition for the current diffusion equation.
    :ivar electrons : Quantities related to the electrons
    :ivar ion : Quantities related to the different ion species
    :ivar energy_ion_total : Boundary condition for the ion total (sum over ion species) energy equation (temperature if ID = 1)
    :ivar momentum_tor : Boundary condition for the total plasma toroidal momentum equation (summed over ion species and electrons) (momentum if ID = 1)
    :ivar momentum_phi : Boundary condition for the total plasma toroidal momentum equation (summed over ion species and electrons) (momentum if ID = 1)
    :ivar time : Time
    """

    class Meta:
        name = "numerics_bc_1d"
        is_root_ids = False

    current: Optional[NumericsBc1DCurrent] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_current",
            "field_type": NumericsBc1DCurrent,
        },
    )
    electrons: Optional[NumericsBc1DElectrons] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_electrons",
            "field_type": NumericsBc1DElectrons,
        },
    )
    ion: Optional[NumericsBc1DIon] = field(
        default_factory=lambda: StructArray(type=NumericsBc1DIon),
        metadata={
            "imas_type": "numerics_bc_1d_ion",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBc1DIon,
        },
    )
    energy_ion_total: Optional[NumericsBc1DBc] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_bc",
            "field_type": NumericsBc1DBc,
        },
    )
    momentum_tor: Optional[NumericsBc1DBc] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_bc",
            "field_type": NumericsBc1DBc,
        },
    )
    momentum_phi: Optional[NumericsBc1DBc] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_1d_bc",
            "field_type": NumericsBc1DBc,
        },
    )
    time: Optional[float] = field(
        default=9e40, metadata={"imas_type": "flt_type", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsBcGgd(IdsBaseClass):
    """

    :ivar grid : Grid description
    :ivar current : Boundary condition for the current diffusion equation, on various grid subsets
    :ivar electrons : Quantities related to the electrons
    :ivar ion : Quantities related to the different ion species
    :ivar time : Time
    """

    class Meta:
        name = "numerics_bc_ggd"
        is_root_ids = False

    grid: Optional[GenericGridDynamic] = field(
        default=None,
        metadata={
            "imas_type": "generic_grid_dynamic",
            "field_type": GenericGridDynamic,
        },
    )
    current: Optional[NumericsBcGgdCurrent] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgdCurrent),
        metadata={
            "imas_type": "numerics_bc_ggd_current",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBcGgdCurrent,
        },
    )
    electrons: Optional[NumericsBcGgdElectrons] = field(
        default=None,
        metadata={
            "imas_type": "numerics_bc_ggd_electrons",
            "field_type": NumericsBcGgdElectrons,
        },
    )
    ion: Optional[NumericsBcGgdIon] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgdIon),
        metadata={
            "imas_type": "numerics_bc_ggd_ion",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsBcGgdIon,
        },
    )
    time: Optional[float] = field(
        default=9e40, metadata={"imas_type": "flt_type", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsConvergenceEquationsSingleDelta(IdsBaseClass):
    """

    :ivar value : Value of the relative deviation
    :ivar expression : Expression used by the solver to calculate the relative deviation
    """

    class Meta:
        name = "numerics_convergence_equations_single_delta"
        is_root_ids = False

    value: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    expression: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsConvergenceEquationsSingle(IdsBaseClass):
    """

    :ivar iterations_n : Number of iterations carried out in the convergence loop
    :ivar delta_relative : Relative deviation on the primary quantity of the transport equation between the present and the  previous iteration of the solver
    """

    class Meta:
        name = "numerics_convergence_equations_single"
        is_root_ids = False

    iterations_n: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    delta_relative: Optional[NumericsConvergenceEquationsSingleDelta] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single_delta",
            "field_type": NumericsConvergenceEquationsSingleDelta,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsConvergenceEquationsIonChargeState(IdsBaseClass):
    """

    :ivar z_min : Minimum Z of the charge state bundle
    :ivar z_max : Maximum Z of the charge state bundle
    :ivar label : String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)
    :ivar name : String identifying charge state (e.g. C+, C+2 , C+3, C+4, C+5, C+6, ...)
    :ivar vibrational_level : Vibrational level (can be bundled)
    :ivar vibrational_mode : Vibrational mode of this state, e.g. &#34;A_g&#34;. Need to define, or adopt a standard nomenclature.
    :ivar is_neutral : Flag specifying if this state corresponds to a neutral (1) or not (0)
    :ivar neutral_type : Neutral type (if the considered state is a neutral), in terms of energy. ID =1: cold; 2: thermal; 3: fast; 4: NBI
    :ivar electron_configuration : Configuration of atomic orbitals of this state, e.g. 1s2-2s1
    :ivar particles : Convergence details of the charge state density equation
    :ivar energy : Convergence details of the charge state energy equation
    """

    class Meta:
        name = "numerics_convergence_equations_ion_charge_state"
        is_root_ids = False

    z_min: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_max: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    label: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    vibrational_level: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    vibrational_mode: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    is_neutral: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    neutral_type: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    electron_configuration: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    particles: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single",
            "field_type": NumericsConvergenceEquationsSingle,
        },
    )
    energy: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single",
            "field_type": NumericsConvergenceEquationsSingle,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsConvergenceEquationsIon(IdsBaseClass):
    """

    :ivar a : Mass of atom
    :ivar z_ion : Ion charge (of the dominant ionisation state; lumped ions are allowed)
    :ivar z_n : Nuclear charge
    :ivar label : String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar name : String identifying ion (e.g. H+, D+, T+, He+2, C+, ...)
    :ivar particles : Convergence details of the  ion density equation
    :ivar energy : Convergence details of the ion energy equation
    :ivar multiple_states_flag : Multiple state calculation flag : 0-Only one state is considered; 1-Multiple states are considered and are described in the state structure
    :ivar state : Convergence details of the related to the different states transport equations
    """

    class Meta:
        name = "numerics_convergence_equations_ion"
        is_root_ids = False

    a: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_ion: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    z_n: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )
    label: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    particles: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single",
            "field_type": NumericsConvergenceEquationsSingle,
        },
    )
    energy: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single",
            "field_type": NumericsConvergenceEquationsSingle,
        },
    )
    multiple_states_flag: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    state: Optional[NumericsConvergenceEquationsIonChargeState] = field(
        default_factory=lambda: StructArray(
            type=NumericsConvergenceEquationsIonChargeState
        ),
        metadata={
            "imas_type": "numerics_convergence_equations_ion_charge_state",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsConvergenceEquationsIonChargeState,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsConvergenceEquationsElectrons(IdsBaseClass):
    """

    :ivar particles : Convergence details of the electron density equation
    :ivar energy : Convergence details of the electron energy equation
    """

    class Meta:
        name = "numerics_convergence_equations_electrons"
        is_root_ids = False

    particles: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single",
            "field_type": NumericsConvergenceEquationsSingle,
        },
    )
    energy: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single",
            "field_type": NumericsConvergenceEquationsSingle,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsConvergenceEquation(IdsBaseClass):
    """

    :ivar current : Convergence details of the current diffusion equation
    :ivar electrons : Quantities related to the electrons
    :ivar ion : Quantities related to the different ion species
    :ivar energy_ion_total : Convergence details of the ion total (sum over ion species) energy equation
    :ivar time : Time
    """

    class Meta:
        name = "numerics_convergence_equation"
        is_root_ids = False

    current: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single",
            "field_type": NumericsConvergenceEquationsSingle,
        },
    )
    electrons: Optional[NumericsConvergenceEquationsElectrons] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_electrons",
            "field_type": NumericsConvergenceEquationsElectrons,
        },
    )
    ion: Optional[NumericsConvergenceEquationsIon] = field(
        default_factory=lambda: StructArray(
            type=NumericsConvergenceEquationsIon
        ),
        metadata={
            "imas_type": "numerics_convergence_equations_ion",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsConvergenceEquationsIon,
        },
    )
    energy_ion_total: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single",
            "field_type": NumericsConvergenceEquationsSingle,
        },
    )
    time: Optional[float] = field(
        default=9e40, metadata={"imas_type": "flt_type", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsConvergence(IdsBaseClass):
    """

    :ivar time_step : Internal time step used by the transport solver (assuming all transport equations are solved with the same time step)
    :ivar equations : Convergence details of the transport equations, for various time slices
    """

    class Meta:
        name = "numerics_convergence"
        is_root_ids = False

    time_step: Optional[SignalFlt1D] = field(
        default=None,
        metadata={"imas_type": "signal_flt_1d", "field_type": SignalFlt1D},
    )
    equations: Optional[NumericsConvergenceEquation] = field(
        default_factory=lambda: StructArray(type=NumericsConvergenceEquation),
        metadata={
            "imas_type": "numerics_convergence_equation",
            "ndims": 1,
            "coordinates": {"coordinate1": "time"},
            "field_type": NumericsConvergenceEquation,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsSolver1DEquationControlFloat(IdsBaseClass):
    """

    :ivar name : Name of the control parameter
    :ivar value : Value of the control parameter
    """

    class Meta:
        name = "numerics_solver_1d_equation_control_float"
        is_root_ids = False

    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    value: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsSolver1DEquationControlInt(IdsBaseClass):
    """

    :ivar name : Name of the control parameter
    :ivar value : Value of the control parameter
    """

    class Meta:
        name = "numerics_solver_1d_equation_control_int"
        is_root_ids = False

    name: Optional[str] = field(
        default="", metadata={"imas_type": "STR_0D", "field_type": str}
    )
    value: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsSolver1DEquationControlParameters(IdsBaseClass):
    """

    :ivar integer0d : Set of integer type scalar control parameters
    :ivar real0d : Set of real type scalar control parameters
    """

    class Meta:
        name = "numerics_solver_1d_equation_control_parameters"
        is_root_ids = False

    integer0d: Optional[NumericsSolver1DEquationControlInt] = field(
        default_factory=lambda: StructArray(
            type=NumericsSolver1DEquationControlInt
        ),
        metadata={
            "imas_type": "numerics_solver_1d_equation_control_int",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsSolver1DEquationControlInt,
        },
    )
    real0d: Optional[NumericsSolver1DEquationControlFloat] = field(
        default_factory=lambda: StructArray(
            type=NumericsSolver1DEquationControlFloat
        ),
        metadata={
            "imas_type": "numerics_solver_1d_equation_control_float",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsSolver1DEquationControlFloat,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsSolver1DEquationCoefficient(IdsBaseClass):
    """

    :ivar profile : Radial profile of the numerical coefficient
    """

    class Meta:
        name = "numerics_solver_1d_equation_coefficient"
        is_root_ids = False

    profile: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsSolver1DEquationPrimary(IdsBaseClass):
    """

    :ivar identifier : Identifier of the primary quantity of the transport equation. The description node contains the path to the quantity in the physics IDS (example: core_profiles/profiles_1d/ion(1)/density)
    :ivar ion_index : If the primary quantity is related to a ion species, index of the corresponding species in the core_profiles/profiles_1d/ion array
    :ivar neutral_index : If the primary quantity is related to a neutral species, index of the corresponding species in the core_profiles/profiles_1d/neutral array
    :ivar state_index : If the primary quantity is related to a particular state (of an ion or a neutral species), index of the corresponding state in the core_profiles/profiles_1d/ion (or neutral)/state array
    :ivar profile : Profile of the primary quantity
    :ivar d_dr : Radial derivative with respect to the primary coordinate
    :ivar d2_dr2 : Second order radial derivative with respect to the primary coordinate
    :ivar d_dt : Time derivative
    :ivar d_dt_cphi : Derivative with respect to time, at constant toroidal flux (for current diffusion equation)
    :ivar d_dt_cr : Derivative with respect to time, at constant primary coordinate coordinate (for current diffusion equation)
    """

    class Meta:
        name = "numerics_solver_1d_equation_primary"
        is_root_ids = False

    identifier: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    ion_index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    neutral_index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    state_index: Optional[int] = field(
        default=999999999, metadata={"imas_type": "INT_0D", "field_type": int}
    )
    profile: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_dr: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d2_dr2: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_dt_cphi: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_dt_cr: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../../../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsSolver1DEquationBc(IdsBaseClass):
    """

    :ivar type : Boundary condition type
    :ivar value : Value of the boundary condition. For type/index = 1 to 3, only the first position in the vector is used. For type/index = 5, all three positions are used, meaning respectively a1, a2, a3.
    :ivar position : Position, in terms of the primary coordinate, at which the boundary condition is imposed. Outside this position, the value of the data are considered to be prescribed (in case of a single boundary condition).
    """

    class Meta:
        name = "numerics_solver_1d_equation_bc"
        is_root_ids = False

    type: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    value: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...3"},
            "field_type": np.ndarray,
        },
    )
    position: Optional[float] = field(
        default=9e40, metadata={"imas_type": "FLT_0D", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsSolver1DEquation(IdsBaseClass):
    """

    :ivar primary_quantity : Profile and derivatives of the primary quantity of the transport equation
    :ivar computation_mode : Computation mode for this equation
    :ivar boundary_condition : Set of boundary conditions of the transport equation
    :ivar coefficient : Set of numerical coefficients involved in the transport equation
    :ivar convergence : Convergence details
    """

    class Meta:
        name = "numerics_solver_1d_equation"
        is_root_ids = False

    primary_quantity: Optional[NumericsSolver1DEquationPrimary] = field(
        default=None,
        metadata={
            "imas_type": "numerics_solver_1d_equation_primary",
            "field_type": NumericsSolver1DEquationPrimary,
        },
    )
    computation_mode: Optional[IdentifierDynamicAos3] = field(
        default=None,
        metadata={
            "imas_type": "identifier_dynamic_aos3",
            "field_type": IdentifierDynamicAos3,
        },
    )
    boundary_condition: Optional[NumericsSolver1DEquationBc] = field(
        default_factory=lambda: StructArray(type=NumericsSolver1DEquationBc),
        metadata={
            "imas_type": "numerics_solver_1d_equation_bc",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsSolver1DEquationBc,
        },
    )
    coefficient: Optional[NumericsSolver1DEquationCoefficient] = field(
        default_factory=lambda: StructArray(
            type=NumericsSolver1DEquationCoefficient
        ),
        metadata={
            "imas_type": "numerics_solver_1d_equation_coefficient",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsSolver1DEquationCoefficient,
        },
    )
    convergence: Optional[NumericsConvergenceEquationsSingle] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence_equations_single",
            "field_type": NumericsConvergenceEquationsSingle,
        },
    )


@idspy_dataclass(repr=False, slots=True)
class NumericsSolver1D(IdsBaseClass):
    """

    :ivar grid : Radial grid
    :ivar equation : Set of transport equations
    :ivar control_parameters : Solver-specific input or output quantities
    :ivar drho_tor_dt : Partial derivative of the toroidal flux coordinate profile with respect to time
    :ivar d_dvolume_drho_tor_dt : Partial derivative with respect to time of the derivative of the volume with respect to the toroidal flux coordinate
    :ivar time : Time
    """

    class Meta:
        name = "numerics_solver_1d"
        is_root_ids = False

    grid: Optional[CoreRadialGrid] = field(
        default=None,
        metadata={
            "imas_type": "core_radial_grid",
            "field_type": CoreRadialGrid,
        },
    )
    equation: Optional[NumericsSolver1DEquation] = field(
        default_factory=lambda: StructArray(type=NumericsSolver1DEquation),
        metadata={
            "imas_type": "numerics_solver_1d_equation",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": NumericsSolver1DEquation,
        },
    )
    control_parameters: Optional[NumericsSolver1DEquationControlParameters] = (
        field(
            default=None,
            metadata={
                "imas_type": "numerics_solver_1d_equation_control_parameters",
                "field_type": NumericsSolver1DEquationControlParameters,
            },
        )
    )
    drho_tor_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    d_dvolume_drho_tor_dt: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "FLT_1D",
            "ndims": 1,
            "coordinates": {"coordinate1": "../grid/rho_tor_norm"},
            "field_type": np.ndarray,
        },
    )
    time: Optional[float] = field(
        default=9e40, metadata={"imas_type": "flt_type", "field_type": float}
    )


@idspy_dataclass(repr=False, slots=True)
class TransportSolverNumerics(IdsBaseClass):
    """

    :ivar ids_properties :
    :ivar time_step : Internal time step used by the transport solver (assuming all transport equations are solved with the same time step)
    :ivar time_step_average : Average internal time step used by the transport solver between the previous and the current time stored for this quantity (assuming all transport equations are solved with the same time step)
    :ivar time_step_min : Minimum internal time step used by the transport solver between the previous and the current time stored for this quantity (assuming all transport equations are solved with the same time step)
    :ivar solver_1d : Numerics related to 1D radial solver, for various time slices.
    :ivar derivatives_1d : Radial profiles derivatives for various time slices. To be removed when the solver_1d structure is finalized.
    :ivar boundary_conditions_1d : Boundary conditions of the radial transport equations for various time slices. To be removed when the solver_1d structure is finalized.
    :ivar boundary_conditions_ggd : Boundary conditions of the transport equations, provided on the GGD, for various time slices
    :ivar convergence : Convergence details To be removed when the solver_1d structure is finalized.
    :ivar vacuum_toroidal_field : Characteristics of the vacuum toroidal field (used in rho_tor definition and in the normalization of current densities)
    :ivar restart_files : Set of code-specific restart files for a given time slice. These files are managed by a physical application to ensure its restart during long simulations
    :ivar code :
    :ivar time : Generic time
    """

    class Meta:
        name = "transport_solver_numerics"
        is_root_ids = True

    ids_properties: Optional[IdsProperties] = field(
        default=None,
        metadata={"imas_type": "ids_properties", "field_type": IdsProperties},
    )
    time_step: Optional[SignalFlt1D] = field(
        default=None,
        metadata={"imas_type": "signal_flt_1d", "field_type": SignalFlt1D},
    )
    time_step_average: Optional[SignalFlt1D] = field(
        default=None,
        metadata={"imas_type": "signal_flt_1d", "field_type": SignalFlt1D},
    )
    time_step_min: Optional[SignalFlt1D] = field(
        default=None,
        metadata={"imas_type": "signal_flt_1d", "field_type": SignalFlt1D},
    )
    solver_1d: Optional[NumericsSolver1D] = field(
        default_factory=lambda: StructArray(type=NumericsSolver1D),
        metadata={
            "imas_type": "numerics_solver_1d",
            "ndims": 1,
            "coordinates": {"coordinate1": "time"},
            "field_type": NumericsSolver1D,
        },
    )
    derivatives_1d: Optional[NumericsProfiles1DDerivatives] = field(
        default_factory=lambda: StructArray(type=NumericsProfiles1DDerivatives),
        metadata={
            "imas_type": "numerics_profiles_1d_derivatives",
            "ndims": 1,
            "coordinates": {"coordinate1": "time"},
            "field_type": NumericsProfiles1DDerivatives,
        },
    )
    boundary_conditions_1d: Optional[NumericsBc1D] = field(
        default_factory=lambda: StructArray(type=NumericsBc1D),
        metadata={
            "imas_type": "numerics_bc_1d",
            "ndims": 1,
            "coordinates": {"coordinate1": "time"},
            "field_type": NumericsBc1D,
        },
    )
    boundary_conditions_ggd: Optional[NumericsBcGgd] = field(
        default_factory=lambda: StructArray(type=NumericsBcGgd),
        metadata={
            "imas_type": "numerics_bc_ggd",
            "ndims": 1,
            "coordinates": {"coordinate1": "time"},
            "field_type": NumericsBcGgd,
        },
    )
    convergence: Optional[NumericsConvergence] = field(
        default=None,
        metadata={
            "imas_type": "numerics_convergence",
            "field_type": NumericsConvergence,
        },
    )
    vacuum_toroidal_field: Optional[BTorVacuum1] = field(
        default=None,
        metadata={"imas_type": "b_tor_vacuum_1", "field_type": BTorVacuum1},
    )
    restart_files: Optional[NumericsRestart] = field(
        default_factory=lambda: StructArray(type=NumericsRestart),
        metadata={
            "imas_type": "numerics_restart",
            "ndims": 1,
            "coordinates": {"coordinate1": "time"},
            "field_type": NumericsRestart,
        },
    )
    code: Optional[Code] = field(
        default=None, metadata={"imas_type": "code", "field_type": Code}
    )
    time: Optional[np.ndarray] = field(
        default_factory=lambda: np.zeros(shape=(0,) * 1, dtype=float),
        metadata={
            "imas_type": "flt_1d_type",
            "ndims": 1,
            "coordinates": {"coordinate1": "1...N"},
            "field_type": np.ndarray,
        },
    )
