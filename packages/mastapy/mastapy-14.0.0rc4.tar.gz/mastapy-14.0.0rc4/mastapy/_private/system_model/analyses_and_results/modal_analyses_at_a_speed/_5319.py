"""PartModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717

_PART_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "PartModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5237,
        _5238,
        _5239,
        _5242,
        _5243,
        _5244,
        _5245,
        _5247,
        _5249,
        _5250,
        _5251,
        _5252,
        _5254,
        _5255,
        _5256,
        _5257,
        _5259,
        _5260,
        _5262,
        _5264,
        _5265,
        _5267,
        _5268,
        _5270,
        _5271,
        _5273,
        _5275,
        _5276,
        _5278,
        _5279,
        _5280,
        _5282,
        _5285,
        _5286,
        _5287,
        _5288,
        _5289,
        _5291,
        _5292,
        _5293,
        _5294,
        _5296,
        _5297,
        _5298,
        _5300,
        _5301,
        _5304,
        _5305,
        _5307,
        _5308,
        _5310,
        _5311,
        _5312,
        _5313,
        _5314,
        _5315,
        _5316,
        _5317,
        _5318,
        _5321,
        _5322,
        _5324,
        _5325,
        _5326,
        _5327,
        _5328,
        _5329,
        _5331,
        _5333,
        _5334,
        _5335,
        _5336,
        _5338,
        _5340,
        _5341,
        _5343,
        _5344,
        _5346,
        _5347,
        _5349,
        _5350,
        _5351,
        _5352,
        _5353,
        _5354,
        _5355,
        _5356,
        _5358,
        _5359,
        _5360,
        _5361,
        _5362,
        _5364,
        _5365,
        _5367,
        _5368,
    )
    from mastapy._private.system_model.part_model import _2525

    Self = TypeVar("Self", bound="PartModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf", bound="PartModalAnalysisAtASpeed._Cast_PartModalAnalysisAtASpeed"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartModalAnalysisAtASpeed:
    """Special nested class for casting PartModalAnalysisAtASpeed to subclasses."""

    __parent__: "PartModalAnalysisAtASpeed"

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
    def abstract_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5237.AbstractAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5237,
        )

        return self.__parent__._cast(_5237.AbstractAssemblyModalAnalysisAtASpeed)

    @property
    def abstract_shaft_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5238.AbstractShaftModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5238,
        )

        return self.__parent__._cast(_5238.AbstractShaftModalAnalysisAtASpeed)

    @property
    def abstract_shaft_or_housing_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5239.AbstractShaftOrHousingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5239,
        )

        return self.__parent__._cast(_5239.AbstractShaftOrHousingModalAnalysisAtASpeed)

    @property
    def agma_gleason_conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5242.AGMAGleasonConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5242,
        )

        return self.__parent__._cast(_5242.AGMAGleasonConicalGearModalAnalysisAtASpeed)

    @property
    def agma_gleason_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5243.AGMAGleasonConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5243,
        )

        return self.__parent__._cast(
            _5243.AGMAGleasonConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5244.AssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5244,
        )

        return self.__parent__._cast(_5244.AssemblyModalAnalysisAtASpeed)

    @property
    def bearing_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5245.BearingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5245,
        )

        return self.__parent__._cast(_5245.BearingModalAnalysisAtASpeed)

    @property
    def belt_drive_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5247.BeltDriveModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5247,
        )

        return self.__parent__._cast(_5247.BeltDriveModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5249.BevelDifferentialGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5249,
        )

        return self.__parent__._cast(_5249.BevelDifferentialGearModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5250.BevelDifferentialGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5250,
        )

        return self.__parent__._cast(
            _5250.BevelDifferentialGearSetModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5251.BevelDifferentialPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5251,
        )

        return self.__parent__._cast(
            _5251.BevelDifferentialPlanetGearModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_sun_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5252.BevelDifferentialSunGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5252,
        )

        return self.__parent__._cast(
            _5252.BevelDifferentialSunGearModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5254.BevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5254,
        )

        return self.__parent__._cast(_5254.BevelGearModalAnalysisAtASpeed)

    @property
    def bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5255.BevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5255,
        )

        return self.__parent__._cast(_5255.BevelGearSetModalAnalysisAtASpeed)

    @property
    def bolted_joint_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5256.BoltedJointModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5256,
        )

        return self.__parent__._cast(_5256.BoltedJointModalAnalysisAtASpeed)

    @property
    def bolt_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5257.BoltModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5257,
        )

        return self.__parent__._cast(_5257.BoltModalAnalysisAtASpeed)

    @property
    def clutch_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5259.ClutchHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5259,
        )

        return self.__parent__._cast(_5259.ClutchHalfModalAnalysisAtASpeed)

    @property
    def clutch_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5260.ClutchModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5260,
        )

        return self.__parent__._cast(_5260.ClutchModalAnalysisAtASpeed)

    @property
    def component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5262.ComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5262,
        )

        return self.__parent__._cast(_5262.ComponentModalAnalysisAtASpeed)

    @property
    def concept_coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5264.ConceptCouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5264,
        )

        return self.__parent__._cast(_5264.ConceptCouplingHalfModalAnalysisAtASpeed)

    @property
    def concept_coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5265.ConceptCouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5265,
        )

        return self.__parent__._cast(_5265.ConceptCouplingModalAnalysisAtASpeed)

    @property
    def concept_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5267.ConceptGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5267,
        )

        return self.__parent__._cast(_5267.ConceptGearModalAnalysisAtASpeed)

    @property
    def concept_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5268.ConceptGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5268,
        )

        return self.__parent__._cast(_5268.ConceptGearSetModalAnalysisAtASpeed)

    @property
    def conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5270.ConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5270,
        )

        return self.__parent__._cast(_5270.ConicalGearModalAnalysisAtASpeed)

    @property
    def conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5271.ConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5271,
        )

        return self.__parent__._cast(_5271.ConicalGearSetModalAnalysisAtASpeed)

    @property
    def connector_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5273.ConnectorModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5273,
        )

        return self.__parent__._cast(_5273.ConnectorModalAnalysisAtASpeed)

    @property
    def coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5275.CouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5275,
        )

        return self.__parent__._cast(_5275.CouplingHalfModalAnalysisAtASpeed)

    @property
    def coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5276.CouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5276,
        )

        return self.__parent__._cast(_5276.CouplingModalAnalysisAtASpeed)

    @property
    def cvt_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5278.CVTModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5278,
        )

        return self.__parent__._cast(_5278.CVTModalAnalysisAtASpeed)

    @property
    def cvt_pulley_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5279.CVTPulleyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5279,
        )

        return self.__parent__._cast(_5279.CVTPulleyModalAnalysisAtASpeed)

    @property
    def cycloidal_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5280.CycloidalAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5280,
        )

        return self.__parent__._cast(_5280.CycloidalAssemblyModalAnalysisAtASpeed)

    @property
    def cycloidal_disc_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5282.CycloidalDiscModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5282,
        )

        return self.__parent__._cast(_5282.CycloidalDiscModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5285.CylindricalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5285,
        )

        return self.__parent__._cast(_5285.CylindricalGearModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5286.CylindricalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5286,
        )

        return self.__parent__._cast(_5286.CylindricalGearSetModalAnalysisAtASpeed)

    @property
    def cylindrical_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5287.CylindricalPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5287,
        )

        return self.__parent__._cast(_5287.CylindricalPlanetGearModalAnalysisAtASpeed)

    @property
    def datum_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5288.DatumModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5288,
        )

        return self.__parent__._cast(_5288.DatumModalAnalysisAtASpeed)

    @property
    def external_cad_model_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5289.ExternalCADModelModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5289,
        )

        return self.__parent__._cast(_5289.ExternalCADModelModalAnalysisAtASpeed)

    @property
    def face_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5291.FaceGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5291,
        )

        return self.__parent__._cast(_5291.FaceGearModalAnalysisAtASpeed)

    @property
    def face_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5292.FaceGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5292,
        )

        return self.__parent__._cast(_5292.FaceGearSetModalAnalysisAtASpeed)

    @property
    def fe_part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5293.FEPartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5293,
        )

        return self.__parent__._cast(_5293.FEPartModalAnalysisAtASpeed)

    @property
    def flexible_pin_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5294.FlexiblePinAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5294,
        )

        return self.__parent__._cast(_5294.FlexiblePinAssemblyModalAnalysisAtASpeed)

    @property
    def gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5296.GearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5296,
        )

        return self.__parent__._cast(_5296.GearModalAnalysisAtASpeed)

    @property
    def gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5297.GearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5297,
        )

        return self.__parent__._cast(_5297.GearSetModalAnalysisAtASpeed)

    @property
    def guide_dxf_model_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5298.GuideDxfModelModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5298,
        )

        return self.__parent__._cast(_5298.GuideDxfModelModalAnalysisAtASpeed)

    @property
    def hypoid_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5300.HypoidGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5300,
        )

        return self.__parent__._cast(_5300.HypoidGearModalAnalysisAtASpeed)

    @property
    def hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5301.HypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5301,
        )

        return self.__parent__._cast(_5301.HypoidGearSetModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5304.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5304,
        )

        return self.__parent__._cast(
            _5304.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5305.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5305,
        )

        return self.__parent__._cast(
            _5305.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5307.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5307,
        )

        return self.__parent__._cast(
            _5307.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5308.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5308,
        )

        return self.__parent__._cast(
            _5308.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5310.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5310,
        )

        return self.__parent__._cast(
            _5310.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5311.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5311,
        )

        return self.__parent__._cast(
            _5311.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed
        )

    @property
    def mass_disc_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5312.MassDiscModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5312,
        )

        return self.__parent__._cast(_5312.MassDiscModalAnalysisAtASpeed)

    @property
    def measurement_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5313.MeasurementComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5313,
        )

        return self.__parent__._cast(_5313.MeasurementComponentModalAnalysisAtASpeed)

    @property
    def microphone_array_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5314.MicrophoneArrayModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5314,
        )

        return self.__parent__._cast(_5314.MicrophoneArrayModalAnalysisAtASpeed)

    @property
    def microphone_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5315.MicrophoneModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5315,
        )

        return self.__parent__._cast(_5315.MicrophoneModalAnalysisAtASpeed)

    @property
    def mountable_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5317.MountableComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5317,
        )

        return self.__parent__._cast(_5317.MountableComponentModalAnalysisAtASpeed)

    @property
    def oil_seal_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5318.OilSealModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5318,
        )

        return self.__parent__._cast(_5318.OilSealModalAnalysisAtASpeed)

    @property
    def part_to_part_shear_coupling_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5321.PartToPartShearCouplingHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5321,
        )

        return self.__parent__._cast(
            _5321.PartToPartShearCouplingHalfModalAnalysisAtASpeed
        )

    @property
    def part_to_part_shear_coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5322.PartToPartShearCouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5322,
        )

        return self.__parent__._cast(_5322.PartToPartShearCouplingModalAnalysisAtASpeed)

    @property
    def planetary_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5324.PlanetaryGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5324,
        )

        return self.__parent__._cast(_5324.PlanetaryGearSetModalAnalysisAtASpeed)

    @property
    def planet_carrier_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5325.PlanetCarrierModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5325,
        )

        return self.__parent__._cast(_5325.PlanetCarrierModalAnalysisAtASpeed)

    @property
    def point_load_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5326.PointLoadModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5326,
        )

        return self.__parent__._cast(_5326.PointLoadModalAnalysisAtASpeed)

    @property
    def power_load_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5327.PowerLoadModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5327,
        )

        return self.__parent__._cast(_5327.PowerLoadModalAnalysisAtASpeed)

    @property
    def pulley_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5328.PulleyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5328,
        )

        return self.__parent__._cast(_5328.PulleyModalAnalysisAtASpeed)

    @property
    def ring_pins_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5329.RingPinsModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5329,
        )

        return self.__parent__._cast(_5329.RingPinsModalAnalysisAtASpeed)

    @property
    def rolling_ring_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5331.RollingRingAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5331,
        )

        return self.__parent__._cast(_5331.RollingRingAssemblyModalAnalysisAtASpeed)

    @property
    def rolling_ring_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5333.RollingRingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5333,
        )

        return self.__parent__._cast(_5333.RollingRingModalAnalysisAtASpeed)

    @property
    def root_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5334.RootAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5334,
        )

        return self.__parent__._cast(_5334.RootAssemblyModalAnalysisAtASpeed)

    @property
    def shaft_hub_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5335.ShaftHubConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5335,
        )

        return self.__parent__._cast(_5335.ShaftHubConnectionModalAnalysisAtASpeed)

    @property
    def shaft_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5336.ShaftModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5336,
        )

        return self.__parent__._cast(_5336.ShaftModalAnalysisAtASpeed)

    @property
    def specialised_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5338.SpecialisedAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5338,
        )

        return self.__parent__._cast(_5338.SpecialisedAssemblyModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5340.SpiralBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5340,
        )

        return self.__parent__._cast(_5340.SpiralBevelGearModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5341.SpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5341,
        )

        return self.__parent__._cast(_5341.SpiralBevelGearSetModalAnalysisAtASpeed)

    @property
    def spring_damper_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5343.SpringDamperHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5343,
        )

        return self.__parent__._cast(_5343.SpringDamperHalfModalAnalysisAtASpeed)

    @property
    def spring_damper_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5344.SpringDamperModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5344,
        )

        return self.__parent__._cast(_5344.SpringDamperModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5346.StraightBevelDiffGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5346,
        )

        return self.__parent__._cast(_5346.StraightBevelDiffGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5347.StraightBevelDiffGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5347,
        )

        return self.__parent__._cast(
            _5347.StraightBevelDiffGearSetModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5349.StraightBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5349,
        )

        return self.__parent__._cast(_5349.StraightBevelGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5350.StraightBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5350,
        )

        return self.__parent__._cast(_5350.StraightBevelGearSetModalAnalysisAtASpeed)

    @property
    def straight_bevel_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5351.StraightBevelPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5351,
        )

        return self.__parent__._cast(_5351.StraightBevelPlanetGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_sun_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5352.StraightBevelSunGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5352,
        )

        return self.__parent__._cast(_5352.StraightBevelSunGearModalAnalysisAtASpeed)

    @property
    def synchroniser_half_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5353.SynchroniserHalfModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5353,
        )

        return self.__parent__._cast(_5353.SynchroniserHalfModalAnalysisAtASpeed)

    @property
    def synchroniser_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5354.SynchroniserModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5354,
        )

        return self.__parent__._cast(_5354.SynchroniserModalAnalysisAtASpeed)

    @property
    def synchroniser_part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5355.SynchroniserPartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5355,
        )

        return self.__parent__._cast(_5355.SynchroniserPartModalAnalysisAtASpeed)

    @property
    def synchroniser_sleeve_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5356.SynchroniserSleeveModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5356,
        )

        return self.__parent__._cast(_5356.SynchroniserSleeveModalAnalysisAtASpeed)

    @property
    def torque_converter_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5358.TorqueConverterModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5358,
        )

        return self.__parent__._cast(_5358.TorqueConverterModalAnalysisAtASpeed)

    @property
    def torque_converter_pump_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5359.TorqueConverterPumpModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5359,
        )

        return self.__parent__._cast(_5359.TorqueConverterPumpModalAnalysisAtASpeed)

    @property
    def torque_converter_turbine_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5360.TorqueConverterTurbineModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5360,
        )

        return self.__parent__._cast(_5360.TorqueConverterTurbineModalAnalysisAtASpeed)

    @property
    def unbalanced_mass_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5361.UnbalancedMassModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5361,
        )

        return self.__parent__._cast(_5361.UnbalancedMassModalAnalysisAtASpeed)

    @property
    def virtual_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5362.VirtualComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5362,
        )

        return self.__parent__._cast(_5362.VirtualComponentModalAnalysisAtASpeed)

    @property
    def worm_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5364.WormGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5364,
        )

        return self.__parent__._cast(_5364.WormGearModalAnalysisAtASpeed)

    @property
    def worm_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5365.WormGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5365,
        )

        return self.__parent__._cast(_5365.WormGearSetModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5367.ZerolBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5367,
        )

        return self.__parent__._cast(_5367.ZerolBevelGearModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5368.ZerolBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5368,
        )

        return self.__parent__._cast(_5368.ZerolBevelGearSetModalAnalysisAtASpeed)

    @property
    def part_modal_analysis_at_a_speed(self: "CastSelf") -> "PartModalAnalysisAtASpeed":
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
class PartModalAnalysisAtASpeed(_7717.PartStaticLoadAnalysisCase):
    """PartModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def modal_analysis_at_a_speed(self: "Self") -> "_5316.ModalAnalysisAtASpeed":
        """mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.ModalAnalysisAtASpeed

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysisAtASpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_PartModalAnalysisAtASpeed
        """
        return _Cast_PartModalAnalysisAtASpeed(self)
