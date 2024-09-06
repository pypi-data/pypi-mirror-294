"""ComponentPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4220

_COMPONENT_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "ComponentPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4137,
        _4138,
        _4141,
        _4144,
        _4148,
        _4150,
        _4151,
        _4153,
        _4156,
        _4158,
        _4163,
        _4166,
        _4169,
        _4172,
        _4174,
        _4178,
        _4182,
        _4185,
        _4187,
        _4188,
        _4189,
        _4191,
        _4195,
        _4198,
        _4200,
        _4202,
        _4206,
        _4209,
        _4212,
        _4214,
        _4215,
        _4217,
        _4218,
        _4219,
        _4222,
        _4226,
        _4227,
        _4230,
        _4231,
        _4232,
        _4236,
        _4238,
        _4239,
        _4243,
        _4246,
        _4249,
        _4252,
        _4254,
        _4255,
        _4256,
        _4257,
        _4259,
        _4263,
        _4264,
        _4265,
        _4266,
        _4268,
        _4271,
    )
    from mastapy._private.system_model.part_model import _2499

    Self = TypeVar("Self", bound="ComponentPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="ComponentPowerFlow._Cast_ComponentPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("ComponentPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentPowerFlow:
    """Special nested class for casting ComponentPowerFlow to subclasses."""

    __parent__: "ComponentPowerFlow"

    @property
    def part_power_flow(self: "CastSelf") -> "_4220.PartPowerFlow":
        return self.__parent__._cast(_4220.PartPowerFlow)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7714.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2741.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2741

        return self.__parent__._cast(_2741.PartAnalysis)

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
    def abstract_shaft_or_housing_power_flow(
        self: "CastSelf",
    ) -> "_4137.AbstractShaftOrHousingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4137

        return self.__parent__._cast(_4137.AbstractShaftOrHousingPowerFlow)

    @property
    def abstract_shaft_power_flow(self: "CastSelf") -> "_4138.AbstractShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4138

        return self.__parent__._cast(_4138.AbstractShaftPowerFlow)

    @property
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4141.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4141

        return self.__parent__._cast(_4141.AGMAGleasonConicalGearPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4144.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4144

        return self.__parent__._cast(_4144.BearingPowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4148.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4148

        return self.__parent__._cast(_4148.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4150.BevelDifferentialPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4150

        return self.__parent__._cast(_4150.BevelDifferentialPlanetGearPowerFlow)

    @property
    def bevel_differential_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4151.BevelDifferentialSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4151

        return self.__parent__._cast(_4151.BevelDifferentialSunGearPowerFlow)

    @property
    def bevel_gear_power_flow(self: "CastSelf") -> "_4153.BevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4153

        return self.__parent__._cast(_4153.BevelGearPowerFlow)

    @property
    def bolt_power_flow(self: "CastSelf") -> "_4156.BoltPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4156

        return self.__parent__._cast(_4156.BoltPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4158.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4158

        return self.__parent__._cast(_4158.ClutchHalfPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4163.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4163

        return self.__parent__._cast(_4163.ConceptCouplingHalfPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4166.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4166

        return self.__parent__._cast(_4166.ConceptGearPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4169.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4169

        return self.__parent__._cast(_4169.ConicalGearPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4172.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4172

        return self.__parent__._cast(_4172.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4174.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4174

        return self.__parent__._cast(_4174.CouplingHalfPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4178.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4178

        return self.__parent__._cast(_4178.CVTPulleyPowerFlow)

    @property
    def cycloidal_disc_power_flow(self: "CastSelf") -> "_4182.CycloidalDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4182

        return self.__parent__._cast(_4182.CycloidalDiscPowerFlow)

    @property
    def cylindrical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4185.CylindricalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4185

        return self.__parent__._cast(_4185.CylindricalGearPowerFlow)

    @property
    def cylindrical_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4187.CylindricalPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4187

        return self.__parent__._cast(_4187.CylindricalPlanetGearPowerFlow)

    @property
    def datum_power_flow(self: "CastSelf") -> "_4188.DatumPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4188

        return self.__parent__._cast(_4188.DatumPowerFlow)

    @property
    def external_cad_model_power_flow(
        self: "CastSelf",
    ) -> "_4189.ExternalCADModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4189

        return self.__parent__._cast(_4189.ExternalCADModelPowerFlow)

    @property
    def face_gear_power_flow(self: "CastSelf") -> "_4191.FaceGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4191

        return self.__parent__._cast(_4191.FaceGearPowerFlow)

    @property
    def fe_part_power_flow(self: "CastSelf") -> "_4195.FEPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4195

        return self.__parent__._cast(_4195.FEPartPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4198.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4198

        return self.__parent__._cast(_4198.GearPowerFlow)

    @property
    def guide_dxf_model_power_flow(self: "CastSelf") -> "_4200.GuideDxfModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4200

        return self.__parent__._cast(_4200.GuideDxfModelPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4202.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4202

        return self.__parent__._cast(_4202.HypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4206.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4206

        return self.__parent__._cast(_4206.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4209

        return self.__parent__._cast(_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4212.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4212

        return self.__parent__._cast(
            _4212.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def mass_disc_power_flow(self: "CastSelf") -> "_4214.MassDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4214

        return self.__parent__._cast(_4214.MassDiscPowerFlow)

    @property
    def measurement_component_power_flow(
        self: "CastSelf",
    ) -> "_4215.MeasurementComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4215

        return self.__parent__._cast(_4215.MeasurementComponentPowerFlow)

    @property
    def microphone_power_flow(self: "CastSelf") -> "_4217.MicrophonePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4217

        return self.__parent__._cast(_4217.MicrophonePowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4218.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4218

        return self.__parent__._cast(_4218.MountableComponentPowerFlow)

    @property
    def oil_seal_power_flow(self: "CastSelf") -> "_4219.OilSealPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4219

        return self.__parent__._cast(_4219.OilSealPowerFlow)

    @property
    def part_to_part_shear_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4222.PartToPartShearCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4222

        return self.__parent__._cast(_4222.PartToPartShearCouplingHalfPowerFlow)

    @property
    def planet_carrier_power_flow(self: "CastSelf") -> "_4226.PlanetCarrierPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4226

        return self.__parent__._cast(_4226.PlanetCarrierPowerFlow)

    @property
    def point_load_power_flow(self: "CastSelf") -> "_4227.PointLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4227

        return self.__parent__._cast(_4227.PointLoadPowerFlow)

    @property
    def power_load_power_flow(self: "CastSelf") -> "_4230.PowerLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4230

        return self.__parent__._cast(_4230.PowerLoadPowerFlow)

    @property
    def pulley_power_flow(self: "CastSelf") -> "_4231.PulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4231

        return self.__parent__._cast(_4231.PulleyPowerFlow)

    @property
    def ring_pins_power_flow(self: "CastSelf") -> "_4232.RingPinsPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4232

        return self.__parent__._cast(_4232.RingPinsPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4236.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4236

        return self.__parent__._cast(_4236.RollingRingPowerFlow)

    @property
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "_4238.ShaftHubConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4238

        return self.__parent__._cast(_4238.ShaftHubConnectionPowerFlow)

    @property
    def shaft_power_flow(self: "CastSelf") -> "_4239.ShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4239

        return self.__parent__._cast(_4239.ShaftPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4243.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4243

        return self.__parent__._cast(_4243.SpiralBevelGearPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4246.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4246

        return self.__parent__._cast(_4246.SpringDamperHalfPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4249.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4249

        return self.__parent__._cast(_4249.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4252.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4252

        return self.__parent__._cast(_4252.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4254.StraightBevelPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4254

        return self.__parent__._cast(_4254.StraightBevelPlanetGearPowerFlow)

    @property
    def straight_bevel_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4255.StraightBevelSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4255

        return self.__parent__._cast(_4255.StraightBevelSunGearPowerFlow)

    @property
    def synchroniser_half_power_flow(
        self: "CastSelf",
    ) -> "_4256.SynchroniserHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4256

        return self.__parent__._cast(_4256.SynchroniserHalfPowerFlow)

    @property
    def synchroniser_part_power_flow(
        self: "CastSelf",
    ) -> "_4257.SynchroniserPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4257

        return self.__parent__._cast(_4257.SynchroniserPartPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4259.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4259

        return self.__parent__._cast(_4259.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_pump_power_flow(
        self: "CastSelf",
    ) -> "_4263.TorqueConverterPumpPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4263

        return self.__parent__._cast(_4263.TorqueConverterPumpPowerFlow)

    @property
    def torque_converter_turbine_power_flow(
        self: "CastSelf",
    ) -> "_4264.TorqueConverterTurbinePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4264

        return self.__parent__._cast(_4264.TorqueConverterTurbinePowerFlow)

    @property
    def unbalanced_mass_power_flow(self: "CastSelf") -> "_4265.UnbalancedMassPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4265

        return self.__parent__._cast(_4265.UnbalancedMassPowerFlow)

    @property
    def virtual_component_power_flow(
        self: "CastSelf",
    ) -> "_4266.VirtualComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4266

        return self.__parent__._cast(_4266.VirtualComponentPowerFlow)

    @property
    def worm_gear_power_flow(self: "CastSelf") -> "_4268.WormGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4268

        return self.__parent__._cast(_4268.WormGearPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4271.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4271

        return self.__parent__._cast(_4271.ZerolBevelGearPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "ComponentPowerFlow":
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
class ComponentPowerFlow(_4220.PartPowerFlow):
    """ComponentPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self: "Self") -> "_2499.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ComponentPowerFlow
        """
        return _Cast_ComponentPowerFlow(self)
