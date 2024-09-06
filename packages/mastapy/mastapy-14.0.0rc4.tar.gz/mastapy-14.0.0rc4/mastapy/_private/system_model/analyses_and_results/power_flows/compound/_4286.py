"""BevelDifferentialGearSetCompoundPowerFlow"""

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
    _4291,
)

_BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "BevelDifferentialGearSetCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4149
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4273,
        _4279,
        _4284,
        _4285,
        _4307,
        _4333,
        _4354,
        _4373,
    )
    from mastapy._private.system_model.part_model.gears import _2573

    Self = TypeVar("Self", bound="BevelDifferentialGearSetCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialGearSetCompoundPowerFlow._Cast_BevelDifferentialGearSetCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGearSetCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGearSetCompoundPowerFlow:
    """Special nested class for casting BevelDifferentialGearSetCompoundPowerFlow to subclasses."""

    __parent__: "BevelDifferentialGearSetCompoundPowerFlow"

    @property
    def bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4291.BevelGearSetCompoundPowerFlow":
        return self.__parent__._cast(_4291.BevelGearSetCompoundPowerFlow)

    @property
    def agma_gleason_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4279.AGMAGleasonConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4279,
        )

        return self.__parent__._cast(_4279.AGMAGleasonConicalGearSetCompoundPowerFlow)

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
    def bevel_differential_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "BevelDifferentialGearSetCompoundPowerFlow":
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
class BevelDifferentialGearSetCompoundPowerFlow(_4291.BevelGearSetCompoundPowerFlow):
    """BevelDifferentialGearSetCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR_SET_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2573.BevelDifferentialGearSet":
        """mastapy.system_model.part_model.gears.BevelDifferentialGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2573.BevelDifferentialGearSet":
        """mastapy.system_model.part_model.gears.BevelDifferentialGearSet

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
    ) -> "List[_4149.BevelDifferentialGearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearSetPowerFlow]

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
    def bevel_differential_gears_compound_power_flow(
        self: "Self",
    ) -> "List[_4284.BevelDifferentialGearCompoundPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearCompoundPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelDifferentialGearsCompoundPowerFlow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_differential_meshes_compound_power_flow(
        self: "Self",
    ) -> "List[_4285.BevelDifferentialGearMeshCompoundPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.compound.BevelDifferentialGearMeshCompoundPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelDifferentialMeshesCompoundPowerFlow"
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
    ) -> "List[_4149.BevelDifferentialGearSetPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearSetPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialGearSetCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGearSetCompoundPowerFlow
        """
        return _Cast_BevelDifferentialGearSetCompoundPowerFlow(self)
