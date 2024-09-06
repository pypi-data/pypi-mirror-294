"""GearMeshCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4064,
)

_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "GearMeshCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3923,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4004,
        _4011,
        _4016,
        _4029,
        _4032,
        _4034,
        _4047,
        _4053,
        _4062,
        _4066,
        _4069,
        _4072,
        _4101,
        _4107,
        _4110,
        _4125,
        _4128,
    )

    Self = TypeVar("Self", bound="GearMeshCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshCompoundStabilityAnalysis._Cast_GearMeshCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshCompoundStabilityAnalysis:
    """Special nested class for casting GearMeshCompoundStabilityAnalysis to subclasses."""

    __parent__: "GearMeshCompoundStabilityAnalysis"

    @property
    def inter_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4064.InterMountableComponentConnectionCompoundStabilityAnalysis":
        return self.__parent__._cast(
            _4064.InterMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4034.ConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4034,
        )

        return self.__parent__._cast(_4034.ConnectionCompoundStabilityAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4004.AGMAGleasonConicalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4004,
        )

        return self.__parent__._cast(
            _4004.AGMAGleasonConicalGearMeshCompoundStabilityAnalysis
        )

    @property
    def bevel_differential_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4011.BevelDifferentialGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4011,
        )

        return self.__parent__._cast(
            _4011.BevelDifferentialGearMeshCompoundStabilityAnalysis
        )

    @property
    def bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4016.BevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4016,
        )

        return self.__parent__._cast(_4016.BevelGearMeshCompoundStabilityAnalysis)

    @property
    def concept_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4029.ConceptGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4029,
        )

        return self.__parent__._cast(_4029.ConceptGearMeshCompoundStabilityAnalysis)

    @property
    def conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4032.ConicalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4032,
        )

        return self.__parent__._cast(_4032.ConicalGearMeshCompoundStabilityAnalysis)

    @property
    def cylindrical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4047.CylindricalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4047,
        )

        return self.__parent__._cast(_4047.CylindricalGearMeshCompoundStabilityAnalysis)

    @property
    def face_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4053.FaceGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4053,
        )

        return self.__parent__._cast(_4053.FaceGearMeshCompoundStabilityAnalysis)

    @property
    def hypoid_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4062.HypoidGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4062,
        )

        return self.__parent__._cast(_4062.HypoidGearMeshCompoundStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4066.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4066,
        )

        return self.__parent__._cast(
            _4066.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4069.KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4069,
        )

        return self.__parent__._cast(
            _4069.KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4072.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4072,
        )

        return self.__parent__._cast(
            _4072.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundStabilityAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4101.SpiralBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4101,
        )

        return self.__parent__._cast(_4101.SpiralBevelGearMeshCompoundStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4107.StraightBevelDiffGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4107,
        )

        return self.__parent__._cast(
            _4107.StraightBevelDiffGearMeshCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4110.StraightBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4110,
        )

        return self.__parent__._cast(
            _4110.StraightBevelGearMeshCompoundStabilityAnalysis
        )

    @property
    def worm_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4125.WormGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4125,
        )

        return self.__parent__._cast(_4125.WormGearMeshCompoundStabilityAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4128.ZerolBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4128,
        )

        return self.__parent__._cast(_4128.ZerolBevelGearMeshCompoundStabilityAnalysis)

    @property
    def gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "GearMeshCompoundStabilityAnalysis":
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
class GearMeshCompoundStabilityAnalysis(
    _4064.InterMountableComponentConnectionCompoundStabilityAnalysis
):
    """GearMeshCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3923.GearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.GearMeshStabilityAnalysis]

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
    ) -> "List[_3923.GearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.GearMeshStabilityAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_GearMeshCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshCompoundStabilityAnalysis
        """
        return _Cast_GearMeshCompoundStabilityAnalysis(self)
