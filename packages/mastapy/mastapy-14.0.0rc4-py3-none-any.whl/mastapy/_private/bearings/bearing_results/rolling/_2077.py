"""LoadedNonBarrelRollerBearingDutyCycle"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results import _2013

_LOADED_NON_BARREL_ROLLER_BEARING_DUTY_CYCLE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedNonBarrelRollerBearingDutyCycle",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2002, _2010
    from mastapy._private.bearings.bearing_results.rolling import _2046, _2061, _2100

    Self = TypeVar("Self", bound="LoadedNonBarrelRollerBearingDutyCycle")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedNonBarrelRollerBearingDutyCycle._Cast_LoadedNonBarrelRollerBearingDutyCycle",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedNonBarrelRollerBearingDutyCycle",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedNonBarrelRollerBearingDutyCycle:
    """Special nested class for casting LoadedNonBarrelRollerBearingDutyCycle to subclasses."""

    __parent__: "LoadedNonBarrelRollerBearingDutyCycle"

    @property
    def loaded_rolling_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2013.LoadedRollingBearingDutyCycle":
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
    def loaded_axial_thrust_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2046.LoadedAxialThrustCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2046

        return self.__parent__._cast(
            _2046.LoadedAxialThrustCylindricalRollerBearingDutyCycle
        )

    @property
    def loaded_cylindrical_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2061.LoadedCylindricalRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2061

        return self.__parent__._cast(_2061.LoadedCylindricalRollerBearingDutyCycle)

    @property
    def loaded_taper_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "_2100.LoadedTaperRollerBearingDutyCycle":
        from mastapy._private.bearings.bearing_results.rolling import _2100

        return self.__parent__._cast(_2100.LoadedTaperRollerBearingDutyCycle)

    @property
    def loaded_non_barrel_roller_bearing_duty_cycle(
        self: "CastSelf",
    ) -> "LoadedNonBarrelRollerBearingDutyCycle":
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
class LoadedNonBarrelRollerBearingDutyCycle(_2013.LoadedRollingBearingDutyCycle):
    """LoadedNonBarrelRollerBearingDutyCycle

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_NON_BARREL_ROLLER_BEARING_DUTY_CYCLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def smt_rib_stress_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SMTRibStressSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedNonBarrelRollerBearingDutyCycle":
        """Cast to another type.

        Returns:
            _Cast_LoadedNonBarrelRollerBearingDutyCycle
        """
        return _Cast_LoadedNonBarrelRollerBearingDutyCycle(self)
