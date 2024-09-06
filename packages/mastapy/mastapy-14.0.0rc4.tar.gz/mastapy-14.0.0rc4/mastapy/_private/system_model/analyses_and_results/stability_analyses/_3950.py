"""PlanetaryConnectionStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses import _3964

_PLANETARY_CONNECTION_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "PlanetaryConnectionStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3866,
        _3898,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7082
    from mastapy._private.system_model.connections_and_sockets import _2341

    Self = TypeVar("Self", bound="PlanetaryConnectionStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlanetaryConnectionStabilityAnalysis._Cast_PlanetaryConnectionStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryConnectionStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryConnectionStabilityAnalysis:
    """Special nested class for casting PlanetaryConnectionStabilityAnalysis to subclasses."""

    __parent__: "PlanetaryConnectionStabilityAnalysis"

    @property
    def shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3964.ShaftToMountableComponentConnectionStabilityAnalysis":
        return self.__parent__._cast(
            _3964.ShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3866.AbstractShaftToMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3866,
        )

        return self.__parent__._cast(
            _3866.AbstractShaftToMountableComponentConnectionStabilityAnalysis
        )

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3898.ConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3898,
        )

        return self.__parent__._cast(_3898.ConnectionStabilityAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7710.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7707.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7707,
        )

        return self.__parent__._cast(_7707.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2733.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2733

        return self.__parent__._cast(_2733.ConnectionAnalysis)

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
    def planetary_connection_stability_analysis(
        self: "CastSelf",
    ) -> "PlanetaryConnectionStabilityAnalysis":
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
class PlanetaryConnectionStabilityAnalysis(
    _3964.ShaftToMountableComponentConnectionStabilityAnalysis
):
    """PlanetaryConnectionStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_CONNECTION_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2341.PlanetaryConnection":
        """mastapy.system_model.connections_and_sockets.PlanetaryConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7082.PlanetaryConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetaryConnectionStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryConnectionStabilityAnalysis
        """
        return _Cast_PlanetaryConnectionStabilityAnalysis(self)
