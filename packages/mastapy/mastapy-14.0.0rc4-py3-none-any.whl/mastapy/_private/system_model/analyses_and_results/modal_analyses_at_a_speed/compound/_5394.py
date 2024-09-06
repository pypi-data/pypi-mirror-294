"""ComponentCompoundModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5450,
)

_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "ComponentCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5262,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5370,
        _5371,
        _5373,
        _5377,
        _5380,
        _5383,
        _5384,
        _5385,
        _5388,
        _5392,
        _5397,
        _5398,
        _5401,
        _5405,
        _5408,
        _5411,
        _5414,
        _5416,
        _5419,
        _5420,
        _5421,
        _5422,
        _5425,
        _5427,
        _5430,
        _5431,
        _5435,
        _5438,
        _5441,
        _5444,
        _5445,
        _5447,
        _5448,
        _5449,
        _5453,
        _5456,
        _5457,
        _5458,
        _5459,
        _5460,
        _5463,
        _5466,
        _5467,
        _5470,
        _5475,
        _5476,
        _5479,
        _5482,
        _5483,
        _5485,
        _5486,
        _5487,
        _5490,
        _5491,
        _5492,
        _5493,
        _5494,
        _5497,
    )

    Self = TypeVar("Self", bound="ComponentCompoundModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentCompoundModalAnalysisAtASpeed._Cast_ComponentCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentCompoundModalAnalysisAtASpeed:
    """Special nested class for casting ComponentCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "ComponentCompoundModalAnalysisAtASpeed"

    @property
    def part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5450.PartCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(_5450.PartCompoundModalAnalysisAtASpeed)

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
    def abstract_shaft_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5370.AbstractShaftCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5370,
        )

        return self.__parent__._cast(_5370.AbstractShaftCompoundModalAnalysisAtASpeed)

    @property
    def abstract_shaft_or_housing_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5371.AbstractShaftOrHousingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5371,
        )

        return self.__parent__._cast(
            _5371.AbstractShaftOrHousingCompoundModalAnalysisAtASpeed
        )

    @property
    def agma_gleason_conical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5373.AGMAGleasonConicalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5373,
        )

        return self.__parent__._cast(
            _5373.AGMAGleasonConicalGearCompoundModalAnalysisAtASpeed
        )

    @property
    def bearing_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5377.BearingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5377,
        )

        return self.__parent__._cast(_5377.BearingCompoundModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5380.BevelDifferentialGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5380,
        )

        return self.__parent__._cast(
            _5380.BevelDifferentialGearCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_planet_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5383.BevelDifferentialPlanetGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5383,
        )

        return self.__parent__._cast(
            _5383.BevelDifferentialPlanetGearCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_sun_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5384.BevelDifferentialSunGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5384,
        )

        return self.__parent__._cast(
            _5384.BevelDifferentialSunGearCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5385.BevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5385,
        )

        return self.__parent__._cast(_5385.BevelGearCompoundModalAnalysisAtASpeed)

    @property
    def bolt_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5388.BoltCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5388,
        )

        return self.__parent__._cast(_5388.BoltCompoundModalAnalysisAtASpeed)

    @property
    def clutch_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5392.ClutchHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5392,
        )

        return self.__parent__._cast(_5392.ClutchHalfCompoundModalAnalysisAtASpeed)

    @property
    def concept_coupling_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5397.ConceptCouplingHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5397,
        )

        return self.__parent__._cast(
            _5397.ConceptCouplingHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def concept_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5398.ConceptGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5398,
        )

        return self.__parent__._cast(_5398.ConceptGearCompoundModalAnalysisAtASpeed)

    @property
    def conical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5401.ConicalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5401,
        )

        return self.__parent__._cast(_5401.ConicalGearCompoundModalAnalysisAtASpeed)

    @property
    def connector_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5405.ConnectorCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5405,
        )

        return self.__parent__._cast(_5405.ConnectorCompoundModalAnalysisAtASpeed)

    @property
    def coupling_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5408.CouplingHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5408,
        )

        return self.__parent__._cast(_5408.CouplingHalfCompoundModalAnalysisAtASpeed)

    @property
    def cvt_pulley_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5411.CVTPulleyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5411,
        )

        return self.__parent__._cast(_5411.CVTPulleyCompoundModalAnalysisAtASpeed)

    @property
    def cycloidal_disc_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5414.CycloidalDiscCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5414,
        )

        return self.__parent__._cast(_5414.CycloidalDiscCompoundModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5416.CylindricalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5416,
        )

        return self.__parent__._cast(_5416.CylindricalGearCompoundModalAnalysisAtASpeed)

    @property
    def cylindrical_planet_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5419.CylindricalPlanetGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5419,
        )

        return self.__parent__._cast(
            _5419.CylindricalPlanetGearCompoundModalAnalysisAtASpeed
        )

    @property
    def datum_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5420.DatumCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5420,
        )

        return self.__parent__._cast(_5420.DatumCompoundModalAnalysisAtASpeed)

    @property
    def external_cad_model_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5421.ExternalCADModelCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5421,
        )

        return self.__parent__._cast(
            _5421.ExternalCADModelCompoundModalAnalysisAtASpeed
        )

    @property
    def face_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5422.FaceGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5422,
        )

        return self.__parent__._cast(_5422.FaceGearCompoundModalAnalysisAtASpeed)

    @property
    def fe_part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5425.FEPartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5425,
        )

        return self.__parent__._cast(_5425.FEPartCompoundModalAnalysisAtASpeed)

    @property
    def gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5427.GearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5427,
        )

        return self.__parent__._cast(_5427.GearCompoundModalAnalysisAtASpeed)

    @property
    def guide_dxf_model_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5430.GuideDxfModelCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5430,
        )

        return self.__parent__._cast(_5430.GuideDxfModelCompoundModalAnalysisAtASpeed)

    @property
    def hypoid_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5431.HypoidGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5431,
        )

        return self.__parent__._cast(_5431.HypoidGearCompoundModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5435.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5435,
        )

        return self.__parent__._cast(
            _5435.KlingelnbergCycloPalloidConicalGearCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5438.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5438,
        )

        return self.__parent__._cast(
            _5438.KlingelnbergCycloPalloidHypoidGearCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5441.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5441,
        )

        return self.__parent__._cast(
            _5441.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtASpeed
        )

    @property
    def mass_disc_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5444.MassDiscCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5444,
        )

        return self.__parent__._cast(_5444.MassDiscCompoundModalAnalysisAtASpeed)

    @property
    def measurement_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5445.MeasurementComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5445,
        )

        return self.__parent__._cast(
            _5445.MeasurementComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def microphone_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5447.MicrophoneCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5447,
        )

        return self.__parent__._cast(_5447.MicrophoneCompoundModalAnalysisAtASpeed)

    @property
    def mountable_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5448.MountableComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5448,
        )

        return self.__parent__._cast(
            _5448.MountableComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def oil_seal_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5449.OilSealCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5449,
        )

        return self.__parent__._cast(_5449.OilSealCompoundModalAnalysisAtASpeed)

    @property
    def part_to_part_shear_coupling_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5453.PartToPartShearCouplingHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5453,
        )

        return self.__parent__._cast(
            _5453.PartToPartShearCouplingHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def planet_carrier_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5456.PlanetCarrierCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5456,
        )

        return self.__parent__._cast(_5456.PlanetCarrierCompoundModalAnalysisAtASpeed)

    @property
    def point_load_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5457.PointLoadCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5457,
        )

        return self.__parent__._cast(_5457.PointLoadCompoundModalAnalysisAtASpeed)

    @property
    def power_load_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5458.PowerLoadCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5458,
        )

        return self.__parent__._cast(_5458.PowerLoadCompoundModalAnalysisAtASpeed)

    @property
    def pulley_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5459.PulleyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5459,
        )

        return self.__parent__._cast(_5459.PulleyCompoundModalAnalysisAtASpeed)

    @property
    def ring_pins_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5460.RingPinsCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5460,
        )

        return self.__parent__._cast(_5460.RingPinsCompoundModalAnalysisAtASpeed)

    @property
    def rolling_ring_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5463.RollingRingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5463,
        )

        return self.__parent__._cast(_5463.RollingRingCompoundModalAnalysisAtASpeed)

    @property
    def shaft_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5466.ShaftCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5466,
        )

        return self.__parent__._cast(_5466.ShaftCompoundModalAnalysisAtASpeed)

    @property
    def shaft_hub_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5467.ShaftHubConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5467,
        )

        return self.__parent__._cast(
            _5467.ShaftHubConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5470.SpiralBevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5470,
        )

        return self.__parent__._cast(_5470.SpiralBevelGearCompoundModalAnalysisAtASpeed)

    @property
    def spring_damper_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5475.SpringDamperHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5475,
        )

        return self.__parent__._cast(
            _5475.SpringDamperHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_diff_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5476.StraightBevelDiffGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5476,
        )

        return self.__parent__._cast(
            _5476.StraightBevelDiffGearCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5479.StraightBevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5479,
        )

        return self.__parent__._cast(
            _5479.StraightBevelGearCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_planet_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5482.StraightBevelPlanetGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5482,
        )

        return self.__parent__._cast(
            _5482.StraightBevelPlanetGearCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_sun_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5483.StraightBevelSunGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5483,
        )

        return self.__parent__._cast(
            _5483.StraightBevelSunGearCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_half_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5485.SynchroniserHalfCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5485,
        )

        return self.__parent__._cast(
            _5485.SynchroniserHalfCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5486.SynchroniserPartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5486,
        )

        return self.__parent__._cast(
            _5486.SynchroniserPartCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_sleeve_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5487.SynchroniserSleeveCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5487,
        )

        return self.__parent__._cast(
            _5487.SynchroniserSleeveCompoundModalAnalysisAtASpeed
        )

    @property
    def torque_converter_pump_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5490.TorqueConverterPumpCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5490,
        )

        return self.__parent__._cast(
            _5490.TorqueConverterPumpCompoundModalAnalysisAtASpeed
        )

    @property
    def torque_converter_turbine_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5491.TorqueConverterTurbineCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5491,
        )

        return self.__parent__._cast(
            _5491.TorqueConverterTurbineCompoundModalAnalysisAtASpeed
        )

    @property
    def unbalanced_mass_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5492.UnbalancedMassCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5492,
        )

        return self.__parent__._cast(_5492.UnbalancedMassCompoundModalAnalysisAtASpeed)

    @property
    def virtual_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5493.VirtualComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5493,
        )

        return self.__parent__._cast(
            _5493.VirtualComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def worm_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5494.WormGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5494,
        )

        return self.__parent__._cast(_5494.WormGearCompoundModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5497.ZerolBevelGearCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5497,
        )

        return self.__parent__._cast(_5497.ZerolBevelGearCompoundModalAnalysisAtASpeed)

    @property
    def component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "ComponentCompoundModalAnalysisAtASpeed":
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
class ComponentCompoundModalAnalysisAtASpeed(_5450.PartCompoundModalAnalysisAtASpeed):
    """ComponentCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5262.ComponentModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.ComponentModalAnalysisAtASpeed]

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
    ) -> "List[_5262.ComponentModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.ComponentModalAnalysisAtASpeed]

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
    def cast_to(self: "Self") -> "_Cast_ComponentCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_ComponentCompoundModalAnalysisAtASpeed
        """
        return _Cast_ComponentCompoundModalAnalysisAtASpeed(self)
