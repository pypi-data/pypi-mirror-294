"""StraightBevelSunGearCompoundPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4380,
)

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "StraightBevelSunGearCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4255
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4277,
        _4289,
        _4298,
        _4305,
        _4331,
        _4352,
        _4354,
    )

    Self = TypeVar("Self", bound="StraightBevelSunGearCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelSunGearCompoundPowerFlow._Cast_StraightBevelSunGearCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGearCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelSunGearCompoundPowerFlow:
    """Special nested class for casting StraightBevelSunGearCompoundPowerFlow to subclasses."""

    __parent__: "StraightBevelSunGearCompoundPowerFlow"

    @property
    def straight_bevel_diff_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4380.StraightBevelDiffGearCompoundPowerFlow":
        return self.__parent__._cast(_4380.StraightBevelDiffGearCompoundPowerFlow)

    @property
    def bevel_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4289.BevelGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4289,
        )

        return self.__parent__._cast(_4289.BevelGearCompoundPowerFlow)

    @property
    def agma_gleason_conical_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "_4277.AGMAGleasonConicalGearCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4277,
        )

        return self.__parent__._cast(_4277.AGMAGleasonConicalGearCompoundPowerFlow)

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
    def straight_bevel_sun_gear_compound_power_flow(
        self: "CastSelf",
    ) -> "StraightBevelSunGearCompoundPowerFlow":
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
class StraightBevelSunGearCompoundPowerFlow(
    _4380.StraightBevelDiffGearCompoundPowerFlow
):
    """StraightBevelSunGearCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4255.StraightBevelSunGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow]

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
    ) -> "List[_4255.StraightBevelSunGearPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_StraightBevelSunGearCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelSunGearCompoundPowerFlow
        """
        return _Cast_StraightBevelSunGearCompoundPowerFlow(self)
