"""InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"""

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
    _3241,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3137,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3211,
        _3215,
        _3218,
        _3223,
        _3228,
        _3233,
        _3236,
        _3239,
        _3244,
        _3246,
        _3254,
        _3260,
        _3265,
        _3269,
        _3273,
        _3276,
        _3279,
        _3289,
        _3298,
        _3301,
        _3308,
        _3311,
        _3314,
        _3317,
        _3326,
        _3332,
        _3335,
    )

    Self = TypeVar(
        "Self",
        bound="InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse._Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: (
        "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"
    )

    @property
    def connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3241.ConnectionCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3241.ConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7708.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7708,
        )

        return self.__parent__._cast(_7708.ConnectionCompoundAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3211.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3211,
        )

        return self.__parent__._cast(
            _3211.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def belt_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3215.BeltConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3215,
        )

        return self.__parent__._cast(
            _3215.BeltConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3218.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3218,
        )

        return self.__parent__._cast(
            _3218.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3223.BevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3223,
        )

        return self.__parent__._cast(
            _3223.BevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def clutch_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3228.ClutchConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3228,
        )

        return self.__parent__._cast(
            _3228.ClutchConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def concept_coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3233.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3233,
        )

        return self.__parent__._cast(
            _3233.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3236.ConceptGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3236,
        )

        return self.__parent__._cast(
            _3236.ConceptGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3239.ConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3239,
        )

        return self.__parent__._cast(
            _3239.ConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3244.CouplingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3244,
        )

        return self.__parent__._cast(
            _3244.CouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def cvt_belt_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3246.CVTBeltConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3246,
        )

        return self.__parent__._cast(
            _3246.CVTBeltConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3254.CylindricalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3254,
        )

        return self.__parent__._cast(
            _3254.CylindricalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def face_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3260.FaceGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3260,
        )

        return self.__parent__._cast(
            _3260.FaceGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3265.GearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3265,
        )

        return self.__parent__._cast(
            _3265.GearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def hypoid_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3269.HypoidGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3269,
        )

        return self.__parent__._cast(
            _3269.HypoidGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3273.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3273,
        )

        return self.__parent__._cast(
            _3273.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3276.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3276,
        )

        return self.__parent__._cast(
            _3276.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3279.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3279,
        )

        return self.__parent__._cast(
            _3279.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> (
        "_3289.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3289,
        )

        return self.__parent__._cast(
            _3289.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def ring_pins_to_disc_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3298.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3298,
        )

        return self.__parent__._cast(
            _3298.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3301.RollingRingConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3301,
        )

        return self.__parent__._cast(
            _3301.RollingRingConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3308.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3308,
        )

        return self.__parent__._cast(
            _3308.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3311.SpringDamperConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3311,
        )

        return self.__parent__._cast(
            _3311.SpringDamperConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3314.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3314,
        )

        return self.__parent__._cast(
            _3314.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3317.StraightBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3317,
        )

        return self.__parent__._cast(
            _3317.StraightBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3326.TorqueConverterConnectionCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3326,
        )

        return self.__parent__._cast(
            _3326.TorqueConverterConnectionCompoundSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3332.WormGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3332,
        )

        return self.__parent__._cast(
            _3332.WormGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_mesh_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3335.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3335,
        )

        return self.__parent__._cast(
            _3335.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponse
        )

    @property
    def inter_mountable_component_connection_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse":
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
class InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse(
    _3241.ConnectionCompoundSteadyStateSynchronousResponse
):
    """InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3137.InterMountableComponentConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.InterMountableComponentConnectionSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3137.InterMountableComponentConnectionSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.InterMountableComponentConnectionSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> (
        "_Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse"
    ):
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse
        """
        return _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponse(
            self
        )
