"""ConnectionPowerFlow"""

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

_CONNECTION_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "ConnectionPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7707
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4139,
        _4140,
        _4145,
        _4147,
        _4152,
        _4157,
        _4160,
        _4162,
        _4165,
        _4168,
        _4173,
        _4176,
        _4180,
        _4181,
        _4184,
        _4190,
        _4197,
        _4201,
        _4204,
        _4205,
        _4208,
        _4211,
        _4221,
        _4224,
        _4228,
        _4233,
        _4235,
        _4240,
        _4242,
        _4245,
        _4248,
        _4251,
        _4261,
        _4267,
        _4270,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2811,
    )
    from mastapy._private.system_model.connections_and_sockets import _2326

    Self = TypeVar("Self", bound="ConnectionPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectionPowerFlow._Cast_ConnectionPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionPowerFlow:
    """Special nested class for casting ConnectionPowerFlow to subclasses."""

    __parent__: "ConnectionPowerFlow"

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
    def abstract_shaft_to_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4139.AbstractShaftToMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4139

        return self.__parent__._cast(
            _4139.AbstractShaftToMountableComponentConnectionPowerFlow
        )

    @property
    def agma_gleason_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4140.AGMAGleasonConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4140

        return self.__parent__._cast(_4140.AGMAGleasonConicalGearMeshPowerFlow)

    @property
    def belt_connection_power_flow(self: "CastSelf") -> "_4145.BeltConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4145

        return self.__parent__._cast(_4145.BeltConnectionPowerFlow)

    @property
    def bevel_differential_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4147.BevelDifferentialGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4147

        return self.__parent__._cast(_4147.BevelDifferentialGearMeshPowerFlow)

    @property
    def bevel_gear_mesh_power_flow(self: "CastSelf") -> "_4152.BevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4152

        return self.__parent__._cast(_4152.BevelGearMeshPowerFlow)

    @property
    def clutch_connection_power_flow(
        self: "CastSelf",
    ) -> "_4157.ClutchConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4157

        return self.__parent__._cast(_4157.ClutchConnectionPowerFlow)

    @property
    def coaxial_connection_power_flow(
        self: "CastSelf",
    ) -> "_4160.CoaxialConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4160

        return self.__parent__._cast(_4160.CoaxialConnectionPowerFlow)

    @property
    def concept_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4162.ConceptCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4162

        return self.__parent__._cast(_4162.ConceptCouplingConnectionPowerFlow)

    @property
    def concept_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4165.ConceptGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4165

        return self.__parent__._cast(_4165.ConceptGearMeshPowerFlow)

    @property
    def conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4168.ConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4168

        return self.__parent__._cast(_4168.ConicalGearMeshPowerFlow)

    @property
    def coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4173.CouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4173

        return self.__parent__._cast(_4173.CouplingConnectionPowerFlow)

    @property
    def cvt_belt_connection_power_flow(
        self: "CastSelf",
    ) -> "_4176.CVTBeltConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4176

        return self.__parent__._cast(_4176.CVTBeltConnectionPowerFlow)

    @property
    def cycloidal_disc_central_bearing_connection_power_flow(
        self: "CastSelf",
    ) -> "_4180.CycloidalDiscCentralBearingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4180

        return self.__parent__._cast(
            _4180.CycloidalDiscCentralBearingConnectionPowerFlow
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_power_flow(
        self: "CastSelf",
    ) -> "_4181.CycloidalDiscPlanetaryBearingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4181

        return self.__parent__._cast(
            _4181.CycloidalDiscPlanetaryBearingConnectionPowerFlow
        )

    @property
    def cylindrical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4184.CylindricalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4184

        return self.__parent__._cast(_4184.CylindricalGearMeshPowerFlow)

    @property
    def face_gear_mesh_power_flow(self: "CastSelf") -> "_4190.FaceGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4190

        return self.__parent__._cast(_4190.FaceGearMeshPowerFlow)

    @property
    def gear_mesh_power_flow(self: "CastSelf") -> "_4197.GearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4197

        return self.__parent__._cast(_4197.GearMeshPowerFlow)

    @property
    def hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4201.HypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4201

        return self.__parent__._cast(_4201.HypoidGearMeshPowerFlow)

    @property
    def inter_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4204.InterMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4204

        return self.__parent__._cast(_4204.InterMountableComponentConnectionPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4205.KlingelnbergCycloPalloidConicalGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4205

        return self.__parent__._cast(
            _4205.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4208.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4208

        return self.__parent__._cast(
            _4208.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4211.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4211

        return self.__parent__._cast(
            _4211.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        )

    @property
    def part_to_part_shear_coupling_connection_power_flow(
        self: "CastSelf",
    ) -> "_4221.PartToPartShearCouplingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4221

        return self.__parent__._cast(_4221.PartToPartShearCouplingConnectionPowerFlow)

    @property
    def planetary_connection_power_flow(
        self: "CastSelf",
    ) -> "_4224.PlanetaryConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4224

        return self.__parent__._cast(_4224.PlanetaryConnectionPowerFlow)

    @property
    def ring_pins_to_disc_connection_power_flow(
        self: "CastSelf",
    ) -> "_4233.RingPinsToDiscConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4233

        return self.__parent__._cast(_4233.RingPinsToDiscConnectionPowerFlow)

    @property
    def rolling_ring_connection_power_flow(
        self: "CastSelf",
    ) -> "_4235.RollingRingConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4235

        return self.__parent__._cast(_4235.RollingRingConnectionPowerFlow)

    @property
    def shaft_to_mountable_component_connection_power_flow(
        self: "CastSelf",
    ) -> "_4240.ShaftToMountableComponentConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4240

        return self.__parent__._cast(_4240.ShaftToMountableComponentConnectionPowerFlow)

    @property
    def spiral_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4242.SpiralBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4242

        return self.__parent__._cast(_4242.SpiralBevelGearMeshPowerFlow)

    @property
    def spring_damper_connection_power_flow(
        self: "CastSelf",
    ) -> "_4245.SpringDamperConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4245

        return self.__parent__._cast(_4245.SpringDamperConnectionPowerFlow)

    @property
    def straight_bevel_diff_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4248.StraightBevelDiffGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4248

        return self.__parent__._cast(_4248.StraightBevelDiffGearMeshPowerFlow)

    @property
    def straight_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4251.StraightBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4251

        return self.__parent__._cast(_4251.StraightBevelGearMeshPowerFlow)

    @property
    def torque_converter_connection_power_flow(
        self: "CastSelf",
    ) -> "_4261.TorqueConverterConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4261

        return self.__parent__._cast(_4261.TorqueConverterConnectionPowerFlow)

    @property
    def worm_gear_mesh_power_flow(self: "CastSelf") -> "_4267.WormGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4267

        return self.__parent__._cast(_4267.WormGearMeshPowerFlow)

    @property
    def zerol_bevel_gear_mesh_power_flow(
        self: "CastSelf",
    ) -> "_4270.ZerolBevelGearMeshPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4270

        return self.__parent__._cast(_4270.ZerolBevelGearMeshPowerFlow)

    @property
    def connection_power_flow(self: "CastSelf") -> "ConnectionPowerFlow":
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
class ConnectionPowerFlow(_7710.ConnectionStaticLoadAnalysisCase):
    """ConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_loaded(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLoaded")

        if temp is None:
            return False

        return temp

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
    def power_flow(self: "Self") -> "_4228.PowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.PowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlow")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def torsional_system_deflection_analysis(
        self: "Self",
    ) -> "_2811.ConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorsionalSystemDeflectionAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ConnectionPowerFlow
        """
        return _Cast_ConnectionPowerFlow(self)
