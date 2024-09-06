"""ConnectionStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710

_CONNECTION_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "ConnectionStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7707
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3866,
        _3867,
        _3872,
        _3874,
        _3879,
        _3884,
        _3887,
        _3889,
        _3892,
        _3895,
        _3900,
        _3904,
        _3908,
        _3909,
        _3911,
        _3918,
        _3923,
        _3927,
        _3930,
        _3931,
        _3934,
        _3937,
        _3947,
        _3950,
        _3957,
        _3959,
        _3964,
        _3966,
        _3969,
        _3972,
        _3975,
        _3978,
        _3987,
        _3993,
        _3996,
    )
    from mastapy._private.system_model.connections_and_sockets import _2326

    Self = TypeVar("Self", bound="ConnectionStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionStabilityAnalysis._Cast_ConnectionStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionStabilityAnalysis:
    """Special nested class for casting ConnectionStabilityAnalysis to subclasses."""

    __parent__: "ConnectionStabilityAnalysis"

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7710.ConnectionStaticLoadAnalysisCase":
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
    def abstract_shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3866.AbstractShaftToMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3866,
        )

        return self.__parent__._cast(
            _3866.AbstractShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3867.AGMAGleasonConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3867,
        )

        return self.__parent__._cast(_3867.AGMAGleasonConicalGearMeshStabilityAnalysis)

    @property
    def belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3872.BeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3872,
        )

        return self.__parent__._cast(_3872.BeltConnectionStabilityAnalysis)

    @property
    def bevel_differential_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3874.BevelDifferentialGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3874,
        )

        return self.__parent__._cast(_3874.BevelDifferentialGearMeshStabilityAnalysis)

    @property
    def bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3879.BevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3879,
        )

        return self.__parent__._cast(_3879.BevelGearMeshStabilityAnalysis)

    @property
    def clutch_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3884.ClutchConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3884,
        )

        return self.__parent__._cast(_3884.ClutchConnectionStabilityAnalysis)

    @property
    def coaxial_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3887.CoaxialConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3887,
        )

        return self.__parent__._cast(_3887.CoaxialConnectionStabilityAnalysis)

    @property
    def concept_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3889.ConceptCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3889,
        )

        return self.__parent__._cast(_3889.ConceptCouplingConnectionStabilityAnalysis)

    @property
    def concept_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3892.ConceptGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3892,
        )

        return self.__parent__._cast(_3892.ConceptGearMeshStabilityAnalysis)

    @property
    def conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3895.ConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3895,
        )

        return self.__parent__._cast(_3895.ConicalGearMeshStabilityAnalysis)

    @property
    def coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3900.CouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3900,
        )

        return self.__parent__._cast(_3900.CouplingConnectionStabilityAnalysis)

    @property
    def cvt_belt_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3904.CVTBeltConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3904,
        )

        return self.__parent__._cast(_3904.CVTBeltConnectionStabilityAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3908.CycloidalDiscCentralBearingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3908,
        )

        return self.__parent__._cast(
            _3908.CycloidalDiscCentralBearingConnectionStabilityAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3909.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3909,
        )

        return self.__parent__._cast(
            _3909.CycloidalDiscPlanetaryBearingConnectionStabilityAnalysis
        )

    @property
    def cylindrical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3911.CylindricalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3911,
        )

        return self.__parent__._cast(_3911.CylindricalGearMeshStabilityAnalysis)

    @property
    def face_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3918.FaceGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3918,
        )

        return self.__parent__._cast(_3918.FaceGearMeshStabilityAnalysis)

    @property
    def gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3923.GearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3923,
        )

        return self.__parent__._cast(_3923.GearMeshStabilityAnalysis)

    @property
    def hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3927.HypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3927,
        )

        return self.__parent__._cast(_3927.HypoidGearMeshStabilityAnalysis)

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
    def klingelnberg_cyclo_palloid_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3931.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3931,
        )

        return self.__parent__._cast(
            _3931.KlingelnbergCycloPalloidConicalGearMeshStabilityAnalysis
        )

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
    def part_to_part_shear_coupling_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3947.PartToPartShearCouplingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3947,
        )

        return self.__parent__._cast(
            _3947.PartToPartShearCouplingConnectionStabilityAnalysis
        )

    @property
    def planetary_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3950.PlanetaryConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3950,
        )

        return self.__parent__._cast(_3950.PlanetaryConnectionStabilityAnalysis)

    @property
    def ring_pins_to_disc_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3957.RingPinsToDiscConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3957,
        )

        return self.__parent__._cast(_3957.RingPinsToDiscConnectionStabilityAnalysis)

    @property
    def rolling_ring_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3959.RollingRingConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3959,
        )

        return self.__parent__._cast(_3959.RollingRingConnectionStabilityAnalysis)

    @property
    def shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3964.ShaftToMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3964,
        )

        return self.__parent__._cast(
            _3964.ShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3966.SpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3966,
        )

        return self.__parent__._cast(_3966.SpiralBevelGearMeshStabilityAnalysis)

    @property
    def spring_damper_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3969.SpringDamperConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3969,
        )

        return self.__parent__._cast(_3969.SpringDamperConnectionStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3975.StraightBevelDiffGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3975,
        )

        return self.__parent__._cast(_3975.StraightBevelDiffGearMeshStabilityAnalysis)

    @property
    def straight_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3978.StraightBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3978,
        )

        return self.__parent__._cast(_3978.StraightBevelGearMeshStabilityAnalysis)

    @property
    def torque_converter_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3987.TorqueConverterConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3987,
        )

        return self.__parent__._cast(_3987.TorqueConverterConnectionStabilityAnalysis)

    @property
    def worm_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3993.WormGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3993,
        )

        return self.__parent__._cast(_3993.WormGearMeshStabilityAnalysis)

    @property
    def zerol_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3996.ZerolBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3996,
        )

        return self.__parent__._cast(_3996.ZerolBevelGearMeshStabilityAnalysis)

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "ConnectionStabilityAnalysis":
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
class ConnectionStabilityAnalysis(_7710.ConnectionStaticLoadAnalysisCase):
    """ConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2326.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2326.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stability_analysis(self: "Self") -> "_3972.StabilityAnalysis":
        """mastapy.system_model.analyses_and_results.stability_analyses.StabilityAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StabilityAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionStabilityAnalysis
        """
        return _Cast_ConnectionStabilityAnalysis(self)
