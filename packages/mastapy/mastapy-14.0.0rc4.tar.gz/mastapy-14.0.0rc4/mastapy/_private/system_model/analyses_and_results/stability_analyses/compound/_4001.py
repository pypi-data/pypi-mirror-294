"""AbstractShaftOrHousingCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4024,
)

_ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "AbstractShaftOrHousingCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3864,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4000,
        _4044,
        _4055,
        _4080,
        _4096,
    )

    Self = TypeVar("Self", bound="AbstractShaftOrHousingCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingCompoundStabilityAnalysis._Cast_AbstractShaftOrHousingCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingCompoundStabilityAnalysis:
    """Special nested class for casting AbstractShaftOrHousingCompoundStabilityAnalysis to subclasses."""

    __parent__: "AbstractShaftOrHousingCompoundStabilityAnalysis"

    @property
    def component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4024.ComponentCompoundStabilityAnalysis":
        return self.__parent__._cast(_4024.ComponentCompoundStabilityAnalysis)

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4080.PartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4080,
        )

        return self.__parent__._cast(_4080.PartCompoundStabilityAnalysis)

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
    def abstract_shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4000.AbstractShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4000,
        )

        return self.__parent__._cast(_4000.AbstractShaftCompoundStabilityAnalysis)

    @property
    def cycloidal_disc_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4044.CycloidalDiscCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4044,
        )

        return self.__parent__._cast(_4044.CycloidalDiscCompoundStabilityAnalysis)

    @property
    def fe_part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4055.FEPartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4055,
        )

        return self.__parent__._cast(_4055.FEPartCompoundStabilityAnalysis)

    @property
    def shaft_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4096.ShaftCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4096,
        )

        return self.__parent__._cast(_4096.ShaftCompoundStabilityAnalysis)

    @property
    def abstract_shaft_or_housing_compound_stability_analysis(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingCompoundStabilityAnalysis":
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
class AbstractShaftOrHousingCompoundStabilityAnalysis(
    _4024.ComponentCompoundStabilityAnalysis
):
    """AbstractShaftOrHousingCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3864.AbstractShaftOrHousingStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AbstractShaftOrHousingStabilityAnalysis]

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
    ) -> "List[_3864.AbstractShaftOrHousingStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AbstractShaftOrHousingStabilityAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftOrHousingCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingCompoundStabilityAnalysis
        """
        return _Cast_AbstractShaftOrHousingCompoundStabilityAnalysis(self)
