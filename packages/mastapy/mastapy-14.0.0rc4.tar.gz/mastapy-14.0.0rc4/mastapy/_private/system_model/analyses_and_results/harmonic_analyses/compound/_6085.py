"""KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6079,
)

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
        "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5913,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6045,
        _6047,
        _6071,
        _6077,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2374

    Self = TypeVar(
        "Self",
        bound="KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis._Cast_KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6079.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis":
        return self.__parent__._cast(
            _6079.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis
        )

    @property
    def conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6045.ConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6045,
        )

        return self.__parent__._cast(_6045.ConicalGearMeshCompoundHarmonicAnalysis)

    @property
    def gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6071.GearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6071,
        )

        return self.__parent__._cast(_6071.GearMeshCompoundHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6077.InterMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6077,
        )

        return self.__parent__._cast(
            _6077.InterMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6047.ConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6047,
        )

        return self.__parent__._cast(_6047.ConnectionCompoundHarmonicAnalysis)

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
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis":
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
class KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis(
    _6079.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis
):
    """KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(
        self: "Self",
    ) -> "_2374.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(
        self: "Self",
    ) -> "_2374.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5913.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis]

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
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5913.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidSpiralBevelGearMeshHarmonicAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis
        """
        return (
            _Cast_KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis(
                self
            )
        )
