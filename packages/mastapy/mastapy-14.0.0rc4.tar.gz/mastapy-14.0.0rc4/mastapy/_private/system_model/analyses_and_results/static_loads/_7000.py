"""CouplingHalfLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7074

_COUPLING_HALF_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "CouplingHalfLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6981,
        _6985,
        _6987,
        _7004,
        _7078,
        _7080,
        _7090,
        _7097,
        _7107,
        _7117,
        _7119,
        _7120,
        _7124,
        _7125,
    )
    from mastapy._private.system_model.part_model.couplings import _2643

    Self = TypeVar("Self", bound="CouplingHalfLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="CouplingHalfLoadCase._Cast_CouplingHalfLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfLoadCase:
    """Special nested class for casting CouplingHalfLoadCase to subclasses."""

    __parent__: "CouplingHalfLoadCase"

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7074.MountableComponentLoadCase":
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
    def clutch_half_load_case(self: "CastSelf") -> "_6981.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6981,
        )

        return self.__parent__._cast(_6981.ClutchHalfLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_6987.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6987,
        )

        return self.__parent__._cast(_6987.ConceptCouplingHalfLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7004.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7004,
        )

        return self.__parent__._cast(_7004.CVTPulleyLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7080.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7080,
        )

        return self.__parent__._cast(_7080.PartToPartShearCouplingHalfLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7090.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7090,
        )

        return self.__parent__._cast(_7090.PulleyLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7097.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7097,
        )

        return self.__parent__._cast(_7097.RollingRingLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7107.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7107,
        )

        return self.__parent__._cast(_7107.SpringDamperHalfLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7117.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7117,
        )

        return self.__parent__._cast(_7117.SynchroniserHalfLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7119.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7119,
        )

        return self.__parent__._cast(_7119.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7120.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7120,
        )

        return self.__parent__._cast(_7120.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7124.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7124,
        )

        return self.__parent__._cast(_7124.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7125.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7125,
        )

        return self.__parent__._cast(_7125.TorqueConverterTurbineLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "CouplingHalfLoadCase":
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
class CouplingHalfLoadCase(_7074.MountableComponentLoadCase):
    """CouplingHalfLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2643.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalfLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfLoadCase
        """
        return _Cast_CouplingHalfLoadCase(self)
