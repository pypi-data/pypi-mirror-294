"""KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7627,
)

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7497,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7586,
        _7593,
        _7619,
        _7640,
        _7642,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.part_model.gears import _2595

    Self = TypeVar(
        "Self",
        bound="KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection._Cast_KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7627.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7627.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7593.ConicalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7593,
        )

        return self.__parent__._cast(_7593.ConicalGearCompoundAdvancedSystemDeflection)

    @property
    def gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7619.GearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7619,
        )

        return self.__parent__._cast(_7619.GearCompoundAdvancedSystemDeflection)

    @property
    def mountable_component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7640.MountableComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7640,
        )

        return self.__parent__._cast(
            _7640.MountableComponentCompoundAdvancedSystemDeflection
        )

    @property
    def component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7586.ComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7586,
        )

        return self.__parent__._cast(_7586.ComponentCompoundAdvancedSystemDeflection)

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7642.PartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7642,
        )

        return self.__parent__._cast(_7642.PartCompoundAdvancedSystemDeflection)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection":
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
class KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection(
    _7627.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection
):
    """KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_ADVANCED_SYSTEM_DEFLECTION
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
    ) -> "List[_7497.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection]

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
    ) -> "List[_7497.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection]

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
    ) -> "_Cast_KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection(
            self
        )
