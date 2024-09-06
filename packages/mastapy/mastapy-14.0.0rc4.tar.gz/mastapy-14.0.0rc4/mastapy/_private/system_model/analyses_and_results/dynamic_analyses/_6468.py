"""DynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7713

_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses", "DynamicAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2734
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7704,
        _7719,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5863,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4737
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5025,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3916,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3123,
    )

    Self = TypeVar("Self", bound="DynamicAnalysis")
    CastSelf = TypeVar("CastSelf", bound="DynamicAnalysis._Cast_DynamicAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("DynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicAnalysis:
    """Special nested class for casting DynamicAnalysis to subclasses."""

    __parent__: "DynamicAnalysis"

    @property
    def fe_analysis(self: "CastSelf") -> "_7713.FEAnalysis":
        return self.__parent__._cast(_7713.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7719.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7704.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7704,
        )

        return self.__parent__._cast(_7704.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2734.Context":
        from mastapy._private.system_model.analyses_and_results import _2734

        return self.__parent__._cast(_2734.Context)

    @property
    def dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3123.DynamicModelForSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3123,
        )

        return self.__parent__._cast(
            _3123.DynamicModelForSteadyStateSynchronousResponse
        )

    @property
    def dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_3916.DynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3916,
        )

        return self.__parent__._cast(_3916.DynamicModelForStabilityAnalysis)

    @property
    def dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_4737.DynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4737,
        )

        return self.__parent__._cast(_4737.DynamicModelForModalAnalysis)

    @property
    def dynamic_model_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5025.DynamicModelAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5025,
        )

        return self.__parent__._cast(_5025.DynamicModelAtAStiffness)

    @property
    def dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5863.DynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5863,
        )

        return self.__parent__._cast(_5863.DynamicModelForHarmonicAnalysis)

    @property
    def dynamic_analysis(self: "CastSelf") -> "DynamicAnalysis":
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
class DynamicAnalysis(_7713.FEAnalysis):
    """DynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_DynamicAnalysis
        """
        return _Cast_DynamicAnalysis(self)
