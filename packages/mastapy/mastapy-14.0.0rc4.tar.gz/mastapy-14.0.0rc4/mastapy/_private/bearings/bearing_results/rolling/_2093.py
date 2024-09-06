"""LoadedSphericalRollerBearingElement"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2082

_LOADED_SPHERICAL_ROLLER_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedSphericalRollerBearingElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2068, _2092, _2099

    Self = TypeVar("Self", bound="LoadedSphericalRollerBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedSphericalRollerBearingElement._Cast_LoadedSphericalRollerBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedSphericalRollerBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedSphericalRollerBearingElement:
    """Special nested class for casting LoadedSphericalRollerBearingElement to subclasses."""

    __parent__: "LoadedSphericalRollerBearingElement"

    @property
    def loaded_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2082.LoadedRollerBearingElement":
        return self.__parent__._cast(_2082.LoadedRollerBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2068.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2068

        return self.__parent__._cast(_2068.LoadedElement)

    @property
    def loaded_spherical_radial_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2092.LoadedSphericalRadialRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2092

        return self.__parent__._cast(_2092.LoadedSphericalRadialRollerBearingElement)

    @property
    def loaded_spherical_thrust_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2099.LoadedSphericalThrustRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2099

        return self.__parent__._cast(_2099.LoadedSphericalThrustRollerBearingElement)

    @property
    def loaded_spherical_roller_bearing_element(
        self: "CastSelf",
    ) -> "LoadedSphericalRollerBearingElement":
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
class LoadedSphericalRollerBearingElement(_2082.LoadedRollerBearingElement):
    """LoadedSphericalRollerBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_SPHERICAL_ROLLER_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedSphericalRollerBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedSphericalRollerBearingElement
        """
        return _Cast_LoadedSphericalRollerBearingElement(self)
