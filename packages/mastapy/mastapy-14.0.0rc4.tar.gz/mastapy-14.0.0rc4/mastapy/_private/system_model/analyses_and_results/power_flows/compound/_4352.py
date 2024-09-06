"""MountableComponentCompoundPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4298,
)

_MOUNTABLE_COMPONENT_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "MountableComponentCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4218
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4277,
        _4281,
        _4284,
        _4287,
        _4288,
        _4289,
        _4296,
        _4301,
        _4302,
        _4305,
        _4309,
        _4312,
        _4315,
        _4320,
        _4323,
        _4326,
        _4331,
        _4335,
        _4339,
        _4342,
        _4345,
        _4348,
        _4349,
        _4353,
        _4354,
        _4357,
        _4360,
        _4361,
        _4362,
        _4363,
        _4364,
        _4367,
        _4371,
        _4374,
        _4379,
        _4380,
        _4383,
        _4386,
        _4387,
        _4389,
        _4390,
        _4391,
        _4394,
        _4395,
        _4396,
        _4397,
        _4398,
        _4401,
    )

    Self = TypeVar("Self", bound="MountableComponentCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentCompoundPowerFlow._Cast_MountableComponentCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentCompoundPowerFlow:
    """Special nested class for casting MountableComponentCompoundPowerFlow to subclasses."""

    __parent__: "MountableComponentCompoundPowerFlow"

    @property
    def component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4298.ComponentCompoundPowerFlow":
        return self.__parent__._cast(_4298.ComponentCompoundPowerFlow)

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4354.PartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4354,
        )

        return self.__parent__._cast(_4354.PartCompoundPowerFlow)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7715.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

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
    def agma_gleason_conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4277.AGMAGleasonConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4277,
        )

        return self.__parent__._cast(_4277.AGMAGleasonConicalGearCompoundPowerFlow)

    @property
    def bearing_compound_power_flow(
        self: "CastSelf",
    ) -> "_4281.BearingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4281,
        )

        return self.__parent__._cast(_4281.BearingCompoundPowerFlow)

    @property
    def bevel_differential_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4284.BevelDifferentialGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4284,
        )

        return self.__parent__._cast(_4284.BevelDifferentialGearCompoundPowerFlow)

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
    def clutch_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4296.ClutchHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4296,
        )

        return self.__parent__._cast(_4296.ClutchHalfCompoundPowerFlow)

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
    def conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4305.ConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4305,
        )

        return self.__parent__._cast(_4305.ConicalGearCompoundPowerFlow)

    @property
    def connector_compound_power_flow(
        self: "CastSelf",
    ) -> "_4309.ConnectorCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4309,
        )

        return self.__parent__._cast(_4309.ConnectorCompoundPowerFlow)

    @property
    def coupling_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4312.CouplingHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4312,
        )

        return self.__parent__._cast(_4312.CouplingHalfCompoundPowerFlow)

    @property
    def cvt_pulley_compound_power_flow(
        self: "CastSelf",
    ) -> "_4315.CVTPulleyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4315,
        )

        return self.__parent__._cast(_4315.CVTPulleyCompoundPowerFlow)

    @property
    def cylindrical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4320.CylindricalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4320,
        )

        return self.__parent__._cast(_4320.CylindricalGearCompoundPowerFlow)

    @property
    def cylindrical_planet_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4323.CylindricalPlanetGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4323,
        )

        return self.__parent__._cast(_4323.CylindricalPlanetGearCompoundPowerFlow)

    @property
    def face_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4326.FaceGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4326,
        )

        return self.__parent__._cast(_4326.FaceGearCompoundPowerFlow)

    @property
    def gear_compound_power_flow(self: "CastSelf") -> "_4331.GearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4331,
        )

        return self.__parent__._cast(_4331.GearCompoundPowerFlow)

    @property
    def hypoid_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4335.HypoidGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4335,
        )

        return self.__parent__._cast(_4335.HypoidGearCompoundPowerFlow)

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
    def oil_seal_compound_power_flow(
        self: "CastSelf",
    ) -> "_4353.OilSealCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4353,
        )

        return self.__parent__._cast(_4353.OilSealCompoundPowerFlow)

    @property
    def part_to_part_shear_coupling_half_compound_power_flow(
        self: "CastSelf",
    ) -> "_4357.PartToPartShearCouplingHalfCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4357,
        )

        return self.__parent__._cast(_4357.PartToPartShearCouplingHalfCompoundPowerFlow)

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
    def rolling_ring_compound_power_flow(
        self: "CastSelf",
    ) -> "_4367.RollingRingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4367,
        )

        return self.__parent__._cast(_4367.RollingRingCompoundPowerFlow)

    @property
    def shaft_hub_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4371.ShaftHubConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4371,
        )

        return self.__parent__._cast(_4371.ShaftHubConnectionCompoundPowerFlow)

    @property
    def spiral_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4374.SpiralBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4374,
        )

        return self.__parent__._cast(_4374.SpiralBevelGearCompoundPowerFlow)

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
    def straight_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4383.StraightBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4383,
        )

        return self.__parent__._cast(_4383.StraightBevelGearCompoundPowerFlow)

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
    def zerol_bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4401.ZerolBevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4401,
        )

        return self.__parent__._cast(_4401.ZerolBevelGearCompoundPowerFlow)

    @property
    def mountable_component_compound_power_flow(
        self: "CastSelf",
    ) -> "MountableComponentCompoundPowerFlow":
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
class MountableComponentCompoundPowerFlow(_4298.ComponentCompoundPowerFlow):
    """MountableComponentCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4218.MountableComponentPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.MountableComponentPowerFlow]

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4218.MountableComponentPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.MountableComponentPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_MountableComponentCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentCompoundPowerFlow
        """
        return _Cast_MountableComponentCompoundPowerFlow(self)
