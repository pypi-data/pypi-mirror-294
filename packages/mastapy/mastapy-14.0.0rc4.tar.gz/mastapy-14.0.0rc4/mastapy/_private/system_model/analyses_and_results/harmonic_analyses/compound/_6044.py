"""ConicalGearCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6070,
)

_CONICAL_GEAR_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ConicalGearCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5843,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6016,
        _6023,
        _6026,
        _6027,
        _6028,
        _6037,
        _6074,
        _6078,
        _6081,
        _6084,
        _6091,
        _6093,
        _6113,
        _6119,
        _6122,
        _6125,
        _6126,
        _6140,
    )

    Self = TypeVar("Self", bound="ConicalGearCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearCompoundHarmonicAnalysis._Cast_ConicalGearCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearCompoundHarmonicAnalysis:
    """Special nested class for casting ConicalGearCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ConicalGearCompoundHarmonicAnalysis"

    @property
    def gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6070.GearCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6070.GearCompoundHarmonicAnalysis)

    @property
    def mountable_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6091.MountableComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6091,
        )

        return self.__parent__._cast(_6091.MountableComponentCompoundHarmonicAnalysis)

    @property
    def component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6037.ComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6037,
        )

        return self.__parent__._cast(_6037.ComponentCompoundHarmonicAnalysis)

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6093.PartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6093,
        )

        return self.__parent__._cast(_6093.PartCompoundHarmonicAnalysis)

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
    def agma_gleason_conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6016.AGMAGleasonConicalGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6016,
        )

        return self.__parent__._cast(
            _6016.AGMAGleasonConicalGearCompoundHarmonicAnalysis
        )

    @property
    def bevel_differential_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6023.BevelDifferentialGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6023,
        )

        return self.__parent__._cast(
            _6023.BevelDifferentialGearCompoundHarmonicAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6026.BevelDifferentialPlanetGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6026,
        )

        return self.__parent__._cast(
            _6026.BevelDifferentialPlanetGearCompoundHarmonicAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6027.BevelDifferentialSunGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6027,
        )

        return self.__parent__._cast(
            _6027.BevelDifferentialSunGearCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6028.BevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6028,
        )

        return self.__parent__._cast(_6028.BevelGearCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6074.HypoidGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6074,
        )

        return self.__parent__._cast(_6074.HypoidGearCompoundHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6078.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6078,
        )

        return self.__parent__._cast(
            _6078.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6081.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6081,
        )

        return self.__parent__._cast(
            _6081.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6084.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6084,
        )

        return self.__parent__._cast(
            _6084.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis
        )

    @property
    def spiral_bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6113.SpiralBevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6113,
        )

        return self.__parent__._cast(_6113.SpiralBevelGearCompoundHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6119.StraightBevelDiffGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6119,
        )

        return self.__parent__._cast(
            _6119.StraightBevelDiffGearCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6122.StraightBevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6122,
        )

        return self.__parent__._cast(_6122.StraightBevelGearCompoundHarmonicAnalysis)

    @property
    def straight_bevel_planet_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6125.StraightBevelPlanetGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6125,
        )

        return self.__parent__._cast(
            _6125.StraightBevelPlanetGearCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6126.StraightBevelSunGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6126,
        )

        return self.__parent__._cast(_6126.StraightBevelSunGearCompoundHarmonicAnalysis)

    @property
    def zerol_bevel_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6140.ZerolBevelGearCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6140,
        )

        return self.__parent__._cast(_6140.ZerolBevelGearCompoundHarmonicAnalysis)

    @property
    def conical_gear_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ConicalGearCompoundHarmonicAnalysis":
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
class ConicalGearCompoundHarmonicAnalysis(_6070.GearCompoundHarmonicAnalysis):
    """ConicalGearCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def planetaries(self: "Self") -> "List[ConicalGearCompoundHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConicalGearCompoundHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5843.ConicalGearHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConicalGearHarmonicAnalysis]

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
    ) -> "List[_5843.ConicalGearHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConicalGearHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearCompoundHarmonicAnalysis
        """
        return _Cast_ConicalGearCompoundHarmonicAnalysis(self)
