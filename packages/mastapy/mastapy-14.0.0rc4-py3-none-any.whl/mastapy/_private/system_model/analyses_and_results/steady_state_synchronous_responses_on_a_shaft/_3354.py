"""BevelGearSetSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
    _3342,
)

_BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "BevelGearSetSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3337,
        _3349,
        _3353,
        _3355,
        _3370,
        _3396,
        _3418,
        _3437,
        _3439,
        _3446,
        _3449,
        _3467,
    )
    from mastapy._private.system_model.part_model.gears import _2577

    Self = TypeVar("Self", bound="BevelGearSetSteadyStateSynchronousResponseOnAShaft")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearSetSteadyStateSynchronousResponseOnAShaft._Cast_BevelGearSetSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearSetSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting BevelGearSetSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "BevelGearSetSteadyStateSynchronousResponseOnAShaft"

    @property
    def agma_gleason_conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3342.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3342.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3370.ConicalGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3370,
        )

        return self.__parent__._cast(
            _3370.ConicalGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3396.GearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3396,
        )

        return self.__parent__._cast(
            _3396.GearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def specialised_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3437.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3437,
        )

        return self.__parent__._cast(
            _3437.SpecialisedAssemblySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_assembly_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3337.AbstractAssemblySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3337,
        )

        return self.__parent__._cast(
            _3337.AbstractAssemblySteadyStateSynchronousResponseOnAShaft
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
    def bevel_differential_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3349.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3349,
        )

        return self.__parent__._cast(
            _3349.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3439.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3439,
        )

        return self.__parent__._cast(
            _3439.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3446.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3446,
        )

        return self.__parent__._cast(
            _3446.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3449.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3449,
        )

        return self.__parent__._cast(
            _3449.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3467.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3467,
        )

        return self.__parent__._cast(
            _3467.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_set_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "BevelGearSetSteadyStateSynchronousResponseOnAShaft":
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
class BevelGearSetSteadyStateSynchronousResponseOnAShaft(
    _3342.AGMAGleasonConicalGearSetSteadyStateSynchronousResponseOnAShaft
):
    """BevelGearSetSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _BEVEL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2577.BevelGearSet":
        """mastapy.system_model.part_model.gears.BevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def agma_gleason_conical_gears_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3355.BevelGearSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.BevelGearSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AGMAGleasonConicalGearsSteadyStateSynchronousResponseOnAShaft",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_gears_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3355.BevelGearSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.BevelGearSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelGearsSteadyStateSynchronousResponseOnAShaft"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def agma_gleason_conical_meshes_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3353.BevelGearMeshSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.BevelGearMeshSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AGMAGleasonConicalMeshesSteadyStateSynchronousResponseOnAShaft",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_meshes_steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "List[_3353.BevelGearMeshSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.BevelGearMeshSteadyStateSynchronousResponseOnAShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelMeshesSteadyStateSynchronousResponseOnAShaft"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_BevelGearSetSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_BevelGearSetSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_BevelGearSetSteadyStateSynchronousResponseOnAShaft(self)
