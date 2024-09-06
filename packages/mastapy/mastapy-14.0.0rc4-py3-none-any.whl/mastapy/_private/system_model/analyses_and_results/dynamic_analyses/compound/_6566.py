"""BevelGearMeshCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6554,
)

_BEVEL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "BevelGearMeshCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6433,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6561,
        _6582,
        _6584,
        _6608,
        _6614,
        _6651,
        _6657,
        _6660,
        _6678,
    )

    Self = TypeVar("Self", bound="BevelGearMeshCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearMeshCompoundDynamicAnalysis._Cast_BevelGearMeshCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshCompoundDynamicAnalysis:
    """Special nested class for casting BevelGearMeshCompoundDynamicAnalysis to subclasses."""

    __parent__: "BevelGearMeshCompoundDynamicAnalysis"

    @property
    def agma_gleason_conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6554.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis":
        return self.__parent__._cast(
            _6554.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis
        )

    @property
    def conical_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6582.ConicalGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6582,
        )

        return self.__parent__._cast(_6582.ConicalGearMeshCompoundDynamicAnalysis)

    @property
    def gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6608.GearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6608,
        )

        return self.__parent__._cast(_6608.GearMeshCompoundDynamicAnalysis)

    @property
    def inter_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6614.InterMountableComponentConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6614,
        )

        return self.__parent__._cast(
            _6614.InterMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6584.ConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6584,
        )

        return self.__parent__._cast(_6584.ConnectionCompoundDynamicAnalysis)

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
    def bevel_differential_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6561.BevelDifferentialGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6561,
        )

        return self.__parent__._cast(
            _6561.BevelDifferentialGearMeshCompoundDynamicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6651.SpiralBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6651,
        )

        return self.__parent__._cast(_6651.SpiralBevelGearMeshCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6657.StraightBevelDiffGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6657,
        )

        return self.__parent__._cast(
            _6657.StraightBevelDiffGearMeshCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6660.StraightBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6660,
        )

        return self.__parent__._cast(_6660.StraightBevelGearMeshCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6678.ZerolBevelGearMeshCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6678,
        )

        return self.__parent__._cast(_6678.ZerolBevelGearMeshCompoundDynamicAnalysis)

    @property
    def bevel_gear_mesh_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "BevelGearMeshCompoundDynamicAnalysis":
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
class BevelGearMeshCompoundDynamicAnalysis(
    _6554.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis
):
    """BevelGearMeshCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6433.BevelGearMeshDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearMeshDynamicAnalysis]

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
    ) -> "List[_6433.BevelGearMeshDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearMeshDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_BevelGearMeshCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshCompoundDynamicAnalysis
        """
        return _Cast_BevelGearMeshCompoundDynamicAnalysis(self)
