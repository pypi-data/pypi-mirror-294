"""LoadedNeedleRollerBearingResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2063

_LOADED_NEEDLE_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedNeedleRollerBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1928
    from mastapy._private.bearings.bearing_results import _2003, _2008, _2011
    from mastapy._private.bearings.bearing_results.rolling import _2078, _2083, _2087

    Self = TypeVar("Self", bound="LoadedNeedleRollerBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNeedleRollerBearingResults._Cast_LoadedNeedleRollerBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNeedleRollerBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNeedleRollerBearingResults:
    """Special nested class for casting LoadedNeedleRollerBearingResults to subclasses."""

    __parent__: "LoadedNeedleRollerBearingResults"

    @property
    def loaded_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2063.LoadedCylindricalRollerBearingResults":
        return self.__parent__._cast(_2063.LoadedCylindricalRollerBearingResults)

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2078.LoadedNonBarrelRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2078

        return self.__parent__._cast(_2078.LoadedNonBarrelRollerBearingResults)

    @property
    def loaded_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2083.LoadedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2083

        return self.__parent__._cast(_2083.LoadedRollerBearingResults)

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
    def loaded_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "LoadedNeedleRollerBearingResults":
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
class LoadedNeedleRollerBearingResults(_2063.LoadedCylindricalRollerBearingResults):
    """LoadedNeedleRollerBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NEEDLE_ROLLER_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNeedleRollerBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedNeedleRollerBearingResults
        """
        return _Cast_LoadedNeedleRollerBearingResults(self)
