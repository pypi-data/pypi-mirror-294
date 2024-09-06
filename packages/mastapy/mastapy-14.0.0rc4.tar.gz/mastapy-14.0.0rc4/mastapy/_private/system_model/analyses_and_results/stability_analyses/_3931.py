"""KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses import _3895

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3898,
        _3923,
        _3930,
        _3934,
        _3937,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2372

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis._Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis"

    @property
    def conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3895.ConicalGearMeshStabilityAnalysis":
        return self.__parent__._cast(_3895.ConicalGearMeshStabilityAnalysis)

    @property
    def gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3923.GearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3923,
        )

        return self.__parent__._cast(_3923.GearMeshStabilityAnalysis)

    @property
    def inter_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3930.InterMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3930,
        )

        return self.__parent__._cast(
            _3930.InterMountableComponentConnectionStabilityAnalysis
        )

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3898.ConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3898,
        )

        return self.__parent__._cast(_3898.ConnectionStabilityAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3934.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3934,
        )

        return self.__parent__._cast(
            _3934.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3937.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3937,
        )

        return self.__parent__._cast(
            _3937.KlingelnbergCycloPalloidSpiralBevelGearMeshStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis":
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
class KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis(
    _3895.ConicalGearMeshStabilityAnalysis
):
    """KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_STABILITY_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(
        self: "Self",
    ) -> "_2372.KlingelnbergCycloPalloidConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis(self)
