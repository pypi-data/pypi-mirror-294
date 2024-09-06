"""AGMAGleasonConicalGearSteadyStateSynchronousResponse"""

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
    _3105,
)

_AGMA_GLEASON_CONICAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "AGMAGleasonConicalGearSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3084,
        _3085,
        _3086,
        _3089,
        _3096,
        _3132,
        _3136,
        _3151,
        _3153,
        _3175,
        _3184,
        _3187,
        _3188,
        _3189,
        _3205,
    )
    from mastapy._private.system_model.part_model.gears import _2570

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearSteadyStateSynchronousResponse._Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponse:
    """Special nested class for casting AGMAGleasonConicalGearSteadyStateSynchronousResponse to subclasses."""

    __parent__: "AGMAGleasonConicalGearSteadyStateSynchronousResponse"

    @property
    def conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3105.ConicalGearSteadyStateSynchronousResponse":
        return self.__parent__._cast(_3105.ConicalGearSteadyStateSynchronousResponse)

    @property
    def gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3132.GearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3132,
        )

        return self.__parent__._cast(_3132.GearSteadyStateSynchronousResponse)

    @property
    def mountable_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3151.MountableComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3151,
        )

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
    def bevel_differential_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3084.BevelDifferentialGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3084,
        )

        return self.__parent__._cast(
            _3084.BevelDifferentialGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3085.BevelDifferentialPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3085,
        )

        return self.__parent__._cast(
            _3085.BevelDifferentialPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3086.BevelDifferentialSunGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3086,
        )

        return self.__parent__._cast(
            _3086.BevelDifferentialSunGearSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3089.BevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3089,
        )

        return self.__parent__._cast(_3089.BevelGearSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3136.HypoidGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3136,
        )

        return self.__parent__._cast(_3136.HypoidGearSteadyStateSynchronousResponse)

    @property
    def spiral_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3175.SpiralBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3175,
        )

        return self.__parent__._cast(
            _3175.SpiralBevelGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3184.StraightBevelDiffGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3184,
        )

        return self.__parent__._cast(
            _3184.StraightBevelDiffGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3187.StraightBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3187,
        )

        return self.__parent__._cast(
            _3187.StraightBevelGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3188.StraightBevelPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3188,
        )

        return self.__parent__._cast(
            _3188.StraightBevelPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_sun_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3189.StraightBevelSunGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3189,
        )

        return self.__parent__._cast(
            _3189.StraightBevelSunGearSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3205.ZerolBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3205,
        )

        return self.__parent__._cast(_3205.ZerolBevelGearSteadyStateSynchronousResponse)

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearSteadyStateSynchronousResponse":
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
class AGMAGleasonConicalGearSteadyStateSynchronousResponse(
    _3105.ConicalGearSteadyStateSynchronousResponse
):
    """AGMAGleasonConicalGearSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _AGMA_GLEASON_CONICAL_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE
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
    ) -> "_Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponse
        """
        return _Cast_AGMAGleasonConicalGearSteadyStateSynchronousResponse(self)
