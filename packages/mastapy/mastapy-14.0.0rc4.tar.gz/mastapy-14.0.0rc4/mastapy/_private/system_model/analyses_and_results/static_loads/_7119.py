"""SynchroniserPartLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7000

_SYNCHRONISER_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SynchroniserPartLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6985,
        _7074,
        _7078,
        _7117,
        _7120,
    )
    from mastapy._private.system_model.part_model.couplings import _2668

    Self = TypeVar("Self", bound="SynchroniserPartLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="SynchroniserPartLoadCase._Cast_SynchroniserPartLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserPartLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserPartLoadCase:
    """Special nested class for casting SynchroniserPartLoadCase to subclasses."""

    __parent__: "SynchroniserPartLoadCase"

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7000.CouplingHalfLoadCase":
        return self.__parent__._cast(_7000.CouplingHalfLoadCase)

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
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7117.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7117,
        )

        return self.__parent__._cast(_7117.SynchroniserHalfLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7120.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7120,
        )

        return self.__parent__._cast(_7120.SynchroniserSleeveLoadCase)

    @property
    def synchroniser_part_load_case(self: "CastSelf") -> "SynchroniserPartLoadCase":
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
class SynchroniserPartLoadCase(_7000.CouplingHalfLoadCase):
    """SynchroniserPartLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_PART_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2668.SynchroniserPart":
        """mastapy.system_model.part_model.couplings.SynchroniserPart

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SynchroniserPartLoadCase":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserPartLoadCase
        """
        return _Cast_SynchroniserPartLoadCase(self)
