"""SuperchargerRotorSetDatabase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import _2620
from mastapy._private.utility.databases import _1881

_SUPERCHARGER_ROTOR_SET_DATABASE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet",
    "SuperchargerRotorSetDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1877, _1884

    Self = TypeVar("Self", bound="SuperchargerRotorSetDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SuperchargerRotorSetDatabase._Cast_SuperchargerRotorSetDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SuperchargerRotorSetDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SuperchargerRotorSetDatabase:
    """Special nested class for casting SuperchargerRotorSetDatabase to subclasses."""

    __parent__: "SuperchargerRotorSetDatabase"

    @property
    def named_database(self: "CastSelf") -> "_1881.NamedDatabase":
        return self.__parent__._cast(_1881.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_1884.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _1884

        return self.__parent__._cast(_1884.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_1877.Database":
        pass

        from mastapy._private.utility.databases import _1877

        return self.__parent__._cast(_1877.Database)

    @property
    def supercharger_rotor_set_database(
        self: "CastSelf",
    ) -> "SuperchargerRotorSetDatabase":
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
class SuperchargerRotorSetDatabase(_1881.NamedDatabase[_2620.SuperchargerRotorSet]):
    """SuperchargerRotorSetDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SUPERCHARGER_ROTOR_SET_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SuperchargerRotorSetDatabase":
        """Cast to another type.

        Returns:
            _Cast_SuperchargerRotorSetDatabase
        """
        return _Cast_SuperchargerRotorSetDatabase(self)
