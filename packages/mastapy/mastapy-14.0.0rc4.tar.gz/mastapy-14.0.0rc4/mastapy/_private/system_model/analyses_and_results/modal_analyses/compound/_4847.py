"""AGMAGleasonConicalGearMeshCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4875,
)

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "AGMAGleasonConicalGearMeshCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4688
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4854,
        _4859,
        _4877,
        _4901,
        _4905,
        _4907,
        _4944,
        _4950,
        _4953,
        _4971,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshCompoundModalAnalysis._Cast_AGMAGleasonConicalGearMeshCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshCompoundModalAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearMeshCompoundModalAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshCompoundModalAnalysis"

    @property
    def conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4875.ConicalGearMeshCompoundModalAnalysis":
        return self.__parent__._cast(_4875.ConicalGearMeshCompoundModalAnalysis)

    @property
    def gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4901.GearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4901,
        )

        return self.__parent__._cast(_4901.GearMeshCompoundModalAnalysis)

    @property
    def inter_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4907.InterMountableComponentConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4907,
        )

        return self.__parent__._cast(
            _4907.InterMountableComponentConnectionCompoundModalAnalysis
        )

    @property
    def connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4877.ConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4877,
        )

        return self.__parent__._cast(_4877.ConnectionCompoundModalAnalysis)

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
    def bevel_differential_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4854.BevelDifferentialGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4854,
        )

        return self.__parent__._cast(
            _4854.BevelDifferentialGearMeshCompoundModalAnalysis
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4859.BevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4859,
        )

        return self.__parent__._cast(_4859.BevelGearMeshCompoundModalAnalysis)

    @property
    def hypoid_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4905.HypoidGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4905,
        )

        return self.__parent__._cast(_4905.HypoidGearMeshCompoundModalAnalysis)

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4944.SpiralBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4944,
        )

        return self.__parent__._cast(_4944.SpiralBevelGearMeshCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4950.StraightBevelDiffGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4950,
        )

        return self.__parent__._cast(
            _4950.StraightBevelDiffGearMeshCompoundModalAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4953.StraightBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4953,
        )

        return self.__parent__._cast(_4953.StraightBevelGearMeshCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4971.ZerolBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4971,
        )

        return self.__parent__._cast(_4971.ZerolBevelGearMeshCompoundModalAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshCompoundModalAnalysis":
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
class AGMAGleasonConicalGearMeshCompoundModalAnalysis(
    _4875.ConicalGearMeshCompoundModalAnalysis
):
    """AGMAGleasonConicalGearMeshCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4688.AGMAGleasonConicalGearMeshModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearMeshModalAnalysis]

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
    ) -> "List[_4688.AGMAGleasonConicalGearMeshModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.AGMAGleasonConicalGearMeshModalAnalysis]

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
    ) -> "_Cast_AGMAGleasonConicalGearMeshCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshCompoundModalAnalysis
        """
        return _Cast_AGMAGleasonConicalGearMeshCompoundModalAnalysis(self)
