"""LoadedNeedleRollerBearingRow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2064

_LOADED_NEEDLE_ROLLER_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedNeedleRollerBearingRow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import (
        _2075,
        _2079,
        _2084,
        _2088,
    )

    Self = TypeVar("Self", bound="LoadedNeedleRollerBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNeedleRollerBearingRow._Cast_LoadedNeedleRollerBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNeedleRollerBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNeedleRollerBearingRow:
    """Special nested class for casting LoadedNeedleRollerBearingRow to subclasses."""

    __parent__: "LoadedNeedleRollerBearingRow"

    @property
    def loaded_cylindrical_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2064.LoadedCylindricalRollerBearingRow":
        return self.__parent__._cast(_2064.LoadedCylindricalRollerBearingRow)

    @property
    def loaded_non_barrel_roller_bearing_row(
        self: "CastSelf",
    ) -> "_2079.LoadedNonBarrelRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2079

        return self.__parent__._cast(_2079.LoadedNonBarrelRollerBearingRow)

    @property
    def loaded_roller_bearing_row(self: "CastSelf") -> "_2084.LoadedRollerBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2084

        return self.__parent__._cast(_2084.LoadedRollerBearingRow)

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "_2088.LoadedRollingBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2088

        return self.__parent__._cast(_2088.LoadedRollingBearingRow)

    @property
    def loaded_needle_roller_bearing_row(
        self: "CastSelf",
    ) -> "LoadedNeedleRollerBearingRow":
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
class LoadedNeedleRollerBearingRow(_2064.LoadedCylindricalRollerBearingRow):
    """LoadedNeedleRollerBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NEEDLE_ROLLER_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cage_land_sliding_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CageLandSlidingPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def rolling_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def rolling_power_loss_traction_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RollingPowerLossTractionCoefficient"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def sliding_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def sliding_power_loss_traction_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingPowerLossTractionCoefficient"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def total_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_power_loss_traction_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalPowerLossTractionCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    def loaded_bearing(self: "Self") -> "_2075.LoadedNeedleRollerBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedNeedleRollerBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNeedleRollerBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedNeedleRollerBearingRow
        """
        return _Cast_LoadedNeedleRollerBearingRow(self)
