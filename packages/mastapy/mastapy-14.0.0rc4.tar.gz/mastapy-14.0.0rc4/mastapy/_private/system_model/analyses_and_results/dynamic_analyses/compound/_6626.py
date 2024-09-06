"""MicrophoneArrayCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6649,
)

_MICROPHONE_ARRAY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "MicrophoneArrayCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6495,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6549,
        _6630,
    )
    from mastapy._private.system_model.part_model import _2520

    Self = TypeVar("Self", bound="MicrophoneArrayCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicrophoneArrayCompoundDynamicAnalysis._Cast_MicrophoneArrayCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicrophoneArrayCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicrophoneArrayCompoundDynamicAnalysis:
    """Special nested class for casting MicrophoneArrayCompoundDynamicAnalysis to subclasses."""

    __parent__: "MicrophoneArrayCompoundDynamicAnalysis"

    @property
    def specialised_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6649.SpecialisedAssemblyCompoundDynamicAnalysis":
        return self.__parent__._cast(_6649.SpecialisedAssemblyCompoundDynamicAnalysis)

    @property
    def abstract_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6549.AbstractAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6549,
        )

        return self.__parent__._cast(_6549.AbstractAssemblyCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6630.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6630,
        )

        return self.__parent__._cast(_6630.PartCompoundDynamicAnalysis)

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
    def microphone_array_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "MicrophoneArrayCompoundDynamicAnalysis":
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
class MicrophoneArrayCompoundDynamicAnalysis(
    _6649.SpecialisedAssemblyCompoundDynamicAnalysis
):
    """MicrophoneArrayCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICROPHONE_ARRAY_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2520.MicrophoneArray":
        """mastapy.system_model.part_model.MicrophoneArray

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2520.MicrophoneArray":
        """mastapy.system_model.part_model.MicrophoneArray

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6495.MicrophoneArrayDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.MicrophoneArrayDynamicAnalysis]

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
    ) -> "List[_6495.MicrophoneArrayDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.MicrophoneArrayDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_MicrophoneArrayCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MicrophoneArrayCompoundDynamicAnalysis
        """
        return _Cast_MicrophoneArrayCompoundDynamicAnalysis(self)
