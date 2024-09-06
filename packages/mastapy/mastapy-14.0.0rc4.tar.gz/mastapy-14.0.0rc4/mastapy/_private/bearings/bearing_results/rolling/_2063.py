"""LoadedCylindricalRollerBearingResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2078

_LOADED_CYLINDRICAL_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedCylindricalRollerBearingResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1928
    from mastapy._private.bearings.bearing_results import _2003, _2008, _2011
    from mastapy._private.bearings.bearing_results.rolling import (
        _2075,
        _2083,
        _2087,
        _2118,
    )

    Self = TypeVar("Self", bound="LoadedCylindricalRollerBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedCylindricalRollerBearingResults._Cast_LoadedCylindricalRollerBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedCylindricalRollerBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedCylindricalRollerBearingResults:
    """Special nested class for casting LoadedCylindricalRollerBearingResults to subclasses."""

    __parent__: "LoadedCylindricalRollerBearingResults"

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2078.LoadedNonBarrelRollerBearingResults":
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
    ) -> "_2075.LoadedNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2075

        return self.__parent__._cast(_2075.LoadedNeedleRollerBearingResults)

    @property
    def loaded_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "LoadedCylindricalRollerBearingResults":
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
class LoadedCylindricalRollerBearingResults(_2078.LoadedNonBarrelRollerBearingResults):
    """LoadedCylindricalRollerBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_CYLINDRICAL_ROLLER_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def permissible_continuous_axial_load(
        self: "Self",
    ) -> "_2118.PermissibleContinuousAxialLoadResults":
        """mastapy.bearings.bearing_results.rolling.PermissibleContinuousAxialLoadResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleContinuousAxialLoad")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedCylindricalRollerBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedCylindricalRollerBearingResults
        """
        return _Cast_LoadedCylindricalRollerBearingResults(self)
