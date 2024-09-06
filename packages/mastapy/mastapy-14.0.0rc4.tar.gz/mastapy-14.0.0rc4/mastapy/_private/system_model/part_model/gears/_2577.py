"""BevelGearSet"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2571

_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import _2489, _2525, _2533
    from mastapy._private.system_model.part_model.gears import (
        _2573,
        _2581,
        _2589,
        _2601,
        _2603,
        _2605,
        _2611,
    )

    Self = TypeVar("Self", bound="BevelGearSet")
    CastSelf = TypeVar("CastSelf", bound="BevelGearSet._Cast_BevelGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearSet:
    """Special nested class for casting BevelGearSet to subclasses."""

    __parent__: "BevelGearSet"

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
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2573.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2573

        return self.__parent__._cast(_2573.BevelDifferentialGearSet)

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
    def bevel_gear_set(self: "CastSelf") -> "BevelGearSet":
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
class BevelGearSet(_2571.AGMAGleasonConicalGearSet):
    """BevelGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearSet":
        """Cast to another type.

        Returns:
            _Cast_BevelGearSet
        """
        return _Cast_BevelGearSet(self)
