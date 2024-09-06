"""InterMountableComponentConnectionModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _5008,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
    "InterMountableComponentConnectionModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _4977,
        _4982,
        _4984,
        _4989,
        _4994,
        _4999,
        _5002,
        _5005,
        _5010,
        _5013,
        _5020,
        _5027,
        _5032,
        _5036,
        _5040,
        _5043,
        _5046,
        _5057,
        _5067,
        _5069,
        _5076,
        _5079,
        _5082,
        _5085,
        _5094,
        _5100,
        _5103,
    )
    from mastapy._private.system_model.connections_and_sockets import _2335

    Self = TypeVar(
        "Self", bound="InterMountableComponentConnectionModalAnalysisAtAStiffness"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionModalAnalysisAtAStiffness._Cast_InterMountableComponentConnectionModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionModalAnalysisAtAStiffness:
    """Special nested class for casting InterMountableComponentConnectionModalAnalysisAtAStiffness to subclasses."""

    __parent__: "InterMountableComponentConnectionModalAnalysisAtAStiffness"

    @property
    def connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5008.ConnectionModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5008.ConnectionModalAnalysisAtAStiffness)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7710.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7707.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7707,
        )

        return self.__parent__._cast(_7707.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2733.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2733

        return self.__parent__._cast(_2733.ConnectionAnalysis)

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
    def agma_gleason_conical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4977.AGMAGleasonConicalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4977,
        )

        return self.__parent__._cast(
            _4977.AGMAGleasonConicalGearMeshModalAnalysisAtAStiffness
        )

    @property
    def belt_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4982.BeltConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4982,
        )

        return self.__parent__._cast(_4982.BeltConnectionModalAnalysisAtAStiffness)

    @property
    def bevel_differential_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4984.BevelDifferentialGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4984,
        )

        return self.__parent__._cast(
            _4984.BevelDifferentialGearMeshModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4989.BevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4989,
        )

        return self.__parent__._cast(_4989.BevelGearMeshModalAnalysisAtAStiffness)

    @property
    def clutch_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4994.ClutchConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4994,
        )

        return self.__parent__._cast(_4994.ClutchConnectionModalAnalysisAtAStiffness)

    @property
    def concept_coupling_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4999.ConceptCouplingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4999,
        )

        return self.__parent__._cast(
            _4999.ConceptCouplingConnectionModalAnalysisAtAStiffness
        )

    @property
    def concept_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5002.ConceptGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5002,
        )

        return self.__parent__._cast(_5002.ConceptGearMeshModalAnalysisAtAStiffness)

    @property
    def conical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5005.ConicalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5005,
        )

        return self.__parent__._cast(_5005.ConicalGearMeshModalAnalysisAtAStiffness)

    @property
    def coupling_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5010.CouplingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5010,
        )

        return self.__parent__._cast(_5010.CouplingConnectionModalAnalysisAtAStiffness)

    @property
    def cvt_belt_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5013.CVTBeltConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5013,
        )

        return self.__parent__._cast(_5013.CVTBeltConnectionModalAnalysisAtAStiffness)

    @property
    def cylindrical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5020.CylindricalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5020,
        )

        return self.__parent__._cast(_5020.CylindricalGearMeshModalAnalysisAtAStiffness)

    @property
    def face_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5027.FaceGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5027,
        )

        return self.__parent__._cast(_5027.FaceGearMeshModalAnalysisAtAStiffness)

    @property
    def gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5032.GearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5032,
        )

        return self.__parent__._cast(_5032.GearMeshModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5036.HypoidGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5036,
        )

        return self.__parent__._cast(_5036.HypoidGearMeshModalAnalysisAtAStiffness)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5040.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5040,
        )

        return self.__parent__._cast(
            _5040.KlingelnbergCycloPalloidConicalGearMeshModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5043.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5043,
        )

        return self.__parent__._cast(
            _5043.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5046.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5046,
        )

        return self.__parent__._cast(
            _5046.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5057.PartToPartShearCouplingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5057,
        )

        return self.__parent__._cast(
            _5057.PartToPartShearCouplingConnectionModalAnalysisAtAStiffness
        )

    @property
    def ring_pins_to_disc_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5067.RingPinsToDiscConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5067,
        )

        return self.__parent__._cast(
            _5067.RingPinsToDiscConnectionModalAnalysisAtAStiffness
        )

    @property
    def rolling_ring_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5069.RollingRingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5069,
        )

        return self.__parent__._cast(
            _5069.RollingRingConnectionModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5076.SpiralBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5076,
        )

        return self.__parent__._cast(_5076.SpiralBevelGearMeshModalAnalysisAtAStiffness)

    @property
    def spring_damper_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5079.SpringDamperConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5079,
        )

        return self.__parent__._cast(
            _5079.SpringDamperConnectionModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5082.StraightBevelDiffGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5082,
        )

        return self.__parent__._cast(
            _5082.StraightBevelDiffGearMeshModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5085.StraightBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5085,
        )

        return self.__parent__._cast(
            _5085.StraightBevelGearMeshModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5094.TorqueConverterConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5094,
        )

        return self.__parent__._cast(
            _5094.TorqueConverterConnectionModalAnalysisAtAStiffness
        )

    @property
    def worm_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5100.WormGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5100,
        )

        return self.__parent__._cast(_5100.WormGearMeshModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_mesh_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5103.ZerolBevelGearMeshModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5103,
        )

        return self.__parent__._cast(_5103.ZerolBevelGearMeshModalAnalysisAtAStiffness)

    @property
    def inter_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionModalAnalysisAtAStiffness":
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
class InterMountableComponentConnectionModalAnalysisAtAStiffness(
    _5008.ConnectionModalAnalysisAtAStiffness
):
    """InterMountableComponentConnectionModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2335.InterMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.InterMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionModalAnalysisAtAStiffness
        """
        return _Cast_InterMountableComponentConnectionModalAnalysisAtAStiffness(self)
