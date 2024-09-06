"""LoadedDeepGrooveBallBearingResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2056

_LOADED_DEEP_GROOVE_BALL_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedDeepGrooveBallBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1928
    from mastapy._private.bearings.bearing_results import _2003, _2008, _2011
    from mastapy._private.bearings.bearing_results.rolling import _2087

    Self = TypeVar("Self", bound="LoadedDeepGrooveBallBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedDeepGrooveBallBearingResults._Cast_LoadedDeepGrooveBallBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedDeepGrooveBallBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedDeepGrooveBallBearingResults:
    """Special nested class for casting LoadedDeepGrooveBallBearingResults to subclasses."""

    __parent__: "LoadedDeepGrooveBallBearingResults"

    @property
    def loaded_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2056.LoadedBallBearingResults":
        return self.__parent__._cast(_2056.LoadedBallBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2087.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2087

        return self.__parent__._cast(_2087.LoadedRollingBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2008.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2008

        return self.__parent__._cast(_2008.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2011.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2011

        return self.__parent__._cast(_2011.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2003.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2003

        return self.__parent__._cast(_2003.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_1928.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _1928

        return self.__parent__._cast(_1928.BearingLoadCaseResultsLightweight)

    @property
    def loaded_deep_groove_ball_bearing_results(
        self: "CastSelf",
    ) -> "LoadedDeepGrooveBallBearingResults":
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
class LoadedDeepGrooveBallBearingResults(_2056.LoadedBallBearingResults):
    """LoadedDeepGrooveBallBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_DEEP_GROOVE_BALL_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedDeepGrooveBallBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedDeepGrooveBallBearingResults
        """
        return _Cast_LoadedDeepGrooveBallBearingResults(self)
