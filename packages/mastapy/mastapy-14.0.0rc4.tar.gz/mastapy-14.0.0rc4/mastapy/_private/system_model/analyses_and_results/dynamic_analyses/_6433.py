"""BevelGearMeshDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6421

_BEVEL_GEAR_MESH_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "BevelGearMeshDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7709,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6428,
        _6449,
        _6451,
        _6477,
        _6483,
        _6520,
        _6526,
        _6529,
        _6547,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2357

    Self = TypeVar("Self", bound="BevelGearMeshDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearMeshDynamicAnalysis._Cast_BevelGearMeshDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshDynamicAnalysis:
    """Special nested class for casting BevelGearMeshDynamicAnalysis to subclasses."""

    __parent__: "BevelGearMeshDynamicAnalysis"

    @property
    def agma_gleason_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6421.AGMAGleasonConicalGearMeshDynamicAnalysis":
        return self.__parent__._cast(_6421.AGMAGleasonConicalGearMeshDynamicAnalysis)

    @property
    def conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6449.ConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6449,
        )

        return self.__parent__._cast(_6449.ConicalGearMeshDynamicAnalysis)

    @property
    def gear_mesh_dynamic_analysis(self: "CastSelf") -> "_6477.GearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6477,
        )

        return self.__parent__._cast(_6477.GearMeshDynamicAnalysis)

    @property
    def inter_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6483.InterMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6483,
        )

        return self.__parent__._cast(
            _6483.InterMountableComponentConnectionDynamicAnalysis
        )

    @property
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6451.ConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6451,
        )

        return self.__parent__._cast(_6451.ConnectionDynamicAnalysis)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7709.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.ConnectionFEAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7710.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7707.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7707,
        )

        return self.__parent__._cast(_7707.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2733.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2733

        return self.__parent__._cast(_2733.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2737.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2737

        return self.__parent__._cast(_2737.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2735.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.DesignEntityAnalysis)

    @property
    def bevel_differential_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6428.BevelDifferentialGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6428,
        )

        return self.__parent__._cast(_6428.BevelDifferentialGearMeshDynamicAnalysis)

    @property
    def spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6520.SpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6520,
        )

        return self.__parent__._cast(_6520.SpiralBevelGearMeshDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6526.StraightBevelDiffGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6526,
        )

        return self.__parent__._cast(_6526.StraightBevelDiffGearMeshDynamicAnalysis)

    @property
    def straight_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6529.StraightBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6529,
        )

        return self.__parent__._cast(_6529.StraightBevelGearMeshDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6547.ZerolBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6547,
        )

        return self.__parent__._cast(_6547.ZerolBevelGearMeshDynamicAnalysis)

    @property
    def bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "BevelGearMeshDynamicAnalysis":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class BevelGearMeshDynamicAnalysis(_6421.AGMAGleasonConicalGearMeshDynamicAnalysis):
    """BevelGearMeshDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2357.BevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.BevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearMeshDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshDynamicAnalysis
        """
        return _Cast_BevelGearMeshDynamicAnalysis(self)
