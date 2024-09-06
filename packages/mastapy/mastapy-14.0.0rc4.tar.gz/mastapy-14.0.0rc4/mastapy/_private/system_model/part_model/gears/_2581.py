"""ConicalGearSet"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2589

_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1196
    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import _2489, _2525, _2533
    from mastapy._private.system_model.part_model.gears import (
        _2571,
        _2573,
        _2577,
        _2580,
        _2592,
        _2594,
        _2596,
        _2598,
        _2601,
        _2603,
        _2605,
        _2611,
    )

    Self = TypeVar("Self", bound="ConicalGearSet")
    CastSelf = TypeVar("CastSelf", bound="ConicalGearSet._Cast_ConicalGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSet:
    """Special nested class for casting ConicalGearSet to subclasses."""

    __parent__: "ConicalGearSet"

    @property
    def gear_set(self: "CastSelf") -> "_2589.GearSet":
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
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2571.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2571

        return self.__parent__._cast(_2571.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2573.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2573

        return self.__parent__._cast(_2573.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2577.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2577

        return self.__parent__._cast(_2577.BevelGearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2592.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2592

        return self.__parent__._cast(_2592.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2594.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2594

        return self.__parent__._cast(_2594.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2596.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2598.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2601.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2603.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2605.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.StraightBevelGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2611.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.ZerolBevelGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "ConicalGearSet":
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
class ConicalGearSet(_2589.GearSet):
    """ConicalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_gear_set_design(self: "Self") -> "_1196.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gear_set_design(self: "Self") -> "_1196.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gears(self: "Self") -> "List[_2580.ConicalGear]":
        """List[mastapy.system_model.part_model.gears.ConicalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSet":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSet
        """
        return _Cast_ConicalGearSet(self)
