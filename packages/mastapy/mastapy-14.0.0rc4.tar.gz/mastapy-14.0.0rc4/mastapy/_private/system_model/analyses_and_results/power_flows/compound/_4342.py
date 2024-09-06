"""KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4339,
)

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4209
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4298,
        _4305,
        _4331,
        _4352,
        _4354,
    )
    from mastapy._private.system_model.part_model.gears import _2595

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow._Cast_KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4339.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow":
        return self.__parent__._cast(
            _4339.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow
        )

    @property
    def conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4305.ConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4305,
        )

        return self.__parent__._cast(_4305.ConicalGearCompoundPowerFlow)

    @property
    def gear_compound_power_flow(self: "CastSelf") -> "_4331.GearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4331,
        )

        return self.__parent__._cast(_4331.GearCompoundPowerFlow)

    @property
    def mountable_component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4352.MountableComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4352,
        )

        return self.__parent__._cast(_4352.MountableComponentCompoundPowerFlow)

    @property
    def component_compound_power_flow(
        self: "CastSelf",
    ) -> "_4298.ComponentCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4298,
        )

        return self.__parent__._cast(_4298.ComponentCompoundPowerFlow)

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4354.PartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4354,
        )

        return self.__parent__._cast(_4354.PartCompoundPowerFlow)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow":
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
class KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow(
    _4339.KlingelnbergCycloPalloidConicalGearCompoundPowerFlow
):
    """KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_COMPOUND_POWER_FLOW

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
    ) -> "List[_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearPowerFlow]

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
    ) -> "List[_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearPowerFlow]

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
    ) -> "_Cast_KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow(self)
