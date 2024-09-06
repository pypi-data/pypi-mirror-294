"""KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6615,
)

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_DYNAMIC_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
        "KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6490,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6574,
        _6581,
        _6607,
        _6628,
        _6630,
    )
    from mastapy._private.system_model.part_model.gears import _2597

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis._Cast_KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6615.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis":
        return self.__parent__._cast(
            _6615.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis
        )

    @property
    def conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6581.ConicalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6581,
        )

        return self.__parent__._cast(_6581.ConicalGearCompoundDynamicAnalysis)

    @property
    def gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6607.GearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6607,
        )

        return self.__parent__._cast(_6607.GearCompoundDynamicAnalysis)

    @property
    def mountable_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6628.MountableComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6628,
        )

        return self.__parent__._cast(_6628.MountableComponentCompoundDynamicAnalysis)

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6574.ComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6574,
        )

        return self.__parent__._cast(_6574.ComponentCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6630.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6630,
        )

        return self.__parent__._cast(_6630.PartCompoundDynamicAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7715.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7712.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2735.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.DesignEntityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis":
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
class KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis(
    _6615.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis
):
    """KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_COMPOUND_DYNAMIC_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(
        self: "Self",
    ) -> "_2597.KlingelnbergCycloPalloidSpiralBevelGear":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6490.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6490.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis(
            self
        )
