"""ConicalGearSetSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3131,
)

_CONICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "ConicalGearSetSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3071,
        _3076,
        _3083,
        _3088,
        _3103,
        _3105,
        _3135,
        _3139,
        _3142,
        _3145,
        _3153,
        _3172,
        _3174,
        _3183,
        _3186,
        _3204,
    )
    from mastapy._private.system_model.part_model.gears import _2581

    Self = TypeVar("Self", bound="ConicalGearSetSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetSteadyStateSynchronousResponse._Cast_ConicalGearSetSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetSteadyStateSynchronousResponse:
    """Special nested class for casting ConicalGearSetSteadyStateSynchronousResponse to subclasses."""

    __parent__: "ConicalGearSetSteadyStateSynchronousResponse"

    @property
    def gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3131.GearSetSteadyStateSynchronousResponse":
        return self.__parent__._cast(_3131.GearSetSteadyStateSynchronousResponse)

    @property
    def specialised_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3172.SpecialisedAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3172,
        )

        return self.__parent__._cast(
            _3172.SpecialisedAssemblySteadyStateSynchronousResponse
        )

    @property
    def abstract_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3071.AbstractAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3071,
        )

        return self.__parent__._cast(
            _3071.AbstractAssemblySteadyStateSynchronousResponse
        )

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
    def agma_gleason_conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3076.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3076,
        )

        return self.__parent__._cast(
            _3076.AGMAGleasonConicalGearSetSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3083.BevelDifferentialGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3083,
        )

        return self.__parent__._cast(
            _3083.BevelDifferentialGearSetSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3088.BevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3088,
        )

        return self.__parent__._cast(_3088.BevelGearSetSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3135.HypoidGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3135,
        )

        return self.__parent__._cast(_3135.HypoidGearSetSteadyStateSynchronousResponse)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3139.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3139,
        )

        return self.__parent__._cast(
            _3139.KlingelnbergCycloPalloidConicalGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3142.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3142,
        )

        return self.__parent__._cast(
            _3142.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3145.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3145,
        )

        return self.__parent__._cast(
            _3145.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3174.SpiralBevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3174,
        )

        return self.__parent__._cast(
            _3174.SpiralBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3183.StraightBevelDiffGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3183,
        )

        return self.__parent__._cast(
            _3183.StraightBevelDiffGearSetSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3186.StraightBevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3186,
        )

        return self.__parent__._cast(
            _3186.StraightBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3204.ZerolBevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3204,
        )

        return self.__parent__._cast(
            _3204.ZerolBevelGearSetSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "ConicalGearSetSteadyStateSynchronousResponse":
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
class ConicalGearSetSteadyStateSynchronousResponse(
    _3131.GearSetSteadyStateSynchronousResponse
):
    """ConicalGearSetSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2581.ConicalGearSet":
        """mastapy.system_model.part_model.gears.ConicalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3105.ConicalGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ConicalGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GearsSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_gears_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3105.ConicalGearSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ConicalGearSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConicalGearsSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3103.ConicalGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ConicalGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeshesSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_meshes_steady_state_synchronous_response(
        self: "Self",
    ) -> "List[_3103.ConicalGearMeshSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ConicalGearMeshSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConicalMeshesSteadyStateSynchronousResponse"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetSteadyStateSynchronousResponse
        """
        return _Cast_ConicalGearSetSteadyStateSynchronousResponse(self)
