"""GearMeshHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5905

_GEAR_MESH_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "GearMeshHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5815,
        _5822,
        _5827,
        _5841,
        _5844,
        _5846,
        _5859,
        _5879,
        _5903,
        _5907,
        _5910,
        _5913,
        _5946,
        _5953,
        _5956,
        _5972,
        _5975,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4260
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2843,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2367

    Self = TypeVar("Self", bound="GearMeshHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshHarmonicAnalysis._Cast_GearMeshHarmonicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshHarmonicAnalysis:
    """Special nested class for casting GearMeshHarmonicAnalysis to subclasses."""

    __parent__: "GearMeshHarmonicAnalysis"

    @property
    def inter_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5905.InterMountableComponentConnectionHarmonicAnalysis":
        return self.__parent__._cast(
            _5905.InterMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5846.ConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5846,
        )

        return self.__parent__._cast(_5846.ConnectionHarmonicAnalysis)

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
    def agma_gleason_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5815.AGMAGleasonConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5815,
        )

        return self.__parent__._cast(_5815.AGMAGleasonConicalGearMeshHarmonicAnalysis)

    @property
    def bevel_differential_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5822.BevelDifferentialGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5822,
        )

        return self.__parent__._cast(_5822.BevelDifferentialGearMeshHarmonicAnalysis)

    @property
    def bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5827.BevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5827,
        )

        return self.__parent__._cast(_5827.BevelGearMeshHarmonicAnalysis)

    @property
    def concept_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5841.ConceptGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5841,
        )

        return self.__parent__._cast(_5841.ConceptGearMeshHarmonicAnalysis)

    @property
    def conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5844.ConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5844,
        )

        return self.__parent__._cast(_5844.ConicalGearMeshHarmonicAnalysis)

    @property
    def cylindrical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5859.CylindricalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5859,
        )

        return self.__parent__._cast(_5859.CylindricalGearMeshHarmonicAnalysis)

    @property
    def face_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5879.FaceGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5879,
        )

        return self.__parent__._cast(_5879.FaceGearMeshHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5903.HypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5903,
        )

        return self.__parent__._cast(_5903.HypoidGearMeshHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5907.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5907,
        )

        return self.__parent__._cast(
            _5907.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5910.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5910,
        )

        return self.__parent__._cast(
            _5910.KlingelnbergCycloPalloidHypoidGearMeshHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5913.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5913,
        )

        return self.__parent__._cast(
            _5913.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5946.SpiralBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5946,
        )

        return self.__parent__._cast(_5946.SpiralBevelGearMeshHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5953.StraightBevelDiffGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5953,
        )

        return self.__parent__._cast(_5953.StraightBevelDiffGearMeshHarmonicAnalysis)

    @property
    def straight_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5956.StraightBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5956,
        )

        return self.__parent__._cast(_5956.StraightBevelGearMeshHarmonicAnalysis)

    @property
    def worm_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5972.WormGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5972,
        )

        return self.__parent__._cast(_5972.WormGearMeshHarmonicAnalysis)

    @property
    def zerol_bevel_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5975.ZerolBevelGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5975,
        )

        return self.__parent__._cast(_5975.ZerolBevelGearMeshHarmonicAnalysis)

    @property
    def gear_mesh_harmonic_analysis(self: "CastSelf") -> "GearMeshHarmonicAnalysis":
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
class GearMeshHarmonicAnalysis(_5905.InterMountableComponentConnectionHarmonicAnalysis):
    """GearMeshHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def set_user_specified_te_from_file(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "SetUserSpecifiedTEFromFile")

        if temp is None:
            return ""

        return temp

    @set_user_specified_te_from_file.setter
    @enforce_parameter_types
    def set_user_specified_te_from_file(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SetUserSpecifiedTEFromFile",
            str(value) if value is not None else "",
        )

    @property
    def connection_design(self: "Self") -> "_2367.GearMesh":
        """mastapy.system_model.connections_and_sockets.gears.GearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def tooth_passing_harmonics(self: "Self") -> "List[_4260.ToothPassingHarmonic]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ToothPassingHarmonic]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothPassingHarmonics")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def system_deflection_results(self: "Self") -> "_2843.GearMeshSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.GearMeshSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshHarmonicAnalysis
        """
        return _Cast_GearMeshHarmonicAnalysis(self)
