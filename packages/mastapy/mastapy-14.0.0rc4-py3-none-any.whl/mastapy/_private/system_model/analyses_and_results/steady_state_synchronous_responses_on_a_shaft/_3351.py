"""BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft"""

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
    _3350,
)

_BEVEL_DIFFERENTIAL_PLANET_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3343,
        _3355,
        _3362,
        _3371,
        _3397,
        _3416,
        _3418,
    )
    from mastapy._private.system_model.part_model.gears import _2574

    Self = TypeVar(
        "Self",
        bound="BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft._Cast_BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft"

    @property
    def bevel_differential_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3350.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3350.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3355.BevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3355,
        )

        return self.__parent__._cast(
            _3355.BevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3343.AGMAGleasonConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3343,
        )

        return self.__parent__._cast(
            _3343.AGMAGleasonConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3371.ConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3371,
        )

        return self.__parent__._cast(
            _3371.ConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3397.GearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3397,
        )

        return self.__parent__._cast(_3397.GearSteadyStateSynchronousResponseOnAShaft)

    @property
    def mountable_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3416.MountableComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3416,
        )

        return self.__parent__._cast(
            _3416.MountableComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3362.ComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3362,
        )

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
    def bevel_differential_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft":
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
class BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft(
    _3350.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft
):
    """BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _BEVEL_DIFFERENTIAL_PLANET_GEAR_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2574.BevelDifferentialPlanetGear":
        """mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear

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
    ) -> "_Cast_BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft(
            self
        )
