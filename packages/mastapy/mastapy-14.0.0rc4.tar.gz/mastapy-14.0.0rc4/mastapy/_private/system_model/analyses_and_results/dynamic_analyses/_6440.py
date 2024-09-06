"""CoaxialConnectionDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6517

_COAXIAL_CONNECTION_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "CoaxialConnectionDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7709,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6419,
        _6451,
        _6460,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6984
    from mastapy._private.system_model.connections_and_sockets import _2323

    Self = TypeVar("Self", bound="CoaxialConnectionDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoaxialConnectionDynamicAnalysis._Cast_CoaxialConnectionDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoaxialConnectionDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoaxialConnectionDynamicAnalysis:
    """Special nested class for casting CoaxialConnectionDynamicAnalysis to subclasses."""

    __parent__: "CoaxialConnectionDynamicAnalysis"

    @property
    def shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6517.ShaftToMountableComponentConnectionDynamicAnalysis":
        return self.__parent__._cast(
            _6517.ShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6419.AbstractShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6419,
        )

        return self.__parent__._cast(
            _6419.AbstractShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6451.ConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6451,
        )

        return self.__parent__._cast(_6451.ConnectionDynamicAnalysis)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7709.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.ConnectionFEAnalysis)

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
    def cycloidal_disc_central_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6460.CycloidalDiscCentralBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6460,
        )

        return self.__parent__._cast(
            _6460.CycloidalDiscCentralBearingConnectionDynamicAnalysis
        )

    @property
    def coaxial_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "CoaxialConnectionDynamicAnalysis":
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
class CoaxialConnectionDynamicAnalysis(
    _6517.ShaftToMountableComponentConnectionDynamicAnalysis
):
    """CoaxialConnectionDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COAXIAL_CONNECTION_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2323.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_6984.CoaxialConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CoaxialConnectionDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CoaxialConnectionDynamicAnalysis
        """
        return _Cast_CoaxialConnectionDynamicAnalysis(self)
