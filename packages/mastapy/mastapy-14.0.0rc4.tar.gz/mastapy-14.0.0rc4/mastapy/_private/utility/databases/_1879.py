"""DatabaseKey"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_DATABASE_KEY = python_net_import("SMT.MastaAPI.Utility.Databases", "DatabaseKey")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1947
    from mastapy._private.utility.databases import _1883
    from mastapy._private.utility.report import _1819
    from mastapy._private.utility.scripting import _1791

    Self = TypeVar("Self", bound="DatabaseKey")
    CastSelf = TypeVar("CastSelf", bound="DatabaseKey._Cast_DatabaseKey")


__docformat__ = "restructuredtext en"
__all__ = ("DatabaseKey",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DatabaseKey:
    """Special nested class for casting DatabaseKey to subclasses."""

    __parent__: "DatabaseKey"

    @property
    def user_defined_property_key(self: "CastSelf") -> "_1791.UserDefinedPropertyKey":
        from mastapy._private.utility.scripting import _1791

        return self.__parent__._cast(_1791.UserDefinedPropertyKey)

    @property
    def custom_report_key(self: "CastSelf") -> "_1819.CustomReportKey":
        from mastapy._private.utility.report import _1819

        return self.__parent__._cast(_1819.CustomReportKey)

    @property
    def named_key(self: "CastSelf") -> "_1883.NamedKey":
        from mastapy._private.utility.databases import _1883

        return self.__parent__._cast(_1883.NamedKey)

    @property
    def rolling_bearing_key(self: "CastSelf") -> "_1947.RollingBearingKey":
        from mastapy._private.bearings import _1947

        return self.__parent__._cast(_1947.RollingBearingKey)

    @property
    def database_key(self: "CastSelf") -> "DatabaseKey":
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
class DatabaseKey(_0.APIBase):
    """DatabaseKey

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATABASE_KEY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DatabaseKey":
        """Cast to another type.

        Returns:
            _Cast_DatabaseKey
        """
        return _Cast_DatabaseKey(self)
