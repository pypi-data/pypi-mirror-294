"""TorqueConverterTurbine"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.couplings import _2643

_TORQUE_CONVERTER_TURBINE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import _2499, _2521, _2525

    Self = TypeVar("Self", bound="TorqueConverterTurbine")
    CastSelf = TypeVar(
        "CastSelf", bound="TorqueConverterTurbine._Cast_TorqueConverterTurbine"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterTurbine",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterTurbine:
    """Special nested class for casting TorqueConverterTurbine to subclasses."""

    __parent__: "TorqueConverterTurbine"

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
    def torque_converter_turbine(self: "CastSelf") -> "TorqueConverterTurbine":
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
class TorqueConverterTurbine(_2643.CouplingHalf):
    """TorqueConverterTurbine

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_TURBINE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_TorqueConverterTurbine":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterTurbine
        """
        return _Cast_TorqueConverterTurbine(self)
