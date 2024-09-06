"""VirtualComponent"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2521

_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import (
        _2499,
        _2517,
        _2518,
        _2525,
        _2528,
        _2529,
        _2534,
    )

    Self = TypeVar("Self", bound="VirtualComponent")
    CastSelf = TypeVar("CastSelf", bound="VirtualComponent._Cast_VirtualComponent")


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponent:
    """Special nested class for casting VirtualComponent to subclasses."""

    __parent__: "VirtualComponent"

    @property
    def mountable_component(self: "CastSelf") -> "_2521.MountableComponent":
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
    def mass_disc(self: "CastSelf") -> "_2517.MassDisc":
        from mastapy._private.system_model.part_model import _2517

        return self.__parent__._cast(_2517.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2518.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2518

        return self.__parent__._cast(_2518.MeasurementComponent)

    @property
    def point_load(self: "CastSelf") -> "_2528.PointLoad":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2529.PowerLoad":
        from mastapy._private.system_model.part_model import _2529

        return self.__parent__._cast(_2529.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2534.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2534

        return self.__parent__._cast(_2534.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "VirtualComponent":
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
class VirtualComponent(_2521.MountableComponent):
    """VirtualComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualComponent":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponent
        """
        return _Cast_VirtualComponent(self)
