"""AGMAGleasonConicalGear"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2580

_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import _2499, _2521, _2525
    from mastapy._private.system_model.part_model.gears import (
        _2572,
        _2574,
        _2575,
        _2576,
        _2587,
        _2591,
        _2600,
        _2602,
        _2604,
        _2606,
        _2607,
        _2610,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGear")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGear:
    """Special nested class for casting AGMAGleasonConicalGear to subclasses."""

    __parent__: "AGMAGleasonConicalGear"

    @property
    def conical_gear(self: "CastSelf") -> "_2580.ConicalGear":
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
    def hypoid_gear(self: "CastSelf") -> "_2591.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.HypoidGear)

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
    def zerol_bevel_gear(self: "CastSelf") -> "_2610.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.ZerolBevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "AGMAGleasonConicalGear":
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
class AGMAGleasonConicalGear(_2580.ConicalGear):
    """AGMAGleasonConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGear":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGear
        """
        return _Cast_AGMAGleasonConicalGear(self)
