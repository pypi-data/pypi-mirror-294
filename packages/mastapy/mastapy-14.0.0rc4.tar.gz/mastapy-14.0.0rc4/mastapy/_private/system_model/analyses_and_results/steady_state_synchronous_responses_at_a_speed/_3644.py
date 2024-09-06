"""CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3624,
)

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3603,
        _3635,
        _3699,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2389

    Self = TypeVar(
        "Self",
        bound="CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed._Cast_CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: (
        "CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed"
    )

    @property
    def coaxial_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3624.CoaxialConnectionSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3624.CoaxialConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3699.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3699,
        )

        return self.__parent__._cast(
            _3699.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3603.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3603,
        )

        return self.__parent__._cast(
            _3603.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3635.ConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3635,
        )

        return self.__parent__._cast(
            _3635.ConnectionSteadyStateSynchronousResponseAtASpeed
        )

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
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed":
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
class CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed(
    _3624.CoaxialConnectionSteadyStateSynchronousResponseAtASpeed
):
    """CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
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
    ) -> "_2389.CycloidalDiscCentralBearingConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection

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
    ) -> "_Cast_CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseAtASpeed(
            self
        )
