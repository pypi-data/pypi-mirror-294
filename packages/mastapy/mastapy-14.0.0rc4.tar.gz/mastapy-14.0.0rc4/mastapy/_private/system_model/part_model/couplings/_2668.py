"""SynchroniserPart"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.couplings import _2643

_SYNCHRONISER_PART = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import _2499, _2521, _2525
    from mastapy._private.system_model.part_model.couplings import _2667, _2669

    Self = TypeVar("Self", bound="SynchroniserPart")
    CastSelf = TypeVar("CastSelf", bound="SynchroniserPart._Cast_SynchroniserPart")


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserPart",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserPart:
    """Special nested class for casting SynchroniserPart to subclasses."""

    __parent__: "SynchroniserPart"

    @property
    def coupling_half(self: "CastSelf") -> "_2643.CouplingHalf":
        return self.__parent__._cast(_2643.CouplingHalf)

    @property
    def mountable_component(self: "CastSelf") -> "_2521.MountableComponent":
        from mastapy._private.system_model.part_model import _2521

        return self.__parent__._cast(_2521.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2499.Component":
        from mastapy._private.system_model.part_model import _2499

        return self.__parent__._cast(_2499.Component)

    @property
    def part(self: "CastSelf") -> "_2525.Part":
        from mastapy._private.system_model.part_model import _2525

        return self.__parent__._cast(_2525.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2257.DesignEntity":
        from mastapy._private.system_model import _2257

        return self.__parent__._cast(_2257.DesignEntity)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2667.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2667

        return self.__parent__._cast(_2667.SynchroniserHalf)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2669.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2669

        return self.__parent__._cast(_2669.SynchroniserSleeve)

    @property
    def synchroniser_part(self: "CastSelf") -> "SynchroniserPart":
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
class SynchroniserPart(_2643.CouplingHalf):
    """SynchroniserPart

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_PART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SynchroniserPart":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserPart
        """
        return _Cast_SynchroniserPart(self)
