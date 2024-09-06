"""TorqueConverterConnectionCompoundSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3244,
)

_TORQUE_CONVERTER_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "TorqueConverterConnectionCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3194,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3241,
        _3271,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2406

    Self = TypeVar(
        "Self", bound="TorqueConverterConnectionCompoundSteadyStateSynchronousResponse"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorqueConverterConnectionCompoundSteadyStateSynchronousResponse._Cast_TorqueConverterConnectionCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterConnectionCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterConnectionCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting TorqueConverterConnectionCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: "TorqueConverterConnectionCompoundSteadyStateSynchronousResponse"

    @property
    def coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3244.CouplingConnectionCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3244.CouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def inter_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3271.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3271,
        )

        return self.__parent__._cast(
            _3271.InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3241.ConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3241,
        )

        return self.__parent__._cast(
            _3241.ConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7708.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7708,
        )

        return self.__parent__._cast(_7708.ConnectionCompoundAnalysis)

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
    def torque_converter_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "TorqueConverterConnectionCompoundSteadyStateSynchronousResponse":
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
class TorqueConverterConnectionCompoundSteadyStateSynchronousResponse(
    _3244.CouplingConnectionCompoundSteadyStateSynchronousResponse
):
    """TorqueConverterConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _TORQUE_CONVERTER_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2406.TorqueConverterConnection":
        """mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2406.TorqueConverterConnection":
        """mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3194.TorqueConverterConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.TorqueConverterConnectionSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3194.TorqueConverterConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.TorqueConverterConnectionSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_TorqueConverterConnectionCompoundSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterConnectionCompoundSteadyStateSynchronousResponse
        """
        return _Cast_TorqueConverterConnectionCompoundSteadyStateSynchronousResponse(
            self
        )
