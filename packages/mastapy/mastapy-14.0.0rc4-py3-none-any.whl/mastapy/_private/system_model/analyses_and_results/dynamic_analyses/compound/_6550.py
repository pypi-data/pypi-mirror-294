"""AbstractShaftCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6551,
)

_ABSTRACT_SHAFT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "AbstractShaftCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6417,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6574,
        _6594,
        _6630,
        _6646,
    )

    Self = TypeVar("Self", bound="AbstractShaftCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftCompoundDynamicAnalysis._Cast_AbstractShaftCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftCompoundDynamicAnalysis:
    """Special nested class for casting AbstractShaftCompoundDynamicAnalysis to subclasses."""

    __parent__: "AbstractShaftCompoundDynamicAnalysis"

    @property
    def abstract_shaft_or_housing_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6551.AbstractShaftOrHousingCompoundDynamicAnalysis":
        return self.__parent__._cast(
            _6551.AbstractShaftOrHousingCompoundDynamicAnalysis
        )

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6574.ComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6574,
        )

        return self.__parent__._cast(_6574.ComponentCompoundDynamicAnalysis)

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
    def cycloidal_disc_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6594.CycloidalDiscCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6594,
        )

        return self.__parent__._cast(_6594.CycloidalDiscCompoundDynamicAnalysis)

    @property
    def shaft_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6646.ShaftCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6646,
        )

        return self.__parent__._cast(_6646.ShaftCompoundDynamicAnalysis)

    @property
    def abstract_shaft_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "AbstractShaftCompoundDynamicAnalysis":
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
class AbstractShaftCompoundDynamicAnalysis(
    _6551.AbstractShaftOrHousingCompoundDynamicAnalysis
):
    """AbstractShaftCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6417.AbstractShaftDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractShaftDynamicAnalysis]

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
    ) -> "List[_6417.AbstractShaftDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AbstractShaftDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_AbstractShaftCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftCompoundDynamicAnalysis
        """
        return _Cast_AbstractShaftCompoundDynamicAnalysis(self)
