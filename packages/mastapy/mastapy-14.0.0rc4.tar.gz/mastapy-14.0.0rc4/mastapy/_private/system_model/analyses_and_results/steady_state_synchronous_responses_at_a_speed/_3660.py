"""GearSteadyStateSynchronousResponseAtASpeed"""

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
    _3679,
)

_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "GearSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3606,
        _3613,
        _3614,
        _3615,
        _3618,
        _3625,
        _3631,
        _3634,
        _3649,
        _3650,
        _3655,
        _3664,
        _3668,
        _3671,
        _3674,
        _3681,
        _3703,
        _3710,
        _3713,
        _3714,
        _3715,
        _3728,
        _3731,
    )
    from mastapy._private.system_model.part_model.gears import _2587

    Self = TypeVar("Self", bound="GearSteadyStateSynchronousResponseAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSteadyStateSynchronousResponseAtASpeed._Cast_GearSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting GearSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "GearSteadyStateSynchronousResponseAtASpeed"

    @property
    def mountable_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3679.MountableComponentSteadyStateSynchronousResponseAtASpeed":
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
    def agma_gleason_conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3606.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3606,
        )

        return self.__parent__._cast(
            _3606.AGMAGleasonConicalGearSteadyStateSynchronousResponseAtASpeed
        )

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
    def concept_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3631.ConceptGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3631,
        )

        return self.__parent__._cast(
            _3631.ConceptGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3634.ConicalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3634,
        )

        return self.__parent__._cast(
            _3634.ConicalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3649.CylindricalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3649,
        )

        return self.__parent__._cast(
            _3649.CylindricalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_planet_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3650.CylindricalPlanetGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3650,
        )

        return self.__parent__._cast(
            _3650.CylindricalPlanetGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3655.FaceGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3655,
        )

        return self.__parent__._cast(
            _3655.FaceGearSteadyStateSynchronousResponseAtASpeed
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
    def klingelnberg_cyclo_palloid_conical_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3668.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3668,
        )

        return self.__parent__._cast(
            _3668.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3671.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3671,
        )

        return self.__parent__._cast(
            _3671.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3674.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3674,
        )

        return self.__parent__._cast(
            _3674.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseAtASpeed
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
    def worm_gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3728.WormGearSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3728,
        )

        return self.__parent__._cast(
            _3728.WormGearSteadyStateSynchronousResponseAtASpeed
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
    def gear_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "GearSteadyStateSynchronousResponseAtASpeed":
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
class GearSteadyStateSynchronousResponseAtASpeed(
    _3679.MountableComponentSteadyStateSynchronousResponseAtASpeed
):
    """GearSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2587.Gear":
        """mastapy.system_model.part_model.gears.Gear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_GearSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_GearSteadyStateSynchronousResponseAtASpeed(self)
