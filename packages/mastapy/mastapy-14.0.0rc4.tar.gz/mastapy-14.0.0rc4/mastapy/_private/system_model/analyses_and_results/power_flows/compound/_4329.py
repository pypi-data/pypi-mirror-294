"""FEPartCompoundPowerFlow"""

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
    _4275,
)

_FE_PART_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "FEPartCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4195
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4298,
        _4354,
    )
    from mastapy._private.system_model.part_model import _2508

    Self = TypeVar("Self", bound="FEPartCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="FEPartCompoundPowerFlow._Cast_FEPartCompoundPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEPartCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartCompoundPowerFlow:
    """Special nested class for casting FEPartCompoundPowerFlow to subclasses."""

    __parent__: "FEPartCompoundPowerFlow"

    @property
    def abstract_shaft_or_housing_compound_power_flow(
        self: "CastSelf",
    ) -> "_4275.AbstractShaftOrHousingCompoundPowerFlow":
        return self.__parent__._cast(_4275.AbstractShaftOrHousingCompoundPowerFlow)

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
    def fe_part_compound_power_flow(self: "CastSelf") -> "FEPartCompoundPowerFlow":
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
class FEPartCompoundPowerFlow(_4275.AbstractShaftOrHousingCompoundPowerFlow):
    """FEPartCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2508.FEPart":
        """mastapy.system_model.part_model.FEPart

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(self: "Self") -> "List[_4195.FEPartPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.FEPartPowerFlow]

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
    def component_analysis_cases(self: "Self") -> "List[_4195.FEPartPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.FEPartPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_FEPartCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_FEPartCompoundPowerFlow
        """
        return _Cast_FEPartCompoundPowerFlow(self)
