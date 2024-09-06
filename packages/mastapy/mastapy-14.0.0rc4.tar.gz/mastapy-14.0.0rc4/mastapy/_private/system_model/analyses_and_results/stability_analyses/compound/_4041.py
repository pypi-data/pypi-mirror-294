"""CVTPulleyCompoundStabilityAnalysis"""

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
    _4089,
)

_CVT_PULLEY_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "CVTPulleyCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3905,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4024,
        _4038,
        _4078,
        _4080,
    )

    Self = TypeVar("Self", bound="CVTPulleyCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CVTPulleyCompoundStabilityAnalysis._Cast_CVTPulleyCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleyCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTPulleyCompoundStabilityAnalysis:
    """Special nested class for casting CVTPulleyCompoundStabilityAnalysis to subclasses."""

    __parent__: "CVTPulleyCompoundStabilityAnalysis"

    @property
    def pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4089.PulleyCompoundStabilityAnalysis":
        return self.__parent__._cast(_4089.PulleyCompoundStabilityAnalysis)

    @property
    def coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4038.CouplingHalfCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4038,
        )

        return self.__parent__._cast(_4038.CouplingHalfCompoundStabilityAnalysis)

    @property
    def mountable_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4078.MountableComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4078,
        )

        return self.__parent__._cast(_4078.MountableComponentCompoundStabilityAnalysis)

    @property
    def component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4024.ComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4024,
        )

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
    def cvt_pulley_compound_stability_analysis(
        self: "CastSelf",
    ) -> "CVTPulleyCompoundStabilityAnalysis":
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
class CVTPulleyCompoundStabilityAnalysis(_4089.PulleyCompoundStabilityAnalysis):
    """CVTPulleyCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_PULLEY_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3905.CVTPulleyStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CVTPulleyStabilityAnalysis]

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
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3905.CVTPulleyStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.CVTPulleyStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CVTPulleyCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CVTPulleyCompoundStabilityAnalysis
        """
        return _Cast_CVTPulleyCompoundStabilityAnalysis(self)
