"""PartSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717

_PART_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "PartSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3071,
        _3072,
        _3073,
        _3076,
        _3077,
        _3078,
        _3079,
        _3081,
        _3083,
        _3084,
        _3085,
        _3086,
        _3088,
        _3089,
        _3090,
        _3091,
        _3093,
        _3094,
        _3096,
        _3098,
        _3099,
        _3101,
        _3102,
        _3104,
        _3105,
        _3107,
        _3109,
        _3110,
        _3112,
        _3113,
        _3114,
        _3117,
        _3119,
        _3120,
        _3121,
        _3122,
        _3124,
        _3126,
        _3127,
        _3128,
        _3129,
        _3131,
        _3132,
        _3133,
        _3135,
        _3136,
        _3139,
        _3140,
        _3142,
        _3143,
        _3145,
        _3146,
        _3147,
        _3148,
        _3149,
        _3150,
        _3151,
        _3152,
        _3155,
        _3156,
        _3158,
        _3159,
        _3160,
        _3161,
        _3162,
        _3163,
        _3165,
        _3167,
        _3168,
        _3169,
        _3170,
        _3172,
        _3174,
        _3175,
        _3177,
        _3178,
        _3179,
        _3183,
        _3184,
        _3186,
        _3187,
        _3188,
        _3189,
        _3190,
        _3191,
        _3192,
        _3193,
        _3195,
        _3196,
        _3197,
        _3198,
        _3199,
        _3201,
        _3202,
        _3204,
        _3205,
    )
    from mastapy._private.system_model.part_model import _2525

    Self = TypeVar("Self", bound="PartSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartSteadyStateSynchronousResponse._Cast_PartSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartSteadyStateSynchronousResponse:
    """Special nested class for casting PartSteadyStateSynchronousResponse to subclasses."""

    __parent__: "PartSteadyStateSynchronousResponse"

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
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
    def abstract_shaft_or_housing_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3072.AbstractShaftOrHousingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3072,
        )

        return self.__parent__._cast(
            _3072.AbstractShaftOrHousingSteadyStateSynchronousResponse
        )

    @property
    def abstract_shaft_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3073.AbstractShaftSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3073,
        )

        return self.__parent__._cast(_3073.AbstractShaftSteadyStateSynchronousResponse)

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
    def agma_gleason_conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3077.AGMAGleasonConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3077,
        )

        return self.__parent__._cast(
            _3077.AGMAGleasonConicalGearSteadyStateSynchronousResponse
        )

    @property
    def assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3078.AssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3078,
        )

        return self.__parent__._cast(_3078.AssemblySteadyStateSynchronousResponse)

    @property
    def bearing_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3079.BearingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3079,
        )

        return self.__parent__._cast(_3079.BearingSteadyStateSynchronousResponse)

    @property
    def belt_drive_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3081.BeltDriveSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3081,
        )

        return self.__parent__._cast(_3081.BeltDriveSteadyStateSynchronousResponse)

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
    def bevel_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3088.BevelGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3088,
        )

        return self.__parent__._cast(_3088.BevelGearSetSteadyStateSynchronousResponse)

    @property
    def bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3089.BevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3089,
        )

        return self.__parent__._cast(_3089.BevelGearSteadyStateSynchronousResponse)

    @property
    def bolted_joint_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3090.BoltedJointSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3090,
        )

        return self.__parent__._cast(_3090.BoltedJointSteadyStateSynchronousResponse)

    @property
    def bolt_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3091.BoltSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3091,
        )

        return self.__parent__._cast(_3091.BoltSteadyStateSynchronousResponse)

    @property
    def clutch_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3093.ClutchHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3093,
        )

        return self.__parent__._cast(_3093.ClutchHalfSteadyStateSynchronousResponse)

    @property
    def clutch_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3094.ClutchSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3094,
        )

        return self.__parent__._cast(_3094.ClutchSteadyStateSynchronousResponse)

    @property
    def component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3096.ComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3096,
        )

        return self.__parent__._cast(_3096.ComponentSteadyStateSynchronousResponse)

    @property
    def concept_coupling_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3098.ConceptCouplingHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3098,
        )

        return self.__parent__._cast(
            _3098.ConceptCouplingHalfSteadyStateSynchronousResponse
        )

    @property
    def concept_coupling_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3099.ConceptCouplingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3099,
        )

        return self.__parent__._cast(
            _3099.ConceptCouplingSteadyStateSynchronousResponse
        )

    @property
    def concept_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3101.ConceptGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3101,
        )

        return self.__parent__._cast(_3101.ConceptGearSetSteadyStateSynchronousResponse)

    @property
    def concept_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3102.ConceptGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3102,
        )

        return self.__parent__._cast(_3102.ConceptGearSteadyStateSynchronousResponse)

    @property
    def conical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3104.ConicalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3104,
        )

        return self.__parent__._cast(_3104.ConicalGearSetSteadyStateSynchronousResponse)

    @property
    def conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3105.ConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3105,
        )

        return self.__parent__._cast(_3105.ConicalGearSteadyStateSynchronousResponse)

    @property
    def connector_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3107.ConnectorSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3107,
        )

        return self.__parent__._cast(_3107.ConnectorSteadyStateSynchronousResponse)

    @property
    def coupling_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3109.CouplingHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3109,
        )

        return self.__parent__._cast(_3109.CouplingHalfSteadyStateSynchronousResponse)

    @property
    def coupling_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3110.CouplingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3110,
        )

        return self.__parent__._cast(_3110.CouplingSteadyStateSynchronousResponse)

    @property
    def cvt_pulley_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3112.CVTPulleySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3112,
        )

        return self.__parent__._cast(_3112.CVTPulleySteadyStateSynchronousResponse)

    @property
    def cvt_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3113.CVTSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3113,
        )

        return self.__parent__._cast(_3113.CVTSteadyStateSynchronousResponse)

    @property
    def cycloidal_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3114.CycloidalAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3114,
        )

        return self.__parent__._cast(
            _3114.CycloidalAssemblySteadyStateSynchronousResponse
        )

    @property
    def cycloidal_disc_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3117.CycloidalDiscSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3117,
        )

        return self.__parent__._cast(_3117.CycloidalDiscSteadyStateSynchronousResponse)

    @property
    def cylindrical_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3119.CylindricalGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3119,
        )

        return self.__parent__._cast(
            _3119.CylindricalGearSetSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3120.CylindricalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3120,
        )

        return self.__parent__._cast(
            _3120.CylindricalGearSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_planet_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3121.CylindricalPlanetGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3121,
        )

        return self.__parent__._cast(
            _3121.CylindricalPlanetGearSteadyStateSynchronousResponse
        )

    @property
    def datum_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3122.DatumSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3122,
        )

        return self.__parent__._cast(_3122.DatumSteadyStateSynchronousResponse)

    @property
    def external_cad_model_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3124.ExternalCADModelSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3124,
        )

        return self.__parent__._cast(
            _3124.ExternalCADModelSteadyStateSynchronousResponse
        )

    @property
    def face_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3126.FaceGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3126,
        )

        return self.__parent__._cast(_3126.FaceGearSetSteadyStateSynchronousResponse)

    @property
    def face_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3127.FaceGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3127,
        )

        return self.__parent__._cast(_3127.FaceGearSteadyStateSynchronousResponse)

    @property
    def fe_part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3128.FEPartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3128,
        )

        return self.__parent__._cast(_3128.FEPartSteadyStateSynchronousResponse)

    @property
    def flexible_pin_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3129.FlexiblePinAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3129,
        )

        return self.__parent__._cast(
            _3129.FlexiblePinAssemblySteadyStateSynchronousResponse
        )

    @property
    def gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3131.GearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3131,
        )

        return self.__parent__._cast(_3131.GearSetSteadyStateSynchronousResponse)

    @property
    def gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3132.GearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3132,
        )

        return self.__parent__._cast(_3132.GearSteadyStateSynchronousResponse)

    @property
    def guide_dxf_model_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3133.GuideDxfModelSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3133,
        )

        return self.__parent__._cast(_3133.GuideDxfModelSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3135.HypoidGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3135,
        )

        return self.__parent__._cast(_3135.HypoidGearSetSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3136.HypoidGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3136,
        )

        return self.__parent__._cast(_3136.HypoidGearSteadyStateSynchronousResponse)

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
    def klingelnberg_cyclo_palloid_conical_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3140.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3140,
        )

        return self.__parent__._cast(
            _3140.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponse
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
    def klingelnberg_cyclo_palloid_hypoid_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3143.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3143,
        )

        return self.__parent__._cast(
            _3143.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponse
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
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3146.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3146,
        )

        return self.__parent__._cast(
            _3146.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponse
        )

    @property
    def mass_disc_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3147.MassDiscSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3147,
        )

        return self.__parent__._cast(_3147.MassDiscSteadyStateSynchronousResponse)

    @property
    def measurement_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3148.MeasurementComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3148,
        )

        return self.__parent__._cast(
            _3148.MeasurementComponentSteadyStateSynchronousResponse
        )

    @property
    def microphone_array_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3149.MicrophoneArraySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3149,
        )

        return self.__parent__._cast(
            _3149.MicrophoneArraySteadyStateSynchronousResponse
        )

    @property
    def microphone_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3150.MicrophoneSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3150,
        )

        return self.__parent__._cast(_3150.MicrophoneSteadyStateSynchronousResponse)

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
    def oil_seal_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3152.OilSealSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3152,
        )

        return self.__parent__._cast(_3152.OilSealSteadyStateSynchronousResponse)

    @property
    def part_to_part_shear_coupling_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3155.PartToPartShearCouplingHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3155,
        )

        return self.__parent__._cast(
            _3155.PartToPartShearCouplingHalfSteadyStateSynchronousResponse
        )

    @property
    def part_to_part_shear_coupling_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3156.PartToPartShearCouplingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3156,
        )

        return self.__parent__._cast(
            _3156.PartToPartShearCouplingSteadyStateSynchronousResponse
        )

    @property
    def planetary_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3158.PlanetaryGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3158,
        )

        return self.__parent__._cast(
            _3158.PlanetaryGearSetSteadyStateSynchronousResponse
        )

    @property
    def planet_carrier_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3159.PlanetCarrierSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3159,
        )

        return self.__parent__._cast(_3159.PlanetCarrierSteadyStateSynchronousResponse)

    @property
    def point_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3160.PointLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3160,
        )

        return self.__parent__._cast(_3160.PointLoadSteadyStateSynchronousResponse)

    @property
    def power_load_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3161.PowerLoadSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3161,
        )

        return self.__parent__._cast(_3161.PowerLoadSteadyStateSynchronousResponse)

    @property
    def pulley_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3162.PulleySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3162,
        )

        return self.__parent__._cast(_3162.PulleySteadyStateSynchronousResponse)

    @property
    def ring_pins_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3163.RingPinsSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3163,
        )

        return self.__parent__._cast(_3163.RingPinsSteadyStateSynchronousResponse)

    @property
    def rolling_ring_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3165.RollingRingAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3165,
        )

        return self.__parent__._cast(
            _3165.RollingRingAssemblySteadyStateSynchronousResponse
        )

    @property
    def rolling_ring_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3167.RollingRingSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3167,
        )

        return self.__parent__._cast(_3167.RollingRingSteadyStateSynchronousResponse)

    @property
    def root_assembly_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3168.RootAssemblySteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3168,
        )

        return self.__parent__._cast(_3168.RootAssemblySteadyStateSynchronousResponse)

    @property
    def shaft_hub_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3169.ShaftHubConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3169,
        )

        return self.__parent__._cast(
            _3169.ShaftHubConnectionSteadyStateSynchronousResponse
        )

    @property
    def shaft_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3170.ShaftSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3170,
        )

        return self.__parent__._cast(_3170.ShaftSteadyStateSynchronousResponse)

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
    def spring_damper_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3177.SpringDamperHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3177,
        )

        return self.__parent__._cast(
            _3177.SpringDamperHalfSteadyStateSynchronousResponse
        )

    @property
    def spring_damper_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3178.SpringDamperSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3178,
        )

        return self.__parent__._cast(_3178.SpringDamperSteadyStateSynchronousResponse)

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
    def synchroniser_half_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3190.SynchroniserHalfSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3190,
        )

        return self.__parent__._cast(
            _3190.SynchroniserHalfSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3191.SynchroniserPartSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3191,
        )

        return self.__parent__._cast(
            _3191.SynchroniserPartSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_sleeve_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3192.SynchroniserSleeveSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3192,
        )

        return self.__parent__._cast(
            _3192.SynchroniserSleeveSteadyStateSynchronousResponse
        )

    @property
    def synchroniser_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3193.SynchroniserSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3193,
        )

        return self.__parent__._cast(_3193.SynchroniserSteadyStateSynchronousResponse)

    @property
    def torque_converter_pump_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3195.TorqueConverterPumpSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3195,
        )

        return self.__parent__._cast(
            _3195.TorqueConverterPumpSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3196.TorqueConverterSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3196,
        )

        return self.__parent__._cast(
            _3196.TorqueConverterSteadyStateSynchronousResponse
        )

    @property
    def torque_converter_turbine_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3197.TorqueConverterTurbineSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3197,
        )

        return self.__parent__._cast(
            _3197.TorqueConverterTurbineSteadyStateSynchronousResponse
        )

    @property
    def unbalanced_mass_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3198.UnbalancedMassSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3198,
        )

        return self.__parent__._cast(_3198.UnbalancedMassSteadyStateSynchronousResponse)

    @property
    def virtual_component_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3199.VirtualComponentSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3199,
        )

        return self.__parent__._cast(
            _3199.VirtualComponentSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_set_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3201.WormGearSetSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3201,
        )

        return self.__parent__._cast(_3201.WormGearSetSteadyStateSynchronousResponse)

    @property
    def worm_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3202.WormGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3202,
        )

        return self.__parent__._cast(_3202.WormGearSteadyStateSynchronousResponse)

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
    def zerol_bevel_gear_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3205.ZerolBevelGearSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3205,
        )

        return self.__parent__._cast(_3205.ZerolBevelGearSteadyStateSynchronousResponse)

    @property
    def part_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "PartSteadyStateSynchronousResponse":
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
class PartSteadyStateSynchronousResponse(_7717.PartStaticLoadAnalysisCase):
    """PartSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2525.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def steady_state_synchronous_response(
        self: "Self",
    ) -> "_3179.SteadyStateSynchronousResponse":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.SteadyStateSynchronousResponse

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SteadyStateSynchronousResponse")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PartSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_PartSteadyStateSynchronousResponse
        """
        return _Cast_PartSteadyStateSynchronousResponse(self)
