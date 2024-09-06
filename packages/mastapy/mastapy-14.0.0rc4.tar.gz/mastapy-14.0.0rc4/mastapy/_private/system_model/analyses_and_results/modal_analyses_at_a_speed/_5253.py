"""BevelGearMeshModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5241,
)

_BEVEL_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "BevelGearMeshModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5248,
        _5269,
        _5272,
        _5295,
        _5302,
        _5339,
        _5345,
        _5348,
        _5366,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2357

    Self = TypeVar("Self", bound="BevelGearMeshModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearMeshModalAnalysisAtASpeed._Cast_BevelGearMeshModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshModalAnalysisAtASpeed:
    """Special nested class for casting BevelGearMeshModalAnalysisAtASpeed to subclasses."""

    __parent__: "BevelGearMeshModalAnalysisAtASpeed"

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5241.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed":
        return self.__parent__._cast(
            _5241.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed
        )

    @property
    def conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5269.ConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5269,
        )

        return self.__parent__._cast(_5269.ConicalGearMeshModalAnalysisAtASpeed)

    @property
    def gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5295.GearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5295,
        )

        return self.__parent__._cast(_5295.GearMeshModalAnalysisAtASpeed)

    @property
    def inter_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5302.InterMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5302,
        )

        return self.__parent__._cast(
            _5302.InterMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5272.ConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5272,
        )

        return self.__parent__._cast(_5272.ConnectionModalAnalysisAtASpeed)

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
    def bevel_differential_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5248.BevelDifferentialGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5248,
        )

        return self.__parent__._cast(
            _5248.BevelDifferentialGearMeshModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5339.SpiralBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5339,
        )

        return self.__parent__._cast(_5339.SpiralBevelGearMeshModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5345.StraightBevelDiffGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5345,
        )

        return self.__parent__._cast(
            _5345.StraightBevelDiffGearMeshModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5348.StraightBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5348,
        )

        return self.__parent__._cast(_5348.StraightBevelGearMeshModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5366.ZerolBevelGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5366,
        )

        return self.__parent__._cast(_5366.ZerolBevelGearMeshModalAnalysisAtASpeed)

    @property
    def bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "BevelGearMeshModalAnalysisAtASpeed":
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
class BevelGearMeshModalAnalysisAtASpeed(
    _5241.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed
):
    """BevelGearMeshModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2357.BevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.BevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearMeshModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshModalAnalysisAtASpeed
        """
        return _Cast_BevelGearMeshModalAnalysisAtASpeed(self)
