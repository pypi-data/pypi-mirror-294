"""PartPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717

_PART_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "PartPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4136,
        _4137,
        _4138,
        _4141,
        _4142,
        _4143,
        _4144,
        _4146,
        _4148,
        _4149,
        _4150,
        _4151,
        _4153,
        _4154,
        _4155,
        _4156,
        _4158,
        _4159,
        _4161,
        _4163,
        _4164,
        _4166,
        _4167,
        _4169,
        _4170,
        _4172,
        _4174,
        _4175,
        _4177,
        _4178,
        _4179,
        _4182,
        _4185,
        _4186,
        _4187,
        _4188,
        _4189,
        _4191,
        _4192,
        _4195,
        _4196,
        _4198,
        _4199,
        _4200,
        _4202,
        _4203,
        _4206,
        _4207,
        _4209,
        _4210,
        _4212,
        _4213,
        _4214,
        _4215,
        _4216,
        _4217,
        _4218,
        _4219,
        _4222,
        _4223,
        _4225,
        _4226,
        _4227,
        _4228,
        _4230,
        _4231,
        _4232,
        _4234,
        _4236,
        _4237,
        _4238,
        _4239,
        _4241,
        _4243,
        _4244,
        _4246,
        _4247,
        _4249,
        _4250,
        _4252,
        _4253,
        _4254,
        _4255,
        _4256,
        _4257,
        _4258,
        _4259,
        _4262,
        _4263,
        _4264,
        _4265,
        _4266,
        _4268,
        _4269,
        _4271,
        _4272,
    )
    from mastapy._private.system_model.drawing import _2308
    from mastapy._private.system_model.part_model import _2525

    Self = TypeVar("Self", bound="PartPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="PartPowerFlow._Cast_PartPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("PartPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartPowerFlow:
    """Special nested class for casting PartPowerFlow to subclasses."""

    __parent__: "PartPowerFlow"

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
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
    def abstract_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4136.AbstractAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4136

        return self.__parent__._cast(_4136.AbstractAssemblyPowerFlow)

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
    def agma_gleason_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4142.AGMAGleasonConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4142

        return self.__parent__._cast(_4142.AGMAGleasonConicalGearSetPowerFlow)

    @property
    def assembly_power_flow(self: "CastSelf") -> "_4143.AssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4143

        return self.__parent__._cast(_4143.AssemblyPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4144.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4144

        return self.__parent__._cast(_4144.BearingPowerFlow)

    @property
    def belt_drive_power_flow(self: "CastSelf") -> "_4146.BeltDrivePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4146

        return self.__parent__._cast(_4146.BeltDrivePowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4148.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4148

        return self.__parent__._cast(_4148.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4149.BevelDifferentialGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4149

        return self.__parent__._cast(_4149.BevelDifferentialGearSetPowerFlow)

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
    def bevel_gear_set_power_flow(self: "CastSelf") -> "_4154.BevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4154

        return self.__parent__._cast(_4154.BevelGearSetPowerFlow)

    @property
    def bolted_joint_power_flow(self: "CastSelf") -> "_4155.BoltedJointPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4155

        return self.__parent__._cast(_4155.BoltedJointPowerFlow)

    @property
    def bolt_power_flow(self: "CastSelf") -> "_4156.BoltPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4156

        return self.__parent__._cast(_4156.BoltPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4158.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4158

        return self.__parent__._cast(_4158.ClutchHalfPowerFlow)

    @property
    def clutch_power_flow(self: "CastSelf") -> "_4159.ClutchPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4159

        return self.__parent__._cast(_4159.ClutchPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4161.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4161

        return self.__parent__._cast(_4161.ComponentPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4163.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4163

        return self.__parent__._cast(_4163.ConceptCouplingHalfPowerFlow)

    @property
    def concept_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4164.ConceptCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4164

        return self.__parent__._cast(_4164.ConceptCouplingPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4166.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4166

        return self.__parent__._cast(_4166.ConceptGearPowerFlow)

    @property
    def concept_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4167.ConceptGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4167

        return self.__parent__._cast(_4167.ConceptGearSetPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4169.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4169

        return self.__parent__._cast(_4169.ConicalGearPowerFlow)

    @property
    def conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4170.ConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4170

        return self.__parent__._cast(_4170.ConicalGearSetPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4172.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4172

        return self.__parent__._cast(_4172.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4174.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4174

        return self.__parent__._cast(_4174.CouplingHalfPowerFlow)

    @property
    def coupling_power_flow(self: "CastSelf") -> "_4175.CouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4175

        return self.__parent__._cast(_4175.CouplingPowerFlow)

    @property
    def cvt_power_flow(self: "CastSelf") -> "_4177.CVTPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4177

        return self.__parent__._cast(_4177.CVTPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4178.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4178

        return self.__parent__._cast(_4178.CVTPulleyPowerFlow)

    @property
    def cycloidal_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4179.CycloidalAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4179

        return self.__parent__._cast(_4179.CycloidalAssemblyPowerFlow)

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
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4186.CylindricalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4186

        return self.__parent__._cast(_4186.CylindricalGearSetPowerFlow)

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
    def face_gear_set_power_flow(self: "CastSelf") -> "_4192.FaceGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4192

        return self.__parent__._cast(_4192.FaceGearSetPowerFlow)

    @property
    def fe_part_power_flow(self: "CastSelf") -> "_4195.FEPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4195

        return self.__parent__._cast(_4195.FEPartPowerFlow)

    @property
    def flexible_pin_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4196.FlexiblePinAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4196

        return self.__parent__._cast(_4196.FlexiblePinAssemblyPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4198.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4198

        return self.__parent__._cast(_4198.GearPowerFlow)

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4199.GearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4199

        return self.__parent__._cast(_4199.GearSetPowerFlow)

    @property
    def guide_dxf_model_power_flow(self: "CastSelf") -> "_4200.GuideDxfModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4200

        return self.__parent__._cast(_4200.GuideDxfModelPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4202.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4202

        return self.__parent__._cast(_4202.HypoidGearPowerFlow)

    @property
    def hypoid_gear_set_power_flow(self: "CastSelf") -> "_4203.HypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4203

        return self.__parent__._cast(_4203.HypoidGearSetPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4206.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4206

        return self.__parent__._cast(_4206.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4207.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4207

        return self.__parent__._cast(
            _4207.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4209

        return self.__parent__._cast(_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4210.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4210

        return self.__parent__._cast(
            _4210.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4212.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4212

        return self.__parent__._cast(
            _4212.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4213.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4213

        return self.__parent__._cast(
            _4213.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
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
    def microphone_array_power_flow(
        self: "CastSelf",
    ) -> "_4216.MicrophoneArrayPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4216

        return self.__parent__._cast(_4216.MicrophoneArrayPowerFlow)

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
    def part_to_part_shear_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4223.PartToPartShearCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4223

        return self.__parent__._cast(_4223.PartToPartShearCouplingPowerFlow)

    @property
    def planetary_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4225.PlanetaryGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4225

        return self.__parent__._cast(_4225.PlanetaryGearSetPowerFlow)

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
    def rolling_ring_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4234.RollingRingAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4234

        return self.__parent__._cast(_4234.RollingRingAssemblyPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4236.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4236

        return self.__parent__._cast(_4236.RollingRingPowerFlow)

    @property
    def root_assembly_power_flow(self: "CastSelf") -> "_4237.RootAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4237

        return self.__parent__._cast(_4237.RootAssemblyPowerFlow)

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
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4241.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4241

        return self.__parent__._cast(_4241.SpecialisedAssemblyPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4243.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4243

        return self.__parent__._cast(_4243.SpiralBevelGearPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4244.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4244

        return self.__parent__._cast(_4244.SpiralBevelGearSetPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4246.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4246

        return self.__parent__._cast(_4246.SpringDamperHalfPowerFlow)

    @property
    def spring_damper_power_flow(self: "CastSelf") -> "_4247.SpringDamperPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4247

        return self.__parent__._cast(_4247.SpringDamperPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4249.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4249

        return self.__parent__._cast(_4249.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_diff_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4250.StraightBevelDiffGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4250

        return self.__parent__._cast(_4250.StraightBevelDiffGearSetPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4252.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4252

        return self.__parent__._cast(_4252.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4253.StraightBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4253

        return self.__parent__._cast(_4253.StraightBevelGearSetPowerFlow)

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
    def synchroniser_power_flow(self: "CastSelf") -> "_4258.SynchroniserPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4258

        return self.__parent__._cast(_4258.SynchroniserPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4259.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4259

        return self.__parent__._cast(_4259.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_power_flow(
        self: "CastSelf",
    ) -> "_4262.TorqueConverterPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4262

        return self.__parent__._cast(_4262.TorqueConverterPowerFlow)

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
    def worm_gear_set_power_flow(self: "CastSelf") -> "_4269.WormGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4269

        return self.__parent__._cast(_4269.WormGearSetPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4271.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4271

        return self.__parent__._cast(_4271.ZerolBevelGearPowerFlow)

    @property
    def zerol_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4272.ZerolBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4272

        return self.__parent__._cast(_4272.ZerolBevelGearSetPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "PartPowerFlow":
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
class PartPowerFlow(_7717.PartStaticLoadAnalysisCase):
    """PartPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def two_d_drawing_showing_power_flow(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingShowingPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def component_design(self: "Self") -> "_2525.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

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

    def create_viewable(self: "Self") -> "_2308.PowerFlowViewable":
        """mastapy.system_model.drawing.PowerFlowViewable"""
        method_result = pythonnet_method_call(self.wrapped, "CreateViewable")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_PartPowerFlow
        """
        return _Cast_PartPowerFlow(self)
