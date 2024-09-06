"""HypoidGearSet"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2571

_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.hypoid import _1013
    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.connections_and_sockets.gears import _2369
    from mastapy._private.system_model.part_model import _2489, _2525, _2533
    from mastapy._private.system_model.part_model.gears import _2581, _2589, _2591

    Self = TypeVar("Self", bound="HypoidGearSet")
    CastSelf = TypeVar("CastSelf", bound="HypoidGearSet._Cast_HypoidGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearSet:
    """Special nested class for casting HypoidGearSet to subclasses."""

    __parent__: "HypoidGearSet"

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2571.AGMAGleasonConicalGearSet":
        return self.__parent__._cast(_2571.AGMAGleasonConicalGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2581.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2581

        return self.__parent__._cast(_2581.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2589.GearSet":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2533.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2533

        return self.__parent__._cast(_2533.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2489.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2489

        return self.__parent__._cast(_2489.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2525.Part":
        from mastapy._private.system_model.part_model import _2525

        return self.__parent__._cast(_2525.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2257.DesignEntity":
        from mastapy._private.system_model import _2257

        return self.__parent__._cast(_2257.DesignEntity)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "HypoidGearSet":
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
class HypoidGearSet(_2571.AGMAGleasonConicalGearSet):
    """HypoidGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def conical_gear_set_design(self: "Self") -> "_1013.HypoidGearSetDesign":
        """mastapy.gears.gear_designs.hypoid.HypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def hypoid_gear_set_design(self: "Self") -> "_1013.HypoidGearSetDesign":
        """mastapy.gears.gear_designs.hypoid.HypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def hypoid_gears(self: "Self") -> "List[_2591.HypoidGear]":
        """List[mastapy.system_model.part_model.gears.HypoidGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def hypoid_meshes(self: "Self") -> "List[_2369.HypoidGearMesh]":
        """List[mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidGearSet":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearSet
        """
        return _Cast_HypoidGearSet(self)
