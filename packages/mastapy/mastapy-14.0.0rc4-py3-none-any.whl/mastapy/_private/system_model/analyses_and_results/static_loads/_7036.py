"""FlexiblePinAssemblyLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7102

_FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "FlexiblePinAssemblyLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6954,
        _7078,
    )
    from mastapy._private.system_model.part_model import _2509
    from mastapy._private.utility import _1638

    Self = TypeVar("Self", bound="FlexiblePinAssemblyLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FlexiblePinAssemblyLoadCase._Cast_FlexiblePinAssemblyLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAssemblyLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAssemblyLoadCase:
    """Special nested class for casting FlexiblePinAssemblyLoadCase to subclasses."""

    __parent__: "FlexiblePinAssemblyLoadCase"

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7102.SpecialisedAssemblyLoadCase":
        return self.__parent__._cast(_7102.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6954.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6954,
        )

        return self.__parent__._cast(_6954.AbstractAssemblyLoadCase)

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
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "FlexiblePinAssemblyLoadCase":
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
class FlexiblePinAssemblyLoadCase(_7102.SpecialisedAssemblyLoadCase):
    """FlexiblePinAssemblyLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLEXIBLE_PIN_ASSEMBLY_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def include_inner_race_distortion_for_flexible_pin_spindle(
        self: "Self",
    ) -> "_1638.LoadCaseOverrideOption":
        """mastapy.utility.LoadCaseOverrideOption"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeInnerRaceDistortionForFlexiblePinSpindle"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.LoadCaseOverrideOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility._1638", "LoadCaseOverrideOption"
        )(value)

    @include_inner_race_distortion_for_flexible_pin_spindle.setter
    @enforce_parameter_types
    def include_inner_race_distortion_for_flexible_pin_spindle(
        self: "Self", value: "_1638.LoadCaseOverrideOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.LoadCaseOverrideOption"
        )
        pythonnet_property_set(
            self.wrapped, "IncludeInnerRaceDistortionForFlexiblePinSpindle", value
        )

    @property
    def assembly_design(self: "Self") -> "_2509.FlexiblePinAssembly":
        """mastapy.system_model.part_model.FlexiblePinAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FlexiblePinAssemblyLoadCase":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAssemblyLoadCase
        """
        return _Cast_FlexiblePinAssemblyLoadCase(self)
