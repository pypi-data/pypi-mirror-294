"""LoadedCylindricalRollerBearingDutyCycle"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2077

_LOADED_CYLINDRICAL_ROLLER_BEARING_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedCylindricalRollerBearingDutyCycle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2002, _2010, _2013

    Self = TypeVar("Self", bound="LoadedCylindricalRollerBearingDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedCylindricalRollerBearingDutyCycle._Cast_LoadedCylindricalRollerBearingDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedCylindricalRollerBearingDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedCylindricalRollerBearingDutyCycle:
    """Special nested class for casting LoadedCylindricalRollerBearingDutyCycle to subclasses."""

    __parent__: "LoadedCylindricalRollerBearingDutyCycle"

    @property
    def loaded_non_barrel_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2077.LoadedNonBarrelRollerBearingDutyCycle":
        return self.__parent__._cast(_2077.LoadedNonBarrelRollerBearingDutyCycle)

    @property
    def loaded_rolling_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2013.LoadedRollingBearingDutyCycle":
        from mastapy._private.bearings.bearing_results import _2013

        return self.__parent__._cast(_2013.LoadedRollingBearingDutyCycle)

    @property
    def loaded_non_linear_bearing_duty_cycle_results(
        self: "CastSelf",
    ) -> "_2010.LoadedNonLinearBearingDutyCycleResults":
        from mastapy._private.bearings.bearing_results import _2010

        return self.__parent__._cast(_2010.LoadedNonLinearBearingDutyCycleResults)

    @property
    def loaded_bearing_duty_cycle(self: "CastSelf") -> "_2002.LoadedBearingDutyCycle":
        from mastapy._private.bearings.bearing_results import _2002

        return self.__parent__._cast(_2002.LoadedBearingDutyCycle)

    @property
    def loaded_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "LoadedCylindricalRollerBearingDutyCycle":
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
class LoadedCylindricalRollerBearingDutyCycle(
    _2077.LoadedNonBarrelRollerBearingDutyCycle
):
    """LoadedCylindricalRollerBearingDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_CYLINDRICAL_ROLLER_BEARING_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def permissible_continuous_axial_load_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleContinuousAxialLoadSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedCylindricalRollerBearingDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_LoadedCylindricalRollerBearingDutyCycle
        """
        return _Cast_LoadedCylindricalRollerBearingDutyCycle(self)
