"""Vector6D"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility import _1574

_VECTOR_6D = python_net_import("SMT.MastaAPI.MathUtility", "Vector6D")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1562, _1573

    Self = TypeVar("Self", bound="Vector6D")
    CastSelf = TypeVar("CastSelf", bound="Vector6D._Cast_Vector6D")


__docformat__ = "restructuredtext en"
__all__ = ("Vector6D",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Vector6D:
    """Special nested class for casting Vector6D to subclasses."""

    __parent__: "Vector6D"

    @property
    def real_vector(self: "CastSelf") -> "_1574.RealVector":
        return self.__parent__._cast(_1574.RealVector)

    @property
    def real_matrix(self: "CastSelf") -> "_1573.RealMatrix":
        from mastapy._private.math_utility import _1573

        return self.__parent__._cast(_1573.RealMatrix)

    @property
    def generic_matrix(self: "CastSelf") -> "_1562.GenericMatrix":
        from mastapy._private.math_utility import _1562

        return self.__parent__._cast(_1562.GenericMatrix)

    @property
    def vector_6d(self: "CastSelf") -> "Vector6D":
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
class Vector6D(_1574.RealVector):
    """Vector6D

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VECTOR_6D

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_Vector6D":
        """Cast to another type.

        Returns:
            _Cast_Vector6D
        """
        return _Cast_Vector6D(self)
