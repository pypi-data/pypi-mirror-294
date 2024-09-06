"""StraightBevelGearTeethSocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2358

_STRAIGHT_BEVEL_GEAR_TEETH_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "StraightBevelGearTeethSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2350
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2354,
        _2362,
        _2368,
    )

    Self = TypeVar("Self", bound="StraightBevelGearTeethSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearTeethSocket._Cast_StraightBevelGearTeethSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearTeethSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearTeethSocket:
    """Special nested class for casting StraightBevelGearTeethSocket to subclasses."""

    __parent__: "StraightBevelGearTeethSocket"

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2358.BevelGearTeethSocket":
        return self.__parent__._cast(_2358.BevelGearTeethSocket)

    @property
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2354.AGMAGleasonConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2354

        return self.__parent__._cast(_2354.AGMAGleasonConicalGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2362.ConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2362

        return self.__parent__._cast(_2362.ConicalGearTeethSocket)

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2368.GearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2368

        return self.__parent__._cast(_2368.GearTeethSocket)

    @property
    def socket(self: "CastSelf") -> "_2350.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2350

        return self.__parent__._cast(_2350.Socket)

    @property
    def straight_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "StraightBevelGearTeethSocket":
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
class StraightBevelGearTeethSocket(_2358.BevelGearTeethSocket):
    """StraightBevelGearTeethSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_TEETH_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelGearTeethSocket":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearTeethSocket
        """
        return _Cast_StraightBevelGearTeethSocket(self)
