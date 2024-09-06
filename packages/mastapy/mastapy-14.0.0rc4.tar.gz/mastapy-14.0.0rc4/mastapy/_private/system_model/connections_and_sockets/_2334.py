"""InnerShaftSocketBase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2348

_INNER_SHAFT_SOCKET_BASE = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "InnerShaftSocketBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2330,
        _2333,
        _2350,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2387,
        _2390,
    )

    Self = TypeVar("Self", bound="InnerShaftSocketBase")
    CastSelf = TypeVar(
        "CastSelf", bound="InnerShaftSocketBase._Cast_InnerShaftSocketBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("InnerShaftSocketBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InnerShaftSocketBase:
    """Special nested class for casting InnerShaftSocketBase to subclasses."""

    __parent__: "InnerShaftSocketBase"

    @property
    def shaft_socket(self: "CastSelf") -> "_2348.ShaftSocket":
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
    def inner_shaft_socket(self: "CastSelf") -> "_2333.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2333

        return self.__parent__._cast(_2333.InnerShaftSocket)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2387.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2387,
        )

        return self.__parent__._cast(_2387.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2390.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2390,
        )

        return self.__parent__._cast(_2390.CycloidalDiscInnerSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "InnerShaftSocketBase":
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
class InnerShaftSocketBase(_2348.ShaftSocket):
    """InnerShaftSocketBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INNER_SHAFT_SOCKET_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_InnerShaftSocketBase":
        """Cast to another type.

        Returns:
            _Cast_InnerShaftSocketBase
        """
        return _Cast_InnerShaftSocketBase(self)
