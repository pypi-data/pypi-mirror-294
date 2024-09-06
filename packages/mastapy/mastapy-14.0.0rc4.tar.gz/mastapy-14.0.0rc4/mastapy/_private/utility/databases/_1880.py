"""DatabaseSettings"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility import _1643

_DATABASE_SETTINGS = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "DatabaseSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility import _1644
    from mastapy._private.utility.databases import _1878

    Self = TypeVar("Self", bound="DatabaseSettings")
    CastSelf = TypeVar("CastSelf", bound="DatabaseSettings._Cast_DatabaseSettings")


__docformat__ = "restructuredtext en"
__all__ = ("DatabaseSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DatabaseSettings:
    """Special nested class for casting DatabaseSettings to subclasses."""

    __parent__: "DatabaseSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1643.PerMachineSettings":
        return self.__parent__._cast(_1643.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1644.PersistentSingleton":
        from mastapy._private.utility import _1644

        return self.__parent__._cast(_1644.PersistentSingleton)

    @property
    def database_settings(self: "CastSelf") -> "DatabaseSettings":
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
class DatabaseSettings(_1643.PerMachineSettings):
    """DatabaseSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATABASE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_settings(self: "Self") -> "_1878.DatabaseConnectionSettings":
        """mastapy.utility.databases.DatabaseConnectionSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_DatabaseSettings":
        """Cast to another type.

        Returns:
            _Cast_DatabaseSettings
        """
        return _Cast_DatabaseSettings(self)
