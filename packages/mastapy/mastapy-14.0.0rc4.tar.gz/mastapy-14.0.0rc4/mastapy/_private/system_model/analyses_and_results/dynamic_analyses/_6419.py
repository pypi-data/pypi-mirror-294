"""AbstractShaftToMountableComponentConnectionDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6451

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "AbstractShaftToMountableComponentConnectionDynamicAnalysis",
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
        _6440,
        _6460,
        _6462,
        _6503,
        _6517,
    )
    from mastapy._private.system_model.connections_and_sockets import _2319

    Self = TypeVar(
        "Self", bound="AbstractShaftToMountableComponentConnectionDynamicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionDynamicAnalysis._Cast_AbstractShaftToMountableComponentConnectionDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionDynamicAnalysis:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionDynamicAnalysis to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionDynamicAnalysis"

    @property
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6451.ConnectionDynamicAnalysis":
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
    def coaxial_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6440.CoaxialConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6440,
        )

        return self.__parent__._cast(_6440.CoaxialConnectionDynamicAnalysis)

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
    def cycloidal_disc_planetary_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6462.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6462,
        )

        return self.__parent__._cast(
            _6462.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis
        )

    @property
    def planetary_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6503.PlanetaryConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6503,
        )

        return self.__parent__._cast(_6503.PlanetaryConnectionDynamicAnalysis)

    @property
    def shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6517.ShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6517,
        )

        return self.__parent__._cast(
            _6517.ShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionDynamicAnalysis":
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
class AbstractShaftToMountableComponentConnectionDynamicAnalysis(
    _6451.ConnectionDynamicAnalysis
):
    """AbstractShaftToMountableComponentConnectionDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_DYNAMIC_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(
        self: "Self",
    ) -> "_2319.AbstractShaftToMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionDynamicAnalysis
        """
        return _Cast_AbstractShaftToMountableComponentConnectionDynamicAnalysis(self)
