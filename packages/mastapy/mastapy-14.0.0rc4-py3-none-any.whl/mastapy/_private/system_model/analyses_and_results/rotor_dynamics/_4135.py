"""ShaftModalComplexShapeAtStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4133

_SHAFT_MODAL_COMPLEX_SHAPE_AT_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.RotorDynamics",
    "ShaftModalComplexShapeAtStiffness",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4131

    Self = TypeVar("Self", bound="ShaftModalComplexShapeAtStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftModalComplexShapeAtStiffness._Cast_ShaftModalComplexShapeAtStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftModalComplexShapeAtStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftModalComplexShapeAtStiffness:
    """Special nested class for casting ShaftModalComplexShapeAtStiffness to subclasses."""

    __parent__: "ShaftModalComplexShapeAtStiffness"

    @property
    def shaft_modal_complex_shape(self: "CastSelf") -> "_4133.ShaftModalComplexShape":
        return self.__parent__._cast(_4133.ShaftModalComplexShape)

    @property
    def shaft_complex_shape(self: "CastSelf") -> "_4131.ShaftComplexShape":
        pass

        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4131,
        )

        return self.__parent__._cast(_4131.ShaftComplexShape)

    @property
    def shaft_modal_complex_shape_at_stiffness(
        self: "CastSelf",
    ) -> "ShaftModalComplexShapeAtStiffness":
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
class ShaftModalComplexShapeAtStiffness(_4133.ShaftModalComplexShape):
    """ShaftModalComplexShapeAtStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_MODAL_COMPLEX_SHAPE_AT_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftModalComplexShapeAtStiffness":
        """Cast to another type.

        Returns:
            _Cast_ShaftModalComplexShapeAtStiffness
        """
        return _Cast_ShaftModalComplexShapeAtStiffness(self)
