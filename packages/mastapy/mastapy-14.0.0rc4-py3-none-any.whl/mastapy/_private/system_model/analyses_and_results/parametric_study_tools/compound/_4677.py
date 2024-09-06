"""VirtualComponentCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4632,
)

_VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "VirtualComponentCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4546,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4578,
        _4628,
        _4629,
        _4634,
        _4641,
        _4642,
        _4676,
    )

    Self = TypeVar("Self", bound="VirtualComponentCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentCompoundParametricStudyTool._Cast_VirtualComponentCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentCompoundParametricStudyTool:
    """Special nested class for casting VirtualComponentCompoundParametricStudyTool to subclasses."""

    __parent__: "VirtualComponentCompoundParametricStudyTool"

    @property
    def mountable_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4632.MountableComponentCompoundParametricStudyTool":
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
    def mass_disc_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4628.MassDiscCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4628,
        )

        return self.__parent__._cast(_4628.MassDiscCompoundParametricStudyTool)

    @property
    def measurement_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4629.MeasurementComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4629,
        )

        return self.__parent__._cast(
            _4629.MeasurementComponentCompoundParametricStudyTool
        )

    @property
    def point_load_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4641.PointLoadCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4641,
        )

        return self.__parent__._cast(_4641.PointLoadCompoundParametricStudyTool)

    @property
    def power_load_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4642.PowerLoadCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4642,
        )

        return self.__parent__._cast(_4642.PowerLoadCompoundParametricStudyTool)

    @property
    def unbalanced_mass_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4676.UnbalancedMassCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4676,
        )

        return self.__parent__._cast(_4676.UnbalancedMassCompoundParametricStudyTool)

    @property
    def virtual_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "VirtualComponentCompoundParametricStudyTool":
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
class VirtualComponentCompoundParametricStudyTool(
    _4632.MountableComponentCompoundParametricStudyTool
):
    """VirtualComponentCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4546.VirtualComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool]

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
    ) -> "List[_4546.VirtualComponentParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_VirtualComponentCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentCompoundParametricStudyTool
        """
        return _Cast_VirtualComponentCompoundParametricStudyTool(self)
