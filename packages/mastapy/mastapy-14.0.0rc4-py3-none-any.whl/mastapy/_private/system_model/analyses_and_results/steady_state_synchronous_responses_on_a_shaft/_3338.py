"""AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
    _3362,
)

_ABSTRACT_SHAFT_OR_HOUSING_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3339,
        _3383,
        _3393,
        _3418,
        _3435,
    )
    from mastapy._private.system_model.part_model import _2491

    Self = TypeVar(
        "Self", bound="AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft._Cast_AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft"

    @property
    def component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3362.ComponentSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3362.ComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3418.PartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3418,
        )

        return self.__parent__._cast(_3418.PartSteadyStateSynchronousResponseOnAShaft)

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
    def abstract_shaft_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3339.AbstractShaftSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3339,
        )

        return self.__parent__._cast(
            _3339.AbstractShaftSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3383.CycloidalDiscSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3383,
        )

        return self.__parent__._cast(
            _3383.CycloidalDiscSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def fe_part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3393.FEPartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3393,
        )

        return self.__parent__._cast(_3393.FEPartSteadyStateSynchronousResponseOnAShaft)

    @property
    def shaft_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3435.ShaftSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3435,
        )

        return self.__parent__._cast(_3435.ShaftSteadyStateSynchronousResponseOnAShaft)

    @property
    def abstract_shaft_or_housing_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft":
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
class AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft(
    _3362.ComponentSteadyStateSynchronousResponseOnAShaft
):
    """AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_OR_HOUSING_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2491.AbstractShaftOrHousing":
        """mastapy.system_model.part_model.AbstractShaftOrHousing

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_AbstractShaftOrHousingSteadyStateSynchronousResponseOnAShaft(self)
