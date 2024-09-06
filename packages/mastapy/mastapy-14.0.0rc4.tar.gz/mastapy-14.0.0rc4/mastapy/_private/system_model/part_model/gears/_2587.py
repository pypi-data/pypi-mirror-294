"""Gear"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2521

_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    from mastapy._private.gears.gear_designs import _973
    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import _2499, _2525
    from mastapy._private.system_model.part_model.gears import (
        _2570,
        _2572,
        _2574,
        _2575,
        _2576,
        _2578,
        _2580,
        _2582,
        _2584,
        _2585,
        _2589,
        _2591,
        _2593,
        _2595,
        _2597,
        _2600,
        _2602,
        _2604,
        _2606,
        _2607,
        _2608,
        _2610,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2539

    Self = TypeVar("Self", bound="Gear")
    CastSelf = TypeVar("CastSelf", bound="Gear._Cast_Gear")


__docformat__ = "restructuredtext en"
__all__ = ("Gear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Gear:
    """Special nested class for casting Gear to subclasses."""

    __parent__: "Gear"

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
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2570.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2570

        return self.__parent__._cast(_2570.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2572.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2572

        return self.__parent__._cast(_2572.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2574.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2574

        return self.__parent__._cast(_2574.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2575.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2575

        return self.__parent__._cast(_2575.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2576.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2576

        return self.__parent__._cast(_2576.BevelGear)

    @property
    def concept_gear(self: "CastSelf") -> "_2578.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2578

        return self.__parent__._cast(_2578.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2580.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2580

        return self.__parent__._cast(_2580.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2582.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2584.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2584

        return self.__parent__._cast(_2584.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2585.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.FaceGear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2591.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2593.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2593

        return self.__parent__._cast(_2593.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2595.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2597.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2600.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2600

        return self.__parent__._cast(_2600.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2602.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2602

        return self.__parent__._cast(_2602.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2604.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2606.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2607.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.StraightBevelSunGear)

    @property
    def worm_gear(self: "CastSelf") -> "_2608.WormGear":
        from mastapy._private.system_model.part_model.gears import _2608

        return self.__parent__._cast(_2608.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2610.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.ZerolBevelGear)

    @property
    def gear(self: "CastSelf") -> "Gear":
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
class Gear(_2521.MountableComponent):
    """Gear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cloned_from(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClonedFrom")

        if temp is None:
            return ""

        return temp

    @property
    def even_number_of_teeth_required(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "EvenNumberOfTeethRequired")

        if temp is None:
            return False

        return temp

    @even_number_of_teeth_required.setter
    @enforce_parameter_types
    def even_number_of_teeth_required(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvenNumberOfTeethRequired",
            bool(value) if value is not None else False,
        )

    @property
    def is_clone_gear(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsCloneGear")

        if temp is None:
            return False

        return temp

    @property
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    def maximum_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_teeth.setter
    @enforce_parameter_types
    def maximum_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def maximum_and_minimum_number_of_teeth_deviation(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumAndMinimumNumberOfTeethDeviation"
        )

        if temp is None:
            return None

        return temp

    @maximum_and_minimum_number_of_teeth_deviation.setter
    @enforce_parameter_types
    def maximum_and_minimum_number_of_teeth_deviation(
        self: "Self", value: "Optional[int]"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumAndMinimumNumberOfTeethDeviation", value
        )

    @property
    def minimum_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @minimum_number_of_teeth.setter
    @enforce_parameter_types
    def minimum_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def active_gear_design(self: "Self") -> "_973.GearDesign":
        """mastapy.gears.gear_designs.GearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    def gear_set(self: "Self") -> "_2589.GearSet":
        """mastapy.system_model.part_model.gears.GearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @number_of_teeth.setter
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    def shaft(self: "Self") -> "_2539.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def connect_to(self: "Self", other_gear: "Gear") -> None:
        """Method does not return.

        Args:
            other_gear (mastapy.system_model.part_model.gears.Gear)
        """
        pythonnet_method_call(
            self.wrapped, "ConnectTo", other_gear.wrapped if other_gear else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Gear":
        """Cast to another type.

        Returns:
            _Cast_Gear
        """
        return _Cast_Gear(self)
