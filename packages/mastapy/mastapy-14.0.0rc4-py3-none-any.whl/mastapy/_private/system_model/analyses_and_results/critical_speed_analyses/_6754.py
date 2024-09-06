"""InterMountableComponentConnectionCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6721,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "InterMountableComponentConnectionCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6691,
        _6695,
        _6698,
        _6703,
        _6707,
        _6712,
        _6716,
        _6719,
        _6723,
        _6729,
        _6737,
        _6743,
        _6748,
        _6752,
        _6756,
        _6759,
        _6762,
        _6771,
        _6781,
        _6783,
        _6791,
        _6793,
        _6797,
        _6800,
        _6808,
        _6815,
        _6818,
    )
    from mastapy._private.system_model.connections_and_sockets import _2335

    Self = TypeVar(
        "Self", bound="InterMountableComponentConnectionCriticalSpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCriticalSpeedAnalysis._Cast_InterMountableComponentConnectionCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCriticalSpeedAnalysis:
    """Special nested class for casting InterMountableComponentConnectionCriticalSpeedAnalysis to subclasses."""

    __parent__: "InterMountableComponentConnectionCriticalSpeedAnalysis"

    @property
    def connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6721.ConnectionCriticalSpeedAnalysis":
        return self.__parent__._cast(_6721.ConnectionCriticalSpeedAnalysis)

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
    def agma_gleason_conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6691.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6691,
        )

        return self.__parent__._cast(
            _6691.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis
        )

    @property
    def belt_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6695.BeltConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6695,
        )

        return self.__parent__._cast(_6695.BeltConnectionCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6698.BevelDifferentialGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6698,
        )

        return self.__parent__._cast(
            _6698.BevelDifferentialGearMeshCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6703.BevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6703,
        )

        return self.__parent__._cast(_6703.BevelGearMeshCriticalSpeedAnalysis)

    @property
    def clutch_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6707.ClutchConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6707,
        )

        return self.__parent__._cast(_6707.ClutchConnectionCriticalSpeedAnalysis)

    @property
    def concept_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6712.ConceptCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6712,
        )

        return self.__parent__._cast(
            _6712.ConceptCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def concept_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6716.ConceptGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6716,
        )

        return self.__parent__._cast(_6716.ConceptGearMeshCriticalSpeedAnalysis)

    @property
    def conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6719.ConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6719,
        )

        return self.__parent__._cast(_6719.ConicalGearMeshCriticalSpeedAnalysis)

    @property
    def coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6723.CouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6723,
        )

        return self.__parent__._cast(_6723.CouplingConnectionCriticalSpeedAnalysis)

    @property
    def cvt_belt_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6729.CVTBeltConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6729,
        )

        return self.__parent__._cast(_6729.CVTBeltConnectionCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6737.CylindricalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6737,
        )

        return self.__parent__._cast(_6737.CylindricalGearMeshCriticalSpeedAnalysis)

    @property
    def face_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6743.FaceGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6743,
        )

        return self.__parent__._cast(_6743.FaceGearMeshCriticalSpeedAnalysis)

    @property
    def gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6748.GearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6748,
        )

        return self.__parent__._cast(_6748.GearMeshCriticalSpeedAnalysis)

    @property
    def hypoid_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6752.HypoidGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6752,
        )

        return self.__parent__._cast(_6752.HypoidGearMeshCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6756.KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6756,
        )

        return self.__parent__._cast(
            _6756.KlingelnbergCycloPalloidConicalGearMeshCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6759.KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6759,
        )

        return self.__parent__._cast(
            _6759.KlingelnbergCycloPalloidHypoidGearMeshCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6762.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6762,
        )

        return self.__parent__._cast(
            _6762.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6771.PartToPartShearCouplingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6771,
        )

        return self.__parent__._cast(
            _6771.PartToPartShearCouplingConnectionCriticalSpeedAnalysis
        )

    @property
    def ring_pins_to_disc_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6781.RingPinsToDiscConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6781,
        )

        return self.__parent__._cast(
            _6781.RingPinsToDiscConnectionCriticalSpeedAnalysis
        )

    @property
    def rolling_ring_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6783.RollingRingConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6783,
        )

        return self.__parent__._cast(_6783.RollingRingConnectionCriticalSpeedAnalysis)

    @property
    def spiral_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6791.SpiralBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6791,
        )

        return self.__parent__._cast(_6791.SpiralBevelGearMeshCriticalSpeedAnalysis)

    @property
    def spring_damper_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6793.SpringDamperConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6793,
        )

        return self.__parent__._cast(_6793.SpringDamperConnectionCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6797.StraightBevelDiffGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6797,
        )

        return self.__parent__._cast(
            _6797.StraightBevelDiffGearMeshCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6800.StraightBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6800,
        )

        return self.__parent__._cast(_6800.StraightBevelGearMeshCriticalSpeedAnalysis)

    @property
    def torque_converter_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6808.TorqueConverterConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6808,
        )

        return self.__parent__._cast(
            _6808.TorqueConverterConnectionCriticalSpeedAnalysis
        )

    @property
    def worm_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6815.WormGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6815,
        )

        return self.__parent__._cast(_6815.WormGearMeshCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_mesh_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6818.ZerolBevelGearMeshCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6818,
        )

        return self.__parent__._cast(_6818.ZerolBevelGearMeshCriticalSpeedAnalysis)

    @property
    def inter_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCriticalSpeedAnalysis":
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
class InterMountableComponentConnectionCriticalSpeedAnalysis(
    _6721.ConnectionCriticalSpeedAnalysis
):
    """InterMountableComponentConnectionCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_CRITICAL_SPEED_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2335.InterMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.InterMountableComponentConnection

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
    ) -> "_Cast_InterMountableComponentConnectionCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCriticalSpeedAnalysis
        """
        return _Cast_InterMountableComponentConnectionCriticalSpeedAnalysis(self)
