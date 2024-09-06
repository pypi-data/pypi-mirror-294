"""PartCompoundPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7715

_PART_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "PartCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7712
    from mastapy._private.system_model.analyses_and_results.power_flows import _4220
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4273,
        _4274,
        _4275,
        _4277,
        _4279,
        _4280,
        _4281,
        _4283,
        _4284,
        _4286,
        _4287,
        _4288,
        _4289,
        _4291,
        _4292,
        _4293,
        _4294,
        _4296,
        _4298,
        _4299,
        _4301,
        _4302,
        _4304,
        _4305,
        _4307,
        _4309,
        _4310,
        _4312,
        _4314,
        _4315,
        _4316,
        _4318,
        _4320,
        _4322,
        _4323,
        _4324,
        _4325,
        _4326,
        _4328,
        _4329,
        _4330,
        _4331,
        _4333,
        _4334,
        _4335,
        _4337,
        _4339,
        _4341,
        _4342,
        _4344,
        _4345,
        _4347,
        _4348,
        _4349,
        _4350,
        _4351,
        _4352,
        _4353,
        _4355,
        _4357,
        _4359,
        _4360,
        _4361,
        _4362,
        _4363,
        _4364,
        _4366,
        _4367,
        _4369,
        _4370,
        _4371,
        _4373,
        _4374,
        _4376,
        _4377,
        _4379,
        _4380,
        _4382,
        _4383,
        _4385,
        _4386,
        _4387,
        _4388,
        _4389,
        _4390,
        _4391,
        _4392,
        _4394,
        _4395,
        _4396,
        _4397,
        _4398,
        _4400,
        _4401,
        _4403,
    )

    Self = TypeVar("Self", bound="PartCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="PartCompoundPowerFlow._Cast_PartCompoundPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundPowerFlow:
    """Special nested class for casting PartCompoundPowerFlow to subclasses."""

    __parent__: "PartCompoundPowerFlow"

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7715.PartCompoundAnalysis":
        return self.__parent__._cast(_7715.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7712.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2735.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.DesignEntityAnalysis)

    @property
    def abstract_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4273.AbstractAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4273,
        )

        return self.__parent__._cast(_4273.AbstractAssemblyCompoundPowerFlow)

    @property
    def abstract_shaft_compound_power_flow(
        self: "CastSelf",
    ) -> "_4274.AbstractShaftCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4274,
        )

        return self.__parent__._cast(_4274.AbstractShaftCompoundPowerFlow)

    @property
    def abstract_shaft_or_housing_compound_power_flow(
        self: "CastSelf",
    ) -> "_4275.AbstractShaftOrHousingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4275,
        )

        return self.__parent__._cast(_4275.AbstractShaftOrHousingCompoundPowerFlow)

    @property
    def agma_gleason_conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4277.AGMAGleasonConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4277,
        )

        return self.__parent__._cast(_4277.AGMAGleasonConicalGearCompoundPowerFlow)

    @property
    def agma_gleason_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4279.AGMAGleasonConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4279,
        )

        return self.__parent__._cast(_4279.AGMAGleasonConicalGearSetCompoundPowerFlow)

    @property
    def assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4280.AssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4280,
        )

        return self.__parent__._cast(_4280.AssemblyCompoundPowerFlow)

    @property
    def bearing_compound_power_flow(
        self: "CastSelf",
    ) -> "_4281.BearingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4281,
        )

        return self.__parent__._cast(_4281.BearingCompoundPowerFlow)

    @property
    def belt_drive_compound_power_flow(
        self: "CastSelf",
    ) -> "_4283.BeltDriveCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4283,
        )

        return self.__parent__._cast(_4283.BeltDriveCompoundPowerFlow)

    @property
    def bevel_differential_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4284.BevelDifferentialGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4284,
        )

        return self.__parent__._cast(_4284.BevelDifferentialGearCompoundPowerFlow)

    @property
    def bevel_differential_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4286.BevelDifferentialGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4286,
        )

        return self.__parent__._cast(_4286.BevelDifferentialGearSetCompoundPowerFlow)

    @property
    def bevel_differential_planet_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4287.BevelDifferentialPlanetGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4287,
        )

        return self.__parent__._cast(_4287.BevelDifferentialPlanetGearCompoundPowerFlow)

    @property
    def bevel_differential_sun_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4288.BevelDifferentialSunGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4288,
        )

        return self.__parent__._cast(_4288.BevelDifferentialSunGearCompoundPowerFlow)

    @property
    def bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4289.BevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4289,
        )

        return self.__parent__._cast(_4289.BevelGearCompoundPowerFlow)

    @property
    def bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4291.BevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4291,
        )

        return self.__parent__._cast(_4291.BevelGearSetCompoundPowerFlow)

    @property
    def bolt_compound_power_flow(self: "CastSelf") -> "_4292.BoltCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4292,
        )

        return self.__parent__._cast(_4292.BoltCompoundPowerFlow)

    @property
    def bolted_joint_compound_power_flow(
        self: "CastSelf",
    ) -> "_4293.BoltedJointCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4293,
        )

        return self.__parent__._cast(_4293.BoltedJointCompoundPowerFlow)

    @property
    def clutch_compound_power_flow(self: "CastSelf") -> "_4294.ClutchCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4294,
        )

        return self.__parent__._cast(_4294.ClutchCompoundPowerFlow)

    @property
    def clutch_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4296.ClutchHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4296,
        )

        return self.__parent__._cast(_4296.ClutchHalfCompoundPowerFlow)

    @property
    def component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4298.ComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4298,
        )

        return self.__parent__._cast(_4298.ComponentCompoundPowerFlow)

    @property
    def concept_coupling_compound_power_flow(
        self: "CastSelf",
    ) -> "_4299.ConceptCouplingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4299,
        )

        return self.__parent__._cast(_4299.ConceptCouplingCompoundPowerFlow)

    @property
    def concept_coupling_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4301.ConceptCouplingHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4301,
        )

        return self.__parent__._cast(_4301.ConceptCouplingHalfCompoundPowerFlow)

    @property
    def concept_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4302.ConceptGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4302,
        )

        return self.__parent__._cast(_4302.ConceptGearCompoundPowerFlow)

    @property
    def concept_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4304.ConceptGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4304,
        )

        return self.__parent__._cast(_4304.ConceptGearSetCompoundPowerFlow)

    @property
    def conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4305.ConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4305,
        )

        return self.__parent__._cast(_4305.ConicalGearCompoundPowerFlow)

    @property
    def conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4307.ConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4307,
        )

        return self.__parent__._cast(_4307.ConicalGearSetCompoundPowerFlow)

    @property
    def connector_compound_power_flow(
        self: "CastSelf",
    ) -> "_4309.ConnectorCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4309,
        )

        return self.__parent__._cast(_4309.ConnectorCompoundPowerFlow)

    @property
    def coupling_compound_power_flow(
        self: "CastSelf",
    ) -> "_4310.CouplingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4310,
        )

        return self.__parent__._cast(_4310.CouplingCompoundPowerFlow)

    @property
    def coupling_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4312.CouplingHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4312,
        )

        return self.__parent__._cast(_4312.CouplingHalfCompoundPowerFlow)

    @property
    def cvt_compound_power_flow(self: "CastSelf") -> "_4314.CVTCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4314,
        )

        return self.__parent__._cast(_4314.CVTCompoundPowerFlow)

    @property
    def cvt_pulley_compound_power_flow(
        self: "CastSelf",
    ) -> "_4315.CVTPulleyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4315,
        )

        return self.__parent__._cast(_4315.CVTPulleyCompoundPowerFlow)

    @property
    def cycloidal_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4316.CycloidalAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4316,
        )

        return self.__parent__._cast(_4316.CycloidalAssemblyCompoundPowerFlow)

    @property
    def cycloidal_disc_compound_power_flow(
        self: "CastSelf",
    ) -> "_4318.CycloidalDiscCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4318,
        )

        return self.__parent__._cast(_4318.CycloidalDiscCompoundPowerFlow)

    @property
    def cylindrical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4320.CylindricalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4320,
        )

        return self.__parent__._cast(_4320.CylindricalGearCompoundPowerFlow)

    @property
    def cylindrical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4322.CylindricalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4322,
        )

        return self.__parent__._cast(_4322.CylindricalGearSetCompoundPowerFlow)

    @property
    def cylindrical_planet_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4323.CylindricalPlanetGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4323,
        )

        return self.__parent__._cast(_4323.CylindricalPlanetGearCompoundPowerFlow)

    @property
    def datum_compound_power_flow(self: "CastSelf") -> "_4324.DatumCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4324,
        )

        return self.__parent__._cast(_4324.DatumCompoundPowerFlow)

    @property
    def external_cad_model_compound_power_flow(
        self: "CastSelf",
    ) -> "_4325.ExternalCADModelCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4325,
        )

        return self.__parent__._cast(_4325.ExternalCADModelCompoundPowerFlow)

    @property
    def face_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4326.FaceGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4326,
        )

        return self.__parent__._cast(_4326.FaceGearCompoundPowerFlow)

    @property
    def face_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4328.FaceGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4328,
        )

        return self.__parent__._cast(_4328.FaceGearSetCompoundPowerFlow)

    @property
    def fe_part_compound_power_flow(
        self: "CastSelf",
    ) -> "_4329.FEPartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4329,
        )

        return self.__parent__._cast(_4329.FEPartCompoundPowerFlow)

    @property
    def flexible_pin_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4330.FlexiblePinAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4330,
        )

        return self.__parent__._cast(_4330.FlexiblePinAssemblyCompoundPowerFlow)

    @property
    def gear_compound_power_flow(self: "CastSelf") -> "_4331.GearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4331,
        )

        return self.__parent__._cast(_4331.GearCompoundPowerFlow)

    @property
    def gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4333.GearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4333,
        )

        return self.__parent__._cast(_4333.GearSetCompoundPowerFlow)

    @property
    def guide_dxf_model_compound_power_flow(
        self: "CastSelf",
    ) -> "_4334.GuideDxfModelCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4334,
        )

        return self.__parent__._cast(_4334.GuideDxfModelCompoundPowerFlow)

    @property
    def hypoid_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4335.HypoidGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4335,
        )

        return self.__parent__._cast(_4335.HypoidGearCompoundPowerFlow)

    @property
    def hypoid_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4337.HypoidGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4337,
        )

        return self.__parent__._cast(_4337.HypoidGearSetCompoundPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4339.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4339,
        )

        return self.__parent__._cast(
            _4339.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4341.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4341,
        )

        return self.__parent__._cast(
            _4341.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4342.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4342,
        )

        return self.__parent__._cast(
            _4342.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4344.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4344,
        )

        return self.__parent__._cast(
            _4344.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4345.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4345,
        )

        return self.__parent__._cast(
            _4345.KlingelnbergCycloPalloidSpiralBevelGearCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4347.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4347,
        )

        return self.__parent__._cast(
            _4347.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow
        )

    @property
    def mass_disc_compound_power_flow(
        self: "CastSelf",
    ) -> "_4348.MassDiscCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4348,
        )

        return self.__parent__._cast(_4348.MassDiscCompoundPowerFlow)

    @property
    def measurement_component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4349.MeasurementComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4349,
        )

        return self.__parent__._cast(_4349.MeasurementComponentCompoundPowerFlow)

    @property
    def microphone_array_compound_power_flow(
        self: "CastSelf",
    ) -> "_4350.MicrophoneArrayCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4350,
        )

        return self.__parent__._cast(_4350.MicrophoneArrayCompoundPowerFlow)

    @property
    def microphone_compound_power_flow(
        self: "CastSelf",
    ) -> "_4351.MicrophoneCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4351,
        )

        return self.__parent__._cast(_4351.MicrophoneCompoundPowerFlow)

    @property
    def mountable_component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4352.MountableComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4352,
        )

        return self.__parent__._cast(_4352.MountableComponentCompoundPowerFlow)

    @property
    def oil_seal_compound_power_flow(
        self: "CastSelf",
    ) -> "_4353.OilSealCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4353,
        )

        return self.__parent__._cast(_4353.OilSealCompoundPowerFlow)

    @property
    def part_to_part_shear_coupling_compound_power_flow(
        self: "CastSelf",
    ) -> "_4355.PartToPartShearCouplingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4355,
        )

        return self.__parent__._cast(_4355.PartToPartShearCouplingCompoundPowerFlow)

    @property
    def part_to_part_shear_coupling_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4357.PartToPartShearCouplingHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4357,
        )

        return self.__parent__._cast(_4357.PartToPartShearCouplingHalfCompoundPowerFlow)

    @property
    def planetary_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4359.PlanetaryGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4359,
        )

        return self.__parent__._cast(_4359.PlanetaryGearSetCompoundPowerFlow)

    @property
    def planet_carrier_compound_power_flow(
        self: "CastSelf",
    ) -> "_4360.PlanetCarrierCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4360,
        )

        return self.__parent__._cast(_4360.PlanetCarrierCompoundPowerFlow)

    @property
    def point_load_compound_power_flow(
        self: "CastSelf",
    ) -> "_4361.PointLoadCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4361,
        )

        return self.__parent__._cast(_4361.PointLoadCompoundPowerFlow)

    @property
    def power_load_compound_power_flow(
        self: "CastSelf",
    ) -> "_4362.PowerLoadCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4362,
        )

        return self.__parent__._cast(_4362.PowerLoadCompoundPowerFlow)

    @property
    def pulley_compound_power_flow(self: "CastSelf") -> "_4363.PulleyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4363,
        )

        return self.__parent__._cast(_4363.PulleyCompoundPowerFlow)

    @property
    def ring_pins_compound_power_flow(
        self: "CastSelf",
    ) -> "_4364.RingPinsCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4364,
        )

        return self.__parent__._cast(_4364.RingPinsCompoundPowerFlow)

    @property
    def rolling_ring_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4366.RollingRingAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4366,
        )

        return self.__parent__._cast(_4366.RollingRingAssemblyCompoundPowerFlow)

    @property
    def rolling_ring_compound_power_flow(
        self: "CastSelf",
    ) -> "_4367.RollingRingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4367,
        )

        return self.__parent__._cast(_4367.RollingRingCompoundPowerFlow)

    @property
    def root_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4369.RootAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4369,
        )

        return self.__parent__._cast(_4369.RootAssemblyCompoundPowerFlow)

    @property
    def shaft_compound_power_flow(self: "CastSelf") -> "_4370.ShaftCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4370,
        )

        return self.__parent__._cast(_4370.ShaftCompoundPowerFlow)

    @property
    def shaft_hub_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4371.ShaftHubConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4371,
        )

        return self.__parent__._cast(_4371.ShaftHubConnectionCompoundPowerFlow)

    @property
    def specialised_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4373.SpecialisedAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4373,
        )

        return self.__parent__._cast(_4373.SpecialisedAssemblyCompoundPowerFlow)

    @property
    def spiral_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4374.SpiralBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4374,
        )

        return self.__parent__._cast(_4374.SpiralBevelGearCompoundPowerFlow)

    @property
    def spiral_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4376.SpiralBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4376,
        )

        return self.__parent__._cast(_4376.SpiralBevelGearSetCompoundPowerFlow)

    @property
    def spring_damper_compound_power_flow(
        self: "CastSelf",
    ) -> "_4377.SpringDamperCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4377,
        )

        return self.__parent__._cast(_4377.SpringDamperCompoundPowerFlow)

    @property
    def spring_damper_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4379.SpringDamperHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4379,
        )

        return self.__parent__._cast(_4379.SpringDamperHalfCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4380.StraightBevelDiffGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4380,
        )

        return self.__parent__._cast(_4380.StraightBevelDiffGearCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4382.StraightBevelDiffGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4382,
        )

        return self.__parent__._cast(_4382.StraightBevelDiffGearSetCompoundPowerFlow)

    @property
    def straight_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4383.StraightBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4383,
        )

        return self.__parent__._cast(_4383.StraightBevelGearCompoundPowerFlow)

    @property
    def straight_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4385.StraightBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4385,
        )

        return self.__parent__._cast(_4385.StraightBevelGearSetCompoundPowerFlow)

    @property
    def straight_bevel_planet_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4386.StraightBevelPlanetGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4386,
        )

        return self.__parent__._cast(_4386.StraightBevelPlanetGearCompoundPowerFlow)

    @property
    def straight_bevel_sun_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4387.StraightBevelSunGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4387,
        )

        return self.__parent__._cast(_4387.StraightBevelSunGearCompoundPowerFlow)

    @property
    def synchroniser_compound_power_flow(
        self: "CastSelf",
    ) -> "_4388.SynchroniserCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4388,
        )

        return self.__parent__._cast(_4388.SynchroniserCompoundPowerFlow)

    @property
    def synchroniser_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4389.SynchroniserHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4389,
        )

        return self.__parent__._cast(_4389.SynchroniserHalfCompoundPowerFlow)

    @property
    def synchroniser_part_compound_power_flow(
        self: "CastSelf",
    ) -> "_4390.SynchroniserPartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4390,
        )

        return self.__parent__._cast(_4390.SynchroniserPartCompoundPowerFlow)

    @property
    def synchroniser_sleeve_compound_power_flow(
        self: "CastSelf",
    ) -> "_4391.SynchroniserSleeveCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4391,
        )

        return self.__parent__._cast(_4391.SynchroniserSleeveCompoundPowerFlow)

    @property
    def torque_converter_compound_power_flow(
        self: "CastSelf",
    ) -> "_4392.TorqueConverterCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4392,
        )

        return self.__parent__._cast(_4392.TorqueConverterCompoundPowerFlow)

    @property
    def torque_converter_pump_compound_power_flow(
        self: "CastSelf",
    ) -> "_4394.TorqueConverterPumpCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4394,
        )

        return self.__parent__._cast(_4394.TorqueConverterPumpCompoundPowerFlow)

    @property
    def torque_converter_turbine_compound_power_flow(
        self: "CastSelf",
    ) -> "_4395.TorqueConverterTurbineCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4395,
        )

        return self.__parent__._cast(_4395.TorqueConverterTurbineCompoundPowerFlow)

    @property
    def unbalanced_mass_compound_power_flow(
        self: "CastSelf",
    ) -> "_4396.UnbalancedMassCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4396,
        )

        return self.__parent__._cast(_4396.UnbalancedMassCompoundPowerFlow)

    @property
    def virtual_component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4397.VirtualComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4397,
        )

        return self.__parent__._cast(_4397.VirtualComponentCompoundPowerFlow)

    @property
    def worm_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4398.WormGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4398,
        )

        return self.__parent__._cast(_4398.WormGearCompoundPowerFlow)

    @property
    def worm_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4400.WormGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4400,
        )

        return self.__parent__._cast(_4400.WormGearSetCompoundPowerFlow)

    @property
    def zerol_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4401.ZerolBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4401,
        )

        return self.__parent__._cast(_4401.ZerolBevelGearCompoundPowerFlow)

    @property
    def zerol_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4403.ZerolBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4403,
        )

        return self.__parent__._cast(_4403.ZerolBevelGearSetCompoundPowerFlow)

    @property
    def part_compound_power_flow(self: "CastSelf") -> "PartCompoundPowerFlow":
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
class PartCompoundPowerFlow(_7715.PartCompoundAnalysis):
    """PartCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(self: "Self") -> "List[_4220.PartPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.PartPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(self: "Self") -> "List[_4220.PartPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.PartPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PartCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundPowerFlow
        """
        return _Cast_PartCompoundPowerFlow(self)
