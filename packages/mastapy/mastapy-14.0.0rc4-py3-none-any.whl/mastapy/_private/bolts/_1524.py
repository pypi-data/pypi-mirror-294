"""ClampedSectionMaterialDatabase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bolts import _1514, _1515

_CLAMPED_SECTION_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Bolts", "ClampedSectionMaterialDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _1877, _1881, _1884

    Self = TypeVar("Self", bound="ClampedSectionMaterialDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ClampedSectionMaterialDatabase._Cast_ClampedSectionMaterialDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ClampedSectionMaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClampedSectionMaterialDatabase:
    """Special nested class for casting ClampedSectionMaterialDatabase to subclasses."""

    __parent__: "ClampedSectionMaterialDatabase"

    @property
    def bolted_joint_material_database(
        self: "CastSelf",
    ) -> "_1515.BoltedJointMaterialDatabase":
        return self.__parent__._cast(_1515.BoltedJointMaterialDatabase)

    @property
    def named_database(self: "CastSelf") -> "_1881.NamedDatabase":
        from mastapy._private.utility.databases import _1881

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
    def clamped_section_material_database(
        self: "CastSelf",
    ) -> "ClampedSectionMaterialDatabase":
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
class ClampedSectionMaterialDatabase(
    _1515.BoltedJointMaterialDatabase[_1514.BoltedJointMaterial]
):
    """ClampedSectionMaterialDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLAMPED_SECTION_MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ClampedSectionMaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_ClampedSectionMaterialDatabase
        """
        return _Cast_ClampedSectionMaterialDatabase(self)
