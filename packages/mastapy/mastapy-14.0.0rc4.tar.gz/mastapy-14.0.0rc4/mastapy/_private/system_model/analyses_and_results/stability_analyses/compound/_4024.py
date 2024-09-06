"""ComponentCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4080,
)

_COMPONENT_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "ComponentCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3888,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4000,
        _4001,
        _4003,
        _4007,
        _4010,
        _4013,
        _4014,
        _4015,
        _4018,
        _4022,
        _4027,
        _4028,
        _4031,
        _4035,
        _4038,
        _4041,
        _4044,
        _4046,
        _4049,
        _4050,
        _4051,
        _4052,
        _4055,
        _4057,
        _4060,
        _4061,
        _4065,
        _4068,
        _4071,
        _4074,
        _4075,
        _4077,
        _4078,
        _4079,
        _4083,
        _4086,
        _4087,
        _4088,
        _4089,
        _4090,
        _4093,
        _4096,
        _4097,
        _4100,
        _4105,
        _4106,
        _4109,
        _4112,
        _4113,
        _4115,
        _4116,
        _4117,
        _4120,
        _4121,
        _4122,
        _4123,
        _4124,
        _4127,
    )

    Self = TypeVar("Self", bound="ComponentCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentCompoundStabilityAnalysis._Cast_ComponentCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentCompoundStabilityAnalysis:
    """Special nested class for casting ComponentCompoundStabilityAnalysis to subclasses."""

    __parent__: "ComponentCompoundStabilityAnalysis"

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4080.PartCompoundStabilityAnalysis":
        return self.__parent__._cast(_4080.PartCompoundStabilityAnalysis)

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
    def abstract_shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4000.AbstractShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4000,
        )

        return self.__parent__._cast(_4000.AbstractShaftCompoundStabilityAnalysis)

    @property
    def abstract_shaft_or_housing_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4001.AbstractShaftOrHousingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4001,
        )

        return self.__parent__._cast(
            _4001.AbstractShaftOrHousingCompoundStabilityAnalysis
        )

    @property
    def agma_gleason_conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4003.AGMAGleasonConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4003,
        )

        return self.__parent__._cast(
            _4003.AGMAGleasonConicalGearCompoundStabilityAnalysis
        )

    @property
    def bearing_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4007.BearingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4007,
        )

        return self.__parent__._cast(_4007.BearingCompoundStabilityAnalysis)

    @property
    def bevel_differential_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4010.BevelDifferentialGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4010,
        )

        return self.__parent__._cast(
            _4010.BevelDifferentialGearCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4013.BevelDifferentialPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4013,
        )

        return self.__parent__._cast(
            _4013.BevelDifferentialPlanetGearCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4014.BevelDifferentialSunGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4014,
        )

        return self.__parent__._cast(
            _4014.BevelDifferentialSunGearCompoundStabilityAnalysis
        )

    @property
    def bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4015.BevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4015,
        )

        return self.__parent__._cast(_4015.BevelGearCompoundStabilityAnalysis)

    @property
    def bolt_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4018.BoltCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4018,
        )

        return self.__parent__._cast(_4018.BoltCompoundStabilityAnalysis)

    @property
    def clutch_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4022.ClutchHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4022,
        )

        return self.__parent__._cast(_4022.ClutchHalfCompoundStabilityAnalysis)

    @property
    def concept_coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4027.ConceptCouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4027,
        )

        return self.__parent__._cast(_4027.ConceptCouplingHalfCompoundStabilityAnalysis)

    @property
    def concept_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4028.ConceptGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4028,
        )

        return self.__parent__._cast(_4028.ConceptGearCompoundStabilityAnalysis)

    @property
    def conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4031.ConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4031,
        )

        return self.__parent__._cast(_4031.ConicalGearCompoundStabilityAnalysis)

    @property
    def connector_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4035.ConnectorCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4035,
        )

        return self.__parent__._cast(_4035.ConnectorCompoundStabilityAnalysis)

    @property
    def coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4038.CouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4038,
        )

        return self.__parent__._cast(_4038.CouplingHalfCompoundStabilityAnalysis)

    @property
    def cvt_pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4041.CVTPulleyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4041,
        )

        return self.__parent__._cast(_4041.CVTPulleyCompoundStabilityAnalysis)

    @property
    def cycloidal_disc_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4044.CycloidalDiscCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4044,
        )

        return self.__parent__._cast(_4044.CycloidalDiscCompoundStabilityAnalysis)

    @property
    def cylindrical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4046.CylindricalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4046,
        )

        return self.__parent__._cast(_4046.CylindricalGearCompoundStabilityAnalysis)

    @property
    def cylindrical_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4049.CylindricalPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4049,
        )

        return self.__parent__._cast(
            _4049.CylindricalPlanetGearCompoundStabilityAnalysis
        )

    @property
    def datum_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4050.DatumCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4050,
        )

        return self.__parent__._cast(_4050.DatumCompoundStabilityAnalysis)

    @property
    def external_cad_model_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4051.ExternalCADModelCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4051,
        )

        return self.__parent__._cast(_4051.ExternalCADModelCompoundStabilityAnalysis)

    @property
    def face_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4052.FaceGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4052,
        )

        return self.__parent__._cast(_4052.FaceGearCompoundStabilityAnalysis)

    @property
    def fe_part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4055.FEPartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4055,
        )

        return self.__parent__._cast(_4055.FEPartCompoundStabilityAnalysis)

    @property
    def gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4057.GearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4057,
        )

        return self.__parent__._cast(_4057.GearCompoundStabilityAnalysis)

    @property
    def guide_dxf_model_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4060.GuideDxfModelCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4060,
        )

        return self.__parent__._cast(_4060.GuideDxfModelCompoundStabilityAnalysis)

    @property
    def hypoid_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4061.HypoidGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4061,
        )

        return self.__parent__._cast(_4061.HypoidGearCompoundStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4065.KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4065,
        )

        return self.__parent__._cast(
            _4065.KlingelnbergCycloPalloidConicalGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4068.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4068,
        )

        return self.__parent__._cast(
            _4068.KlingelnbergCycloPalloidHypoidGearCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4071.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4071,
        )

        return self.__parent__._cast(
            _4071.KlingelnbergCycloPalloidSpiralBevelGearCompoundStabilityAnalysis
        )

    @property
    def mass_disc_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4074.MassDiscCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4074,
        )

        return self.__parent__._cast(_4074.MassDiscCompoundStabilityAnalysis)

    @property
    def measurement_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4075.MeasurementComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4075,
        )

        return self.__parent__._cast(
            _4075.MeasurementComponentCompoundStabilityAnalysis
        )

    @property
    def microphone_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4077.MicrophoneCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4077,
        )

        return self.__parent__._cast(_4077.MicrophoneCompoundStabilityAnalysis)

    @property
    def mountable_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4078.MountableComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4078,
        )

        return self.__parent__._cast(_4078.MountableComponentCompoundStabilityAnalysis)

    @property
    def oil_seal_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4079.OilSealCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4079,
        )

        return self.__parent__._cast(_4079.OilSealCompoundStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4083.PartToPartShearCouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4083,
        )

        return self.__parent__._cast(
            _4083.PartToPartShearCouplingHalfCompoundStabilityAnalysis
        )

    @property
    def planet_carrier_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4086.PlanetCarrierCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4086,
        )

        return self.__parent__._cast(_4086.PlanetCarrierCompoundStabilityAnalysis)

    @property
    def point_load_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4087.PointLoadCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4087,
        )

        return self.__parent__._cast(_4087.PointLoadCompoundStabilityAnalysis)

    @property
    def power_load_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4088.PowerLoadCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4088,
        )

        return self.__parent__._cast(_4088.PowerLoadCompoundStabilityAnalysis)

    @property
    def pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4089.PulleyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4089,
        )

        return self.__parent__._cast(_4089.PulleyCompoundStabilityAnalysis)

    @property
    def ring_pins_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4090.RingPinsCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4090,
        )

        return self.__parent__._cast(_4090.RingPinsCompoundStabilityAnalysis)

    @property
    def rolling_ring_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4093.RollingRingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4093,
        )

        return self.__parent__._cast(_4093.RollingRingCompoundStabilityAnalysis)

    @property
    def shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4096.ShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4096,
        )

        return self.__parent__._cast(_4096.ShaftCompoundStabilityAnalysis)

    @property
    def shaft_hub_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4097.ShaftHubConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4097,
        )

        return self.__parent__._cast(_4097.ShaftHubConnectionCompoundStabilityAnalysis)

    @property
    def spiral_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4100.SpiralBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4100,
        )

        return self.__parent__._cast(_4100.SpiralBevelGearCompoundStabilityAnalysis)

    @property
    def spring_damper_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4105.SpringDamperHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4105,
        )

        return self.__parent__._cast(_4105.SpringDamperHalfCompoundStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4106.StraightBevelDiffGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4106,
        )

        return self.__parent__._cast(
            _4106.StraightBevelDiffGearCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4109.StraightBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4109,
        )

        return self.__parent__._cast(_4109.StraightBevelGearCompoundStabilityAnalysis)

    @property
    def straight_bevel_planet_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4112.StraightBevelPlanetGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4112,
        )

        return self.__parent__._cast(
            _4112.StraightBevelPlanetGearCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4113.StraightBevelSunGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4113,
        )

        return self.__parent__._cast(
            _4113.StraightBevelSunGearCompoundStabilityAnalysis
        )

    @property
    def synchroniser_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4115.SynchroniserHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4115,
        )

        return self.__parent__._cast(_4115.SynchroniserHalfCompoundStabilityAnalysis)

    @property
    def synchroniser_part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4116.SynchroniserPartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4116,
        )

        return self.__parent__._cast(_4116.SynchroniserPartCompoundStabilityAnalysis)

    @property
    def synchroniser_sleeve_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4117.SynchroniserSleeveCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4117,
        )

        return self.__parent__._cast(_4117.SynchroniserSleeveCompoundStabilityAnalysis)

    @property
    def torque_converter_pump_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4120.TorqueConverterPumpCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4120,
        )

        return self.__parent__._cast(_4120.TorqueConverterPumpCompoundStabilityAnalysis)

    @property
    def torque_converter_turbine_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4121.TorqueConverterTurbineCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4121,
        )

        return self.__parent__._cast(
            _4121.TorqueConverterTurbineCompoundStabilityAnalysis
        )

    @property
    def unbalanced_mass_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4122.UnbalancedMassCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4122,
        )

        return self.__parent__._cast(_4122.UnbalancedMassCompoundStabilityAnalysis)

    @property
    def virtual_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4123.VirtualComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4123,
        )

        return self.__parent__._cast(_4123.VirtualComponentCompoundStabilityAnalysis)

    @property
    def worm_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4124.WormGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4124,
        )

        return self.__parent__._cast(_4124.WormGearCompoundStabilityAnalysis)

    @property
    def zerol_bevel_gear_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4127.ZerolBevelGearCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4127,
        )

        return self.__parent__._cast(_4127.ZerolBevelGearCompoundStabilityAnalysis)

    @property
    def component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "ComponentCompoundStabilityAnalysis":
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
class ComponentCompoundStabilityAnalysis(_4080.PartCompoundStabilityAnalysis):
    """ComponentCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3888.ComponentStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ComponentStabilityAnalysis]

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
    ) -> "List[_3888.ComponentStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.ComponentStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ComponentCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ComponentCompoundStabilityAnalysis
        """
        return _Cast_ComponentCompoundStabilityAnalysis(self)
