"""KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6886,
)

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
        "KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6758,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6845,
        _6852,
        _6878,
        _6899,
        _6901,
    )
    from mastapy._private.system_model.part_model.gears import _2595

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6886.KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _6886.KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis
        )

    @property
    def conical_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6852.ConicalGearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6852,
        )

        return self.__parent__._cast(_6852.ConicalGearCompoundCriticalSpeedAnalysis)

    @property
    def gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6878.GearCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6878,
        )

        return self.__parent__._cast(_6878.GearCompoundCriticalSpeedAnalysis)

    @property
    def mountable_component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6899.MountableComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6899,
        )

        return self.__parent__._cast(
            _6899.MountableComponentCompoundCriticalSpeedAnalysis
        )

    @property
    def component_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6845.ComponentCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6845,
        )

        return self.__parent__._cast(_6845.ComponentCompoundCriticalSpeedAnalysis)

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6901.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6901,
        )

        return self.__parent__._cast(_6901.PartCompoundCriticalSpeedAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis":
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
class KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis(
    _6886.KlingelnbergCycloPalloidConicalGearCompoundCriticalSpeedAnalysis
):
    """KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_CRITICAL_SPEED_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2595.KlingelnbergCycloPalloidHypoidGear":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear

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
    ) -> "List[_6758.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis]

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
    ) -> "List[_6758.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.KlingelnbergCycloPalloidHypoidGearCriticalSpeedAnalysis]

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
    ) -> "_Cast_KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearCompoundCriticalSpeedAnalysis(
            self
        )
