"""BevelGearMeshCompoundModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5374,
)

_BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "BevelGearMeshCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5253,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5381,
        _5402,
        _5404,
        _5428,
        _5434,
        _5471,
        _5477,
        _5480,
        _5498,
    )

    Self = TypeVar("Self", bound="BevelGearMeshCompoundModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearMeshCompoundModalAnalysisAtASpeed._Cast_BevelGearMeshCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshCompoundModalAnalysisAtASpeed:
    """Special nested class for casting BevelGearMeshCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "BevelGearMeshCompoundModalAnalysisAtASpeed"

    @property
    def agma_gleason_conical_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5374.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(
            _5374.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def conical_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5402.ConicalGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5402,
        )

        return self.__parent__._cast(_5402.ConicalGearMeshCompoundModalAnalysisAtASpeed)

    @property
    def gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5428.GearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5428,
        )

        return self.__parent__._cast(_5428.GearMeshCompoundModalAnalysisAtASpeed)

    @property
    def inter_mountable_component_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5434.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5434,
        )

        return self.__parent__._cast(
            _5434.InterMountableComponentConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5404.ConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5404,
        )

        return self.__parent__._cast(_5404.ConnectionCompoundModalAnalysisAtASpeed)

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
    def bevel_differential_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5381.BevelDifferentialGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5381,
        )

        return self.__parent__._cast(
            _5381.BevelDifferentialGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5471.SpiralBevelGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5471,
        )

        return self.__parent__._cast(
            _5471.SpiralBevelGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5477.StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5477,
        )

        return self.__parent__._cast(
            _5477.StraightBevelDiffGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5480.StraightBevelGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5480,
        )

        return self.__parent__._cast(
            _5480.StraightBevelGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5498.ZerolBevelGearMeshCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5498,
        )

        return self.__parent__._cast(
            _5498.ZerolBevelGearMeshCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "BevelGearMeshCompoundModalAnalysisAtASpeed":
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
class BevelGearMeshCompoundModalAnalysisAtASpeed(
    _5374.AGMAGleasonConicalGearMeshCompoundModalAnalysisAtASpeed
):
    """BevelGearMeshCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5253.BevelGearMeshModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.BevelGearMeshModalAnalysisAtASpeed]

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
    ) -> "List[_5253.BevelGearMeshModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.BevelGearMeshModalAnalysisAtASpeed]

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
    def cast_to(self: "Self") -> "_Cast_BevelGearMeshCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshCompoundModalAnalysisAtASpeed
        """
        return _Cast_BevelGearMeshCompoundModalAnalysisAtASpeed(self)
