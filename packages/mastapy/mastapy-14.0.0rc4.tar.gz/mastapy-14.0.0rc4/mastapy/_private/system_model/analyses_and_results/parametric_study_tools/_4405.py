"""AbstractShaftOrHousingParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4429,
)

_ABSTRACT_SHAFT_OR_HOUSING_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "AbstractShaftOrHousingParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4406,
        _4449,
        _4467,
        _4503,
        _4520,
    )
    from mastapy._private.system_model.part_model import _2491

    Self = TypeVar("Self", bound="AbstractShaftOrHousingParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingParametricStudyTool._Cast_AbstractShaftOrHousingParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingParametricStudyTool:
    """Special nested class for casting AbstractShaftOrHousingParametricStudyTool to subclasses."""

    __parent__: "AbstractShaftOrHousingParametricStudyTool"

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4429.ComponentParametricStudyTool":
        return self.__parent__._cast(_4429.ComponentParametricStudyTool)

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
    def abstract_shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4406.AbstractShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4406,
        )

        return self.__parent__._cast(_4406.AbstractShaftParametricStudyTool)

    @property
    def cycloidal_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4449.CycloidalDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4449,
        )

        return self.__parent__._cast(_4449.CycloidalDiscParametricStudyTool)

    @property
    def fe_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4467.FEPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4467,
        )

        return self.__parent__._cast(_4467.FEPartParametricStudyTool)

    @property
    def shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4520.ShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4520,
        )

        return self.__parent__._cast(_4520.ShaftParametricStudyTool)

    @property
    def abstract_shaft_or_housing_parametric_study_tool(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingParametricStudyTool":
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
class AbstractShaftOrHousingParametricStudyTool(_4429.ComponentParametricStudyTool):
    """AbstractShaftOrHousingParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2491.AbstractShaftOrHousing":
        """mastapy.system_model.part_model.AbstractShaftOrHousing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftOrHousingParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingParametricStudyTool
        """
        return _Cast_AbstractShaftOrHousingParametricStudyTool(self)
