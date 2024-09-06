"""MicrophoneArrayParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4522,
)

_MICROPHONE_ARRAY_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "MicrophoneArrayParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4404,
        _4503,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7072
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2866,
    )
    from mastapy._private.system_model.part_model import _2520

    Self = TypeVar("Self", bound="MicrophoneArrayParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MicrophoneArrayParametricStudyTool._Cast_MicrophoneArrayParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MicrophoneArrayParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicrophoneArrayParametricStudyTool:
    """Special nested class for casting MicrophoneArrayParametricStudyTool to subclasses."""

    __parent__: "MicrophoneArrayParametricStudyTool"

    @property
    def specialised_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4522.SpecialisedAssemblyParametricStudyTool":
        return self.__parent__._cast(_4522.SpecialisedAssemblyParametricStudyTool)

    @property
    def abstract_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4404.AbstractAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4404,
        )

        return self.__parent__._cast(_4404.AbstractAssemblyParametricStudyTool)

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "_4503.PartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4503,
        )

        return self.__parent__._cast(_4503.PartParametricStudyTool)

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
    def microphone_array_parametric_study_tool(
        self: "CastSelf",
    ) -> "MicrophoneArrayParametricStudyTool":
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
class MicrophoneArrayParametricStudyTool(_4522.SpecialisedAssemblyParametricStudyTool):
    """MicrophoneArrayParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MICROPHONE_ARRAY_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def assembly_load_case(self: "Self") -> "_7072.MicrophoneArrayLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.MicrophoneArrayLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_system_deflection_results(
        self: "Self",
    ) -> "List[_2866.MicrophoneArraySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.MicrophoneArraySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblySystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_MicrophoneArrayParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_MicrophoneArrayParametricStudyTool
        """
        return _Cast_MicrophoneArrayParametricStudyTool(self)
