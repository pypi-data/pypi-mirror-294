"""OuterShaftSocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2340

_OUTER_SHAFT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "OuterShaftSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2330,
        _2348,
        _2350,
    )

    Self = TypeVar("Self", bound="OuterShaftSocket")
    CastSelf = TypeVar("CastSelf", bound="OuterShaftSocket._Cast_OuterShaftSocket")


__docformat__ = "restructuredtext en"
__all__ = ("OuterShaftSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OuterShaftSocket:
    """Special nested class for casting OuterShaftSocket to subclasses."""

    __parent__: "OuterShaftSocket"

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2340.OuterShaftSocketBase":
        return self.__parent__._cast(_2340.OuterShaftSocketBase)

    @property
    def shaft_socket(self: "CastSelf") -> "_2348.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2348

        return self.__parent__._cast(_2348.ShaftSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2330.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2330

        return self.__parent__._cast(_2330.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2350.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2350

        return self.__parent__._cast(_2350.Socket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "OuterShaftSocket":
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
class OuterShaftSocket(_2340.OuterShaftSocketBase):
    """OuterShaftSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OUTER_SHAFT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_OuterShaftSocket":
        """Cast to another type.

        Returns:
            _Cast_OuterShaftSocket
        """
        return _Cast_OuterShaftSocket(self)
