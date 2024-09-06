"""AbstractShaftOrHousingCompoundHarmonicAnalysis"""

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
    _6037,
)

_ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "AbstractShaftOrHousingCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5812,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6013,
        _6057,
        _6068,
        _6093,
        _6109,
    )

    Self = TypeVar("Self", bound="AbstractShaftOrHousingCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingCompoundHarmonicAnalysis._Cast_AbstractShaftOrHousingCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingCompoundHarmonicAnalysis:
    """Special nested class for casting AbstractShaftOrHousingCompoundHarmonicAnalysis to subclasses."""

    __parent__: "AbstractShaftOrHousingCompoundHarmonicAnalysis"

    @property
    def component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6037.ComponentCompoundHarmonicAnalysis":
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
    def abstract_shaft_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6013.AbstractShaftCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6013,
        )

        return self.__parent__._cast(_6013.AbstractShaftCompoundHarmonicAnalysis)

    @property
    def cycloidal_disc_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6057.CycloidalDiscCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6057,
        )

        return self.__parent__._cast(_6057.CycloidalDiscCompoundHarmonicAnalysis)

    @property
    def fe_part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6068.FEPartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6068,
        )

        return self.__parent__._cast(_6068.FEPartCompoundHarmonicAnalysis)

    @property
    def shaft_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6109.ShaftCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6109,
        )

        return self.__parent__._cast(_6109.ShaftCompoundHarmonicAnalysis)

    @property
    def abstract_shaft_or_housing_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingCompoundHarmonicAnalysis":
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
class AbstractShaftOrHousingCompoundHarmonicAnalysis(
    _6037.ComponentCompoundHarmonicAnalysis
):
    """AbstractShaftOrHousingCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5812.AbstractShaftOrHousingHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.AbstractShaftOrHousingHarmonicAnalysis]

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
    ) -> "List[_5812.AbstractShaftOrHousingHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.AbstractShaftOrHousingHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_AbstractShaftOrHousingCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingCompoundHarmonicAnalysis
        """
        return _Cast_AbstractShaftOrHousingCompoundHarmonicAnalysis(self)
