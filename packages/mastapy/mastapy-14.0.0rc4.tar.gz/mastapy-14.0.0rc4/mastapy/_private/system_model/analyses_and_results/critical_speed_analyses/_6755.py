"""KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis"""

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
    _6718,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis",
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
        _6747,
        _6758,
        _6761,
        _6768,
        _6770,
    )
    from mastapy._private.system_model.part_model.gears import _2593

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis._Cast_KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis"

    @property
    def conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6718.ConicalGearCriticalSpeedAnalysis":
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
    def klingelnberg_cyclo_palloid_hypoid_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6758.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6758,
        )

        return self.__parent__._cast(
            _6758.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6761.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6761,
        )

        return self.__parent__._cast(
            _6761.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_critical_speed_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis":
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
class KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis(
    _6718.ConicalGearCriticalSpeedAnalysis
):
    """KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_CRITICAL_SPEED_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2593.KlingelnbergCycloPalloidConicalGear":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearCriticalSpeedAnalysis(self)
