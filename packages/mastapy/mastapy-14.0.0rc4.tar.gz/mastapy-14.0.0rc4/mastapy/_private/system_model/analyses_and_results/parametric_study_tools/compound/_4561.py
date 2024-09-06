"""BearingCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4589,
)

_BEARING_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "BearingCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2002
    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4412,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4578,
        _4632,
        _4634,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6967
    from mastapy._private.system_model.part_model import _2494

    Self = TypeVar("Self", bound="BearingCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingCompoundParametricStudyTool._Cast_BearingCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingCompoundParametricStudyTool:
    """Special nested class for casting BearingCompoundParametricStudyTool to subclasses."""

    __parent__: "BearingCompoundParametricStudyTool"

    @property
    def connector_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4589.ConnectorCompoundParametricStudyTool":
        return self.__parent__._cast(_4589.ConnectorCompoundParametricStudyTool)

    @property
    def mountable_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4632.MountableComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4632,
        )

        return self.__parent__._cast(
            _4632.MountableComponentCompoundParametricStudyTool
        )

    @property
    def component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4578.ComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4578,
        )

        return self.__parent__._cast(_4578.ComponentCompoundParametricStudyTool)

    @property
    def part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4634.PartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4634,
        )

        return self.__parent__._cast(_4634.PartCompoundParametricStudyTool)

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
    def bearing_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "BearingCompoundParametricStudyTool":
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
class BearingCompoundParametricStudyTool(_4589.ConnectorCompoundParametricStudyTool):
    """BearingCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bearing_duty_cycle_results(self: "Self") -> "_2002.LoadedBearingDutyCycle":
        """mastapy.bearings.bearing_results.LoadedBearingDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingDutyCycleResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_design(self: "Self") -> "_2494.Bearing":
        """mastapy.system_model.part_model.Bearing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def properties_changing_all_load_cases(self: "Self") -> "_6967.BearingLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PropertiesChangingAllLoadCases")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4412.BearingParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.BearingParametricStudyTool]

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
    def planetaries(self: "Self") -> "List[BearingCompoundParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.compound.BearingCompoundParametricStudyTool]

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
    ) -> "List[_4412.BearingParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.BearingParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_BearingCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_BearingCompoundParametricStudyTool
        """
        return _Cast_BearingCompoundParametricStudyTool(self)
