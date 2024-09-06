"""CompoundSteadyStateSynchronousResponseAtASpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results import _2703

_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults",
    "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7722

    Self = TypeVar(
        "Self", bound="CompoundSteadyStateSynchronousResponseAtASpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CompoundSteadyStateSynchronousResponseAtASpeedAnalysis._Cast_CompoundSteadyStateSynchronousResponseAtASpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CompoundSteadyStateSynchronousResponseAtASpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundSteadyStateSynchronousResponseAtASpeedAnalysis:
    """Special nested class for casting CompoundSteadyStateSynchronousResponseAtASpeedAnalysis to subclasses."""

    __parent__: "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis"

    @property
    def compound_analysis(self: "CastSelf") -> "_2703.CompoundAnalysis":
        return self.__parent__._cast(_2703.CompoundAnalysis)

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7722.MarshalByRefObjectPermanent":
        from mastapy._private import _7722

        return self.__parent__._cast(_7722.MarshalByRefObjectPermanent)

    @property
    def compound_steady_state_synchronous_response_at_a_speed_analysis(
        self: "CastSelf",
    ) -> "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis":
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
class CompoundSteadyStateSynchronousResponseAtASpeedAnalysis(_2703.CompoundAnalysis):
    """CompoundSteadyStateSynchronousResponseAtASpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CompoundSteadyStateSynchronousResponseAtASpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CompoundSteadyStateSynchronousResponseAtASpeedAnalysis
        """
        return _Cast_CompoundSteadyStateSynchronousResponseAtASpeedAnalysis(self)
