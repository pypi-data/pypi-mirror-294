"""CycloidalDiscAxialLeftSocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2334

_CYCLOIDAL_DISC_AXIAL_LEFT_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscAxialLeftSocket",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2330,
        _2348,
        _2350,
    )

    Self = TypeVar("Self", bound="CycloidalDiscAxialLeftSocket")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscAxialLeftSocket._Cast_CycloidalDiscAxialLeftSocket",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscAxialLeftSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscAxialLeftSocket:
    """Special nested class for casting CycloidalDiscAxialLeftSocket to subclasses."""

    __parent__: "CycloidalDiscAxialLeftSocket"

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2334.InnerShaftSocketBase":
        return self.__parent__._cast(_2334.InnerShaftSocketBase)

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
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "CycloidalDiscAxialLeftSocket":
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
class CycloidalDiscAxialLeftSocket(_2334.InnerShaftSocketBase):
    """CycloidalDiscAxialLeftSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_AXIAL_LEFT_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscAxialLeftSocket":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscAxialLeftSocket
        """
        return _Cast_CycloidalDiscAxialLeftSocket(self)
