"""PlanetarySocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.connections_and_sockets import _2343

_PLANETARY_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PlanetarySocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import _2330, _2350

    Self = TypeVar("Self", bound="PlanetarySocket")
    CastSelf = TypeVar("CastSelf", bound="PlanetarySocket._Cast_PlanetarySocket")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetarySocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetarySocket:
    """Special nested class for casting PlanetarySocket to subclasses."""

    __parent__: "PlanetarySocket"

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2343.PlanetarySocketBase":
        return self.__parent__._cast(_2343.PlanetarySocketBase)

    @property
    def cylindrical_socket(self: "CastSelf") -> "_2330.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2330

        return self.__parent__._cast(_2330.CylindricalSocket)

    @property
    def socket(self: "CastSelf") -> "_2350.Socket":
        from mastapy._private.system_model.connections_and_sockets import _2350

        return self.__parent__._cast(_2350.Socket)

    @property
    def planetary_socket(self: "CastSelf") -> "PlanetarySocket":
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
class PlanetarySocket(_2343.PlanetarySocketBase):
    """PlanetarySocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def planet_tip_clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetTipClearance")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetarySocket":
        """Cast to another type.

        Returns:
            _Cast_PlanetarySocket
        """
        return _Cast_PlanetarySocket(self)
