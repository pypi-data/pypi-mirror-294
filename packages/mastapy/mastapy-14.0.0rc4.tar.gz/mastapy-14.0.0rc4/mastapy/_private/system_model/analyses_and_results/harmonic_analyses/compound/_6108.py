"""RootAssemblyCompoundHarmonicAnalysis"""

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
    _6019,
)

_ROOT_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "RootAssemblyCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5938,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6012,
        _6093,
    )

    Self = TypeVar("Self", bound="RootAssemblyCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblyCompoundHarmonicAnalysis._Cast_RootAssemblyCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyCompoundHarmonicAnalysis:
    """Special nested class for casting RootAssemblyCompoundHarmonicAnalysis to subclasses."""

    __parent__: "RootAssemblyCompoundHarmonicAnalysis"

    @property
    def assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6019.AssemblyCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6019.AssemblyCompoundHarmonicAnalysis)

    @property
    def abstract_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6012.AbstractAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6012,
        )

        return self.__parent__._cast(_6012.AbstractAssemblyCompoundHarmonicAnalysis)

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
    def root_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "RootAssemblyCompoundHarmonicAnalysis":
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
class RootAssemblyCompoundHarmonicAnalysis(_6019.AssemblyCompoundHarmonicAnalysis):
    """RootAssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROOT_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5938.RootAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.RootAssemblyHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5938.RootAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.RootAssemblyHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RootAssemblyCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyCompoundHarmonicAnalysis
        """
        return _Cast_RootAssemblyCompoundHarmonicAnalysis(self)
