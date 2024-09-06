"""KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow"""

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
    _4341,
)

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4210
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4273,
        _4307,
        _4333,
        _4342,
        _4343,
        _4354,
        _4373,
    )
    from mastapy._private.system_model.part_model.gears import _2596

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow._Cast_KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4341.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow":
        return self.__parent__._cast(
            _4341.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow
        )

    @property
    def conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4307.ConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4307,
        )

        return self.__parent__._cast(_4307.ConicalGearSetCompoundPowerFlow)

    @property
    def gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4333.GearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4333,
        )

        return self.__parent__._cast(_4333.GearSetCompoundPowerFlow)

    @property
    def specialised_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4373.SpecialisedAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4373,
        )

        return self.__parent__._cast(_4373.SpecialisedAssemblyCompoundPowerFlow)

    @property
    def abstract_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4273.AbstractAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4273,
        )

        return self.__parent__._cast(_4273.AbstractAssemblyCompoundPowerFlow)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow":
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
class KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow(
    _4341.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow
):
    """KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_POWER_FLOW
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2596.KlingelnbergCycloPalloidHypoidGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2596.KlingelnbergCycloPalloidHypoidGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4210.KlingelnbergCycloPalloidHypoidGearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearSetPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_power_flow(
        self: "Self",
    ) -> "List[_4342.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearsCompoundPowerFlow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_power_flow(
        self: "Self",
    ) -> "List[_4343.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidMeshesCompoundPowerFlow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_4210.KlingelnbergCycloPalloidHypoidGearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearSetPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow(self)
