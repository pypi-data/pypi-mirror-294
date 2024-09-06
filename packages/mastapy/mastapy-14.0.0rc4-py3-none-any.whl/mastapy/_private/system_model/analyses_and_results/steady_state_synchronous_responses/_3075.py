"""AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3103,
)

_AGMA_GLEASON_CONICAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3082,
        _3087,
        _3106,
        _3130,
        _3134,
        _3137,
        _3173,
        _3182,
        _3185,
        _3203,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2353

    Self = TypeVar(
        "Self", bound="AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse._Cast_AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse:
    """Special nested class for casting AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse"

    @property
    def conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3103.ConicalGearMeshSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3103.ConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3130.GearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3130,
        )

        return self.__parent__._cast(_3130.GearMeshSteadyStateSynchronousResponse)

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3137.InterMountableComponentConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3137,
        )

        return self.__parent__._cast(
            _3137.InterMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3106.ConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3106,
        )

        return self.__parent__._cast(_3106.ConnectionSteadyStateSynchronousResponse)

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
    def bevel_differential_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3082.BevelDifferentialGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3082,
        )

        return self.__parent__._cast(
            _3082.BevelDifferentialGearMeshSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3087.BevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3087,
        )

        return self.__parent__._cast(_3087.BevelGearMeshSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3134.HypoidGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3134,
        )

        return self.__parent__._cast(_3134.HypoidGearMeshSteadyStateSynchronousResponse)

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3173.SpiralBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3173,
        )

        return self.__parent__._cast(
            _3173.SpiralBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3182.StraightBevelDiffGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3182,
        )

        return self.__parent__._cast(
            _3182.StraightBevelDiffGearMeshSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3185.StraightBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3185,
        )

        return self.__parent__._cast(
            _3185.StraightBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3203.ZerolBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3203,
        )

        return self.__parent__._cast(
            _3203.ZerolBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse":
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
class AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse(
    _3103.ConicalGearMeshSteadyStateSynchronousResponse
):
    """AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _AGMA_GLEASON_CONICAL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2353.AGMAGleasonConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh

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
    ) -> "_Cast_AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse
        """
        return _Cast_AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse(self)
