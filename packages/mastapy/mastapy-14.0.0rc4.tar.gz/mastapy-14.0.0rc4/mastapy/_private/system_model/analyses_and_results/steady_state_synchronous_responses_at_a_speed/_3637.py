"""CouplingConnectionSteadyStateSynchronousResponseAtASpeed"""

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
    _3665,
)

_COUPLING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "CouplingConnectionSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3621,
        _3626,
        _3635,
        _3682,
        _3704,
        _3720,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2400

    Self = TypeVar(
        "Self", bound="CouplingConnectionSteadyStateSynchronousResponseAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionSteadyStateSynchronousResponseAtASpeed._Cast_CouplingConnectionSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting CouplingConnectionSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "CouplingConnectionSteadyStateSynchronousResponseAtASpeed"

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3665.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed"
    ):
        return self.__parent__._cast(
            _3665.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
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
    def clutch_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3621.ClutchConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3621,
        )

        return self.__parent__._cast(
            _3621.ClutchConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3626.ConceptCouplingConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3626,
        )

        return self.__parent__._cast(
            _3626.ConceptCouplingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3682.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3682,
        )

        return self.__parent__._cast(
            _3682.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3704.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3704,
        )

        return self.__parent__._cast(
            _3704.SpringDamperConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3720.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3720,
        )

        return self.__parent__._cast(
            _3720.TorqueConverterConnectionSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_connection_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "CouplingConnectionSteadyStateSynchronousResponseAtASpeed":
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
class CouplingConnectionSteadyStateSynchronousResponseAtASpeed(
    _3665.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed
):
    """CouplingConnectionSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _COUPLING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2400.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

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
    ) -> "_Cast_CouplingConnectionSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_CouplingConnectionSteadyStateSynchronousResponseAtASpeed(self)
