"""ClutchLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7001

_CLUTCH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ClutchLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6954,
        _7078,
        _7102,
    )
    from mastapy._private.system_model.part_model.couplings import _2636

    Self = TypeVar("Self", bound="ClutchLoadCase")
    CastSelf = TypeVar("CastSelf", bound="ClutchLoadCase._Cast_ClutchLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("ClutchLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClutchLoadCase:
    """Special nested class for casting ClutchLoadCase to subclasses."""

    __parent__: "ClutchLoadCase"

    @property
    def coupling_load_case(self: "CastSelf") -> "_7001.CouplingLoadCase":
        return self.__parent__._cast(_7001.CouplingLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7102.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7102,
        )

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
    def clutch_load_case(self: "CastSelf") -> "ClutchLoadCase":
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
class ClutchLoadCase(_7001.CouplingLoadCase):
    """ClutchLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2636.Clutch":
        """mastapy.system_model.part_model.couplings.Clutch

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ClutchLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ClutchLoadCase
        """
        return _Cast_ClutchLoadCase(self)
