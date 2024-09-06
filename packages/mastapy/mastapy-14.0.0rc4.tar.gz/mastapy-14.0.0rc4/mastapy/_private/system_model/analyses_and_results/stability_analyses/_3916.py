"""DynamicModelForStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6468

_DYNAMIC_MODEL_FOR_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "DynamicModelForStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2734
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7704,
        _7713,
        _7719,
    )

    Self = TypeVar("Self", bound="DynamicModelForStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DynamicModelForStabilityAnalysis._Cast_DynamicModelForStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicModelForStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicModelForStabilityAnalysis:
    """Special nested class for casting DynamicModelForStabilityAnalysis to subclasses."""

    __parent__: "DynamicModelForStabilityAnalysis"

    @property
    def dynamic_analysis(self: "CastSelf") -> "_6468.DynamicAnalysis":
        return self.__parent__._cast(_6468.DynamicAnalysis)

    @property
    def fe_analysis(self: "CastSelf") -> "_7713.FEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7713,
        )

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
    def dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "DynamicModelForStabilityAnalysis":
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
class DynamicModelForStabilityAnalysis(_6468.DynamicAnalysis):
    """DynamicModelForStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_MODEL_FOR_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicModelForStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_DynamicModelForStabilityAnalysis
        """
        return _Cast_DynamicModelForStabilityAnalysis(self)
