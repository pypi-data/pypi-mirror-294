"""VirtualComponentSteadyStateSynchronousResponse"""

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
    _3151,
)

_VIRTUAL_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "VirtualComponentSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3096,
        _3147,
        _3148,
        _3153,
        _3160,
        _3161,
        _3198,
    )
    from mastapy._private.system_model.part_model import _2536

    Self = TypeVar("Self", bound="VirtualComponentSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentSteadyStateSynchronousResponse._Cast_VirtualComponentSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentSteadyStateSynchronousResponse:
    """Special nested class for casting VirtualComponentSteadyStateSynchronousResponse to subclasses."""

    __parent__: "VirtualComponentSteadyStateSynchronousResponse"

    @property
    def mountable_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3151.MountableComponentSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3151.MountableComponentSteadyStateSynchronousResponse
        )

    @property
    def component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3096.ComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3096,
        )

        return self.__parent__._cast(_3096.ComponentSteadyStateSynchronousResponse)

    @property
    def part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3153.PartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3153,
        )

        return self.__parent__._cast(_3153.PartSteadyStateSynchronousResponse)

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
    def mass_disc_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3147.MassDiscSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3147,
        )

        return self.__parent__._cast(_3147.MassDiscSteadyStateSynchronousResponse)

    @property
    def measurement_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3148.MeasurementComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3148,
        )

        return self.__parent__._cast(
            _3148.MeasurementComponentSteadyStateSynchronousResponse
        )

    @property
    def point_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3160.PointLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3160,
        )

        return self.__parent__._cast(_3160.PointLoadSteadyStateSynchronousResponse)

    @property
    def power_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3161.PowerLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3161,
        )

        return self.__parent__._cast(_3161.PowerLoadSteadyStateSynchronousResponse)

    @property
    def unbalanced_mass_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3198.UnbalancedMassSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3198,
        )

        return self.__parent__._cast(_3198.UnbalancedMassSteadyStateSynchronousResponse)

    @property
    def virtual_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "VirtualComponentSteadyStateSynchronousResponse":
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
class VirtualComponentSteadyStateSynchronousResponse(
    _3151.MountableComponentSteadyStateSynchronousResponse
):
    """VirtualComponentSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2536.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualComponentSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentSteadyStateSynchronousResponse
        """
        return _Cast_VirtualComponentSteadyStateSynchronousResponse(self)
