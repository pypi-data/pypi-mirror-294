"""GearCompoundHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
    _6355,
)

_GEAR_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "GearCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6201,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
        _6280,
        _6287,
        _6290,
        _6291,
        _6292,
        _6301,
        _6305,
        _6308,
        _6323,
        _6326,
        _6329,
        _6338,
        _6342,
        _6345,
        _6348,
        _6357,
        _6377,
        _6383,
        _6386,
        _6389,
        _6390,
        _6401,
        _6404,
    )

    Self = TypeVar("Self", bound="GearCompoundHarmonicAnalysisOfSingleExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearCompoundHarmonicAnalysisOfSingleExcitation._Cast_GearCompoundHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearCompoundHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearCompoundHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting GearCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "GearCompoundHarmonicAnalysisOfSingleExcitation"

    @property
    def mountable_component_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6355.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(
            _6355.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def component_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6301.ComponentCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6301,
        )

        return self.__parent__._cast(
            _6301.ComponentCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6357.PartCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6357,
        )

        return self.__parent__._cast(
            _6357.PartCompoundHarmonicAnalysisOfSingleExcitation
        )

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
    def agma_gleason_conical_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6280.AGMAGleasonConicalGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6280,
        )

        return self.__parent__._cast(
            _6280.AGMAGleasonConicalGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6287.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6287,
        )

        return self.__parent__._cast(
            _6287.BevelDifferentialGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_planet_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6290.BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6290,
        )

        return self.__parent__._cast(
            _6290.BevelDifferentialPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_sun_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6291.BevelDifferentialSunGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6291,
        )

        return self.__parent__._cast(
            _6291.BevelDifferentialSunGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6292.BevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6292,
        )

        return self.__parent__._cast(
            _6292.BevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6305.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6305,
        )

        return self.__parent__._cast(
            _6305.ConceptGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6308.ConicalGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6308,
        )

        return self.__parent__._cast(
            _6308.ConicalGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6323.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6323,
        )

        return self.__parent__._cast(
            _6323.CylindricalGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_planet_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6326.CylindricalPlanetGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6326,
        )

        return self.__parent__._cast(
            _6326.CylindricalPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6329.FaceGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6329,
        )

        return self.__parent__._cast(
            _6329.FaceGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def hypoid_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6338.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6338,
        )

        return self.__parent__._cast(
            _6338.HypoidGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6342.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6342,
        )

        return self.__parent__._cast(
            _6342.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6345.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6345,
        )

        return self.__parent__._cast(
            _6345.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6348.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6348,
        )

        return self.__parent__._cast(
            _6348.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6377.SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6377,
        )

        return self.__parent__._cast(
            _6377.SpiralBevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6383.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6383,
        )

        return self.__parent__._cast(
            _6383.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6386.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6386,
        )

        return self.__parent__._cast(
            _6386.StraightBevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_planet_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6389.StraightBevelPlanetGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6389,
        )

        return self.__parent__._cast(
            _6389.StraightBevelPlanetGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_sun_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6390.StraightBevelSunGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6390,
        )

        return self.__parent__._cast(
            _6390.StraightBevelSunGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6401.WormGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6401,
        )

        return self.__parent__._cast(
            _6401.WormGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def zerol_bevel_gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6404.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6404,
        )

        return self.__parent__._cast(
            _6404.ZerolBevelGearCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "GearCompoundHarmonicAnalysisOfSingleExcitation":
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
class GearCompoundHarmonicAnalysisOfSingleExcitation(
    _6355.MountableComponentCompoundHarmonicAnalysisOfSingleExcitation
):
    """GearCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6201.GearHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.GearHarmonicAnalysisOfSingleExcitation]

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
    ) -> "List[_6201.GearHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.GearHarmonicAnalysisOfSingleExcitation]

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
    def cast_to(self: "Self") -> "_Cast_GearCompoundHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_GearCompoundHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_GearCompoundHarmonicAnalysisOfSingleExcitation(self)
