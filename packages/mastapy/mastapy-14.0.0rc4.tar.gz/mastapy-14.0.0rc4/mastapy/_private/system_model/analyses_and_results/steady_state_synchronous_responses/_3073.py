"""AbstractShaftSteadyStateSynchronousResponse"""

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
    _3072,
)

_ABSTRACT_SHAFT_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "AbstractShaftSteadyStateSynchronousResponse",
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
        _3117,
        _3153,
        _3170,
    )
    from mastapy._private.system_model.part_model import _2490

    Self = TypeVar("Self", bound="AbstractShaftSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftSteadyStateSynchronousResponse._Cast_AbstractShaftSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftSteadyStateSynchronousResponse:
    """Special nested class for casting AbstractShaftSteadyStateSynchronousResponse to subclasses."""

    __parent__: "AbstractShaftSteadyStateSynchronousResponse"

    @property
    def abstract_shaft_or_housing_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3072.AbstractShaftOrHousingSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3072.AbstractShaftOrHousingSteadyStateSynchronousResponse
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
    def cycloidal_disc_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3117.CycloidalDiscSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3117,
        )

        return self.__parent__._cast(_3117.CycloidalDiscSteadyStateSynchronousResponse)

    @property
    def shaft_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3170.ShaftSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3170,
        )

        return self.__parent__._cast(_3170.ShaftSteadyStateSynchronousResponse)

    @property
    def abstract_shaft_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "AbstractShaftSteadyStateSynchronousResponse":
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
class AbstractShaftSteadyStateSynchronousResponse(
    _3072.AbstractShaftOrHousingSteadyStateSynchronousResponse
):
    """AbstractShaftSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2490.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftSteadyStateSynchronousResponse
        """
        return _Cast_AbstractShaftSteadyStateSynchronousResponse(self)
