"""AbstractShaftToMountableComponentConnection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.connections_and_sockets import _2326

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "AbstractShaftToMountableComponentConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.connections_and_sockets import (
        _2323,
        _2341,
        _2349,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2389,
        _2392,
    )
    from mastapy._private.system_model.part_model import _2490, _2521

    Self = TypeVar("Self", bound="AbstractShaftToMountableComponentConnection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnection._Cast_AbstractShaftToMountableComponentConnection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnection:
    """Special nested class for casting AbstractShaftToMountableComponentConnection to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnection"

    @property
    def connection(self: "CastSelf") -> "_2326.Connection":
        return self.__parent__._cast(_2326.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2257.DesignEntity":
        from mastapy._private.system_model import _2257

        return self.__parent__._cast(_2257.DesignEntity)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2323.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2323

        return self.__parent__._cast(_2323.CoaxialConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2341.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2341

        return self.__parent__._cast(_2341.PlanetaryConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2349.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2349

        return self.__parent__._cast(_2349.ShaftToMountableComponentConnection)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2389.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2389,
        )

        return self.__parent__._cast(_2389.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2392.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2392,
        )

        return self.__parent__._cast(_2392.CycloidalDiscPlanetaryBearingConnection)

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnection":
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
class AbstractShaftToMountableComponentConnection(_2326.Connection):
    """AbstractShaftToMountableComponentConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mountable_component(self: "Self") -> "_2521.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MountableComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft(self: "Self") -> "_2490.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftToMountableComponentConnection":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnection
        """
        return _Cast_AbstractShaftToMountableComponentConnection(self)
