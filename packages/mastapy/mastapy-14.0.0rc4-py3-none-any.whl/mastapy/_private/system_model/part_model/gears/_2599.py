"""PlanetaryGearSet"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2583

_PLANETARY_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import _2489, _2525, _2533
    from mastapy._private.system_model.part_model.gears import _2582, _2584, _2589

    Self = TypeVar("Self", bound="PlanetaryGearSet")
    CastSelf = TypeVar("CastSelf", bound="PlanetaryGearSet._Cast_PlanetaryGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryGearSet:
    """Special nested class for casting PlanetaryGearSet to subclasses."""

    __parent__: "PlanetaryGearSet"

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2583.CylindricalGearSet":
        return self.__parent__._cast(_2583.CylindricalGearSet)

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
    def planetary_gear_set(self: "CastSelf") -> "PlanetaryGearSet":
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
class PlanetaryGearSet(_2583.CylindricalGearSet):
    """PlanetaryGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def annuluses(self: "Self") -> "List[_2582.CylindricalGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Annuluses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planets(self: "Self") -> "List[_2584.CylindricalPlanetGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalPlanetGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def suns(self: "Self") -> "List[_2582.CylindricalGear]":
        """List[mastapy.system_model.part_model.gears.CylindricalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Suns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def add_annulus(self: "Self") -> "_2582.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear"""
        method_result = pythonnet_method_call(self.wrapped, "AddAnnulus")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def add_planet(self: "Self") -> "_2582.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear"""
        method_result = pythonnet_method_call(self.wrapped, "AddPlanet")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def add_sun(self: "Self") -> "_2582.CylindricalGear":
        """mastapy.system_model.part_model.gears.CylindricalGear"""
        method_result = pythonnet_method_call(self.wrapped, "AddSun")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def set_number_of_planets(self: "Self", amount: "int") -> None:
        """Method does not return.

        Args:
            amount (int)
        """
        amount = int(amount)
        pythonnet_method_call(
            self.wrapped, "SetNumberOfPlanets", amount if amount else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetaryGearSet":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryGearSet
        """
        return _Cast_PlanetaryGearSet(self)
