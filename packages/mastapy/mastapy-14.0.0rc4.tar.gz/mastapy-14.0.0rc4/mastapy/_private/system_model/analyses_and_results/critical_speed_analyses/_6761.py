"""KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6755,
)

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_CRITICAL_SPEED_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
        "KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6711,
        _6718,
        _6747,
        _6768,
        _6770,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7066
    from mastapy._private.system_model.part_model.gears import _2597

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis._Cast_KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6755.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _6755.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis
        )

    @property
    def conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6718.ConicalGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6718,
        )

        return self.__parent__._cast(_6718.ConicalGearCriticalSpeedAnalysis)

    @property
    def gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6747.GearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6747,
        )

        return self.__parent__._cast(_6747.GearCriticalSpeedAnalysis)

    @property
    def mountable_component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6768.MountableComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6768,
        )

        return self.__parent__._cast(_6768.MountableComponentCriticalSpeedAnalysis)

    @property
    def component_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6711.ComponentCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6711,
        )

        return self.__parent__._cast(_6711.ComponentCriticalSpeedAnalysis)

    @property
    def part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6770.PartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6770,
        )

        return self.__parent__._cast(_6770.PartCriticalSpeedAnalysis)

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
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis":
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
class KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis(
    _6755.KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis
):
    """KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_CRITICAL_SPEED_ANALYSIS
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
    def component_load_case(
        self: "Self",
    ) -> "_7066.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis(self)
