"""StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3313,
)

_STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3188,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3210,
        _3222,
        _3231,
        _3238,
        _3264,
        _3285,
        _3287,
    )

    Self = TypeVar(
        "Self", bound="StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse._Cast_StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: "StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse"

    @property
    def straight_bevel_diff_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3313.StraightBevelDiffGearCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3313.StraightBevelDiffGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3222.BevelGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3222,
        )

        return self.__parent__._cast(
            _3222.BevelGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def agma_gleason_conical_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3210.AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3210,
        )

        return self.__parent__._cast(
            _3210.AGMAGleasonConicalGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3238.ConicalGearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3238,
        )

        return self.__parent__._cast(
            _3238.ConicalGearCompoundSteadyStateSynchronousResponse
        )

    @property
    def gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3264.GearCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3264,
        )

        return self.__parent__._cast(_3264.GearCompoundSteadyStateSynchronousResponse)

    @property
    def mountable_component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3285.MountableComponentCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3285,
        )

        return self.__parent__._cast(
            _3285.MountableComponentCompoundSteadyStateSynchronousResponse
        )

    @property
    def component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3231.ComponentCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3231,
        )

        return self.__parent__._cast(
            _3231.ComponentCompoundSteadyStateSynchronousResponse
        )

    @property
    def part_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3287.PartCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3287,
        )

        return self.__parent__._cast(_3287.PartCompoundSteadyStateSynchronousResponse)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7715.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.PartCompoundAnalysis)

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
    def straight_bevel_planet_gear_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse":
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
class StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse(
    _3313.StraightBevelDiffGearCompoundSteadyStateSynchronousResponse
):
    """StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3188.StraightBevelPlanetGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.StraightBevelPlanetGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3188.StraightBevelPlanetGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.StraightBevelPlanetGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse
        """
        return _Cast_StraightBevelPlanetGearCompoundSteadyStateSynchronousResponse(self)
