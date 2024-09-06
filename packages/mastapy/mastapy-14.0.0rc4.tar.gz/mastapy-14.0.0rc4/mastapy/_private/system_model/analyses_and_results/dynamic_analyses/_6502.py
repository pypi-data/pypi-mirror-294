"""PartToPartShearCouplingHalfDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6455

_PART_TO_PART_SHEAR_COUPLING_HALF_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "PartToPartShearCouplingHalfDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7716,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6441,
        _6497,
        _6499,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7080
    from mastapy._private.system_model.part_model.couplings import _2648

    Self = TypeVar("Self", bound="PartToPartShearCouplingHalfDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartToPartShearCouplingHalfDynamicAnalysis._Cast_PartToPartShearCouplingHalfDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartToPartShearCouplingHalfDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartToPartShearCouplingHalfDynamicAnalysis:
    """Special nested class for casting PartToPartShearCouplingHalfDynamicAnalysis to subclasses."""

    __parent__: "PartToPartShearCouplingHalfDynamicAnalysis"

    @property
    def coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6455.CouplingHalfDynamicAnalysis":
        return self.__parent__._cast(_6455.CouplingHalfDynamicAnalysis)

    @property
    def mountable_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6497.MountableComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6497,
        )

        return self.__parent__._cast(_6497.MountableComponentDynamicAnalysis)

    @property
    def component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6441.ComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6441,
        )

        return self.__parent__._cast(_6441.ComponentDynamicAnalysis)

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6499.PartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6499,
        )

        return self.__parent__._cast(_6499.PartDynamicAnalysis)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7716.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7716,
        )

        return self.__parent__._cast(_7716.PartFEAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7714.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.PartAnalysisCase)

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
    def part_to_part_shear_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "PartToPartShearCouplingHalfDynamicAnalysis":
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
class PartToPartShearCouplingHalfDynamicAnalysis(_6455.CouplingHalfDynamicAnalysis):
    """PartToPartShearCouplingHalfDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_TO_PART_SHEAR_COUPLING_HALF_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2648.PartToPartShearCouplingHalf":
        """mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(
        self: "Self",
    ) -> "_7080.PartToPartShearCouplingHalfLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartToPartShearCouplingHalfDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartToPartShearCouplingHalfDynamicAnalysis
        """
        return _Cast_PartToPartShearCouplingHalfDynamicAnalysis(self)
