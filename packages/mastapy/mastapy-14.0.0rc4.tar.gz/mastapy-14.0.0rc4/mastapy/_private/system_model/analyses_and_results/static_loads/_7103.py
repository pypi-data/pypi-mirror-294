"""SpiralBevelGearLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _6975

_SPIRAL_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "SpiralBevelGearLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6961,
        _6985,
        _6992,
        _7038,
        _7074,
        _7078,
    )
    from mastapy._private.system_model.part_model.gears import _2600

    Self = TypeVar("Self", bound="SpiralBevelGearLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelGearLoadCase._Cast_SpiralBevelGearLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearLoadCase:
    """Special nested class for casting SpiralBevelGearLoadCase to subclasses."""

    __parent__: "SpiralBevelGearLoadCase"

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_6975.BevelGearLoadCase":
        return self.__parent__._cast(_6975.BevelGearLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_6961.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6961,
        )

        return self.__parent__._cast(_6961.AGMAGleasonConicalGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_6992.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6992,
        )

        return self.__parent__._cast(_6992.ConicalGearLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7038.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7038,
        )

        return self.__parent__._cast(_7038.GearLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7074.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7074,
        )

        return self.__parent__._cast(_7074.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6985.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6985,
        )

        return self.__parent__._cast(_6985.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7078.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7078,
        )

        return self.__parent__._cast(_7078.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2741.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2741

        return self.__parent__._cast(_2741.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2737.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2737

        return self.__parent__._cast(_2737.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2735.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.DesignEntityAnalysis)

    @property
    def spiral_bevel_gear_load_case(self: "CastSelf") -> "SpiralBevelGearLoadCase":
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
class SpiralBevelGearLoadCase(_6975.BevelGearLoadCase):
    """SpiralBevelGearLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2600.SpiralBevelGear":
        """mastapy.system_model.part_model.gears.SpiralBevelGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearLoadCase":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearLoadCase
        """
        return _Cast_SpiralBevelGearLoadCase(self)
