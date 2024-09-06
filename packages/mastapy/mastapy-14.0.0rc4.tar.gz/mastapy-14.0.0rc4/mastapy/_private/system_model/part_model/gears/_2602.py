"""StraightBevelDiffGear"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2576

_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.straight_bevel_diff import _991
    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import _2499, _2521, _2525
    from mastapy._private.system_model.part_model.gears import (
        _2570,
        _2580,
        _2587,
        _2606,
        _2607,
    )

    Self = TypeVar("Self", bound="StraightBevelDiffGear")
    CastSelf = TypeVar(
        "CastSelf", bound="StraightBevelDiffGear._Cast_StraightBevelDiffGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGear:
    """Special nested class for casting StraightBevelDiffGear to subclasses."""

    __parent__: "StraightBevelDiffGear"

    @property
    def bevel_gear(self: "CastSelf") -> "_2576.BevelGear":
        return self.__parent__._cast(_2576.BevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2570.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2570

        return self.__parent__._cast(_2570.AGMAGleasonConicalGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2580.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2580

        return self.__parent__._cast(_2580.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2587.Gear":
        from mastapy._private.system_model.part_model.gears import _2587

        return self.__parent__._cast(_2587.Gear)

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
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2606.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2607.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.StraightBevelSunGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "StraightBevelDiffGear":
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
class StraightBevelDiffGear(_2576.BevelGear):
    """StraightBevelDiffGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bevel_gear_design(self: "Self") -> "_991.StraightBevelDiffGearDesign":
        """mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def straight_bevel_diff_gear_design(
        self: "Self",
    ) -> "_991.StraightBevelDiffGearDesign":
        """mastapy.gears.gear_designs.straight_bevel_diff.StraightBevelDiffGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGear":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGear
        """
        return _Cast_StraightBevelDiffGear(self)
