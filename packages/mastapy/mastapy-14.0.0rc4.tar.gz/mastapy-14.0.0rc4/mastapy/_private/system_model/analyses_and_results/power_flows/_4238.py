"""ShaftHubConnectionPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4172

_SHAFT_HUB_CONNECTION_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "ShaftHubConnectionPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.detailed_rigid_connectors.rating import _1484
    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4161,
        _4218,
        _4220,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7099
    from mastapy._private.system_model.part_model.couplings import _2658

    Self = TypeVar("Self", bound="ShaftHubConnectionPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftHubConnectionPowerFlow._Cast_ShaftHubConnectionPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftHubConnectionPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftHubConnectionPowerFlow:
    """Special nested class for casting ShaftHubConnectionPowerFlow to subclasses."""

    __parent__: "ShaftHubConnectionPowerFlow"

    @property
    def connector_power_flow(self: "CastSelf") -> "_4172.ConnectorPowerFlow":
        return self.__parent__._cast(_4172.ConnectorPowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4218.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4218

        return self.__parent__._cast(_4218.MountableComponentPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4161.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4161

        return self.__parent__._cast(_4161.ComponentPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4220.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4220

        return self.__parent__._cast(_4220.PartPowerFlow)

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
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "ShaftHubConnectionPowerFlow":
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
class ShaftHubConnectionPowerFlow(_4172.ConnectorPowerFlow):
    """ShaftHubConnectionPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_HUB_CONNECTION_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2658.ShaftHubConnection":
        """mastapy.system_model.part_model.couplings.ShaftHubConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_1484.ShaftHubConnectionRating":
        """mastapy.detailed_rigid_connectors.rating.ShaftHubConnectionRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7099.ShaftHubConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftHubConnectionPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ShaftHubConnectionPowerFlow
        """
        return _Cast_ShaftHubConnectionPowerFlow(self)
