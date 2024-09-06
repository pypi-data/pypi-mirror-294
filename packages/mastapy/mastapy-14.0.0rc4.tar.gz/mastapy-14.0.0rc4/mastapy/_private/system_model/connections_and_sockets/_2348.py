"""ShaftSocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2330

_SHAFT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "ShaftSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2333,
        _2334,
        _2339,
        _2340,
        _2350,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2387,
        _2388,
        _2390,
    )

    Self = TypeVar("Self", bound="ShaftSocket")
    CastSelf = TypeVar("CastSelf", bound="ShaftSocket._Cast_ShaftSocket")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSocket:
    """Special nested class for casting ShaftSocket to subclasses."""

    __parent__: "ShaftSocket"

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2330.CylindricalSocket":
        return self.__parent__._cast(_2330.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2350.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2350

        return self.__parent__._cast(_2350.Socket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2333.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2333

        return self.__parent__._cast(_2333.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2334.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2334

        return self.__parent__._cast(_2334.InnerShaftSocketBase)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2339.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2339

        return self.__parent__._cast(_2339.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2340.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2340

        return self.__parent__._cast(_2340.OuterShaftSocketBase)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2387.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2387,
        )

        return self.__parent__._cast(_2387.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2388.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2388,
        )

        return self.__parent__._cast(_2388.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2390.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2390,
        )

        return self.__parent__._cast(_2390.CycloidalDiscInnerSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "ShaftSocket":
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
class ShaftSocket(_2330.CylindricalSocket):
    """ShaftSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSocket":
        """Cast to another type.

        Returns:
            _Cast_ShaftSocket
        """
        return _Cast_ShaftSocket(self)
