"""AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed"""

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
    _3634,
)

_AGMA_GLEASON_CONICAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3613,
        _3614,
        _3615,
        _3618,
        _3625,
        _3660,
        _3664,
        _3679,
        _3681,
        _3703,
        _3710,
        _3713,
        _3714,
        _3715,
        _3731,
    )
    from mastapy._private.system_model.part_model.gears import _2570

    Self = TypeVar(
        "Self", bound="AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed._Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed"

    @property
    def conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3634.ConicalGearSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3634.ConicalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3660.GearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3660,
        )

        return self.__parent__._cast(_3660.GearSteadyStateSynchronousResponseAtASpeed)

    @property
    def mountable_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3679.MountableComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3679,
        )

        return self.__parent__._cast(
            _3679.MountableComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3625.ComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3625,
        )

        return self.__parent__._cast(
            _3625.ComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3681.PartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3681,
        )

        return self.__parent__._cast(_3681.PartSteadyStateSynchronousResponseAtASpeed)

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
    def bevel_differential_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3613.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3613,
        )

        return self.__parent__._cast(
            _3613.BevelDifferentialGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3614.BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3614,
        )

        return self.__parent__._cast(
            _3614.BevelDifferentialPlanetGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3615.BevelDifferentialSunGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3615,
        )

        return self.__parent__._cast(
            _3615.BevelDifferentialSunGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3618.BevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3618,
        )

        return self.__parent__._cast(
            _3618.BevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3664.HypoidGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3664,
        )

        return self.__parent__._cast(
            _3664.HypoidGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3703.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3703,
        )

        return self.__parent__._cast(
            _3703.SpiralBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3710.StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3710,
        )

        return self.__parent__._cast(
            _3710.StraightBevelDiffGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3713.StraightBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3713,
        )

        return self.__parent__._cast(
            _3713.StraightBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_planet_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3714.StraightBevelPlanetGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3714,
        )

        return self.__parent__._cast(
            _3714.StraightBevelPlanetGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_sun_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3715.StraightBevelSunGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3715,
        )

        return self.__parent__._cast(
            _3715.StraightBevelSunGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3731.ZerolBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3731,
        )

        return self.__parent__._cast(
            _3731.ZerolBevelGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed":
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
class AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed(
    _3634.ConicalGearSteadyStateSynchronousResponseAtASpeed
):
    """AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _AGMA_GLEASON_CONICAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2570.AGMAGleasonConicalGear":
        """mastapy.system_model.part_model.gears.AGMAGleasonConicalGear

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
    ) -> "_Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed(self)
