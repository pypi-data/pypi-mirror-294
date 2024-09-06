"""ConnectionHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710

_CONNECTION_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "ConnectionHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7707
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5813,
        _5815,
        _5819,
        _5822,
        _5827,
        _5831,
        _5834,
        _5837,
        _5841,
        _5844,
        _5848,
        _5851,
        _5855,
        _5857,
        _5859,
        _5879,
        _5886,
        _5892,
        _5903,
        _5905,
        _5907,
        _5910,
        _5913,
        _5922,
        _5926,
        _5934,
        _5936,
        _5941,
        _5946,
        _5948,
        _5953,
        _5956,
        _5964,
        _5972,
        _5975,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6205,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2811,
    )
    from mastapy._private.system_model.connections_and_sockets import _2326

    Self = TypeVar("Self", bound="ConnectionHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectionHarmonicAnalysis._Cast_ConnectionHarmonicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionHarmonicAnalysis:
    """Special nested class for casting ConnectionHarmonicAnalysis to subclasses."""

    __parent__: "ConnectionHarmonicAnalysis"

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7710.ConnectionStaticLoadAnalysisCase":
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
    def abstract_shaft_to_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5813.AbstractShaftToMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5813,
        )

        return self.__parent__._cast(
            _5813.AbstractShaftToMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5815.AGMAGleasonConicalGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5815,
        )

        return self.__parent__._cast(_5815.AGMAGleasonConicalGearMeshHarmonicAnalysis)

    @property
    def belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5819.BeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5819,
        )

        return self.__parent__._cast(_5819.BeltConnectionHarmonicAnalysis)

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
    def clutch_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5831.ClutchConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5831,
        )

        return self.__parent__._cast(_5831.ClutchConnectionHarmonicAnalysis)

    @property
    def coaxial_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5834.CoaxialConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5834,
        )

        return self.__parent__._cast(_5834.CoaxialConnectionHarmonicAnalysis)

    @property
    def concept_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5837.ConceptCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5837,
        )

        return self.__parent__._cast(_5837.ConceptCouplingConnectionHarmonicAnalysis)

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
    def coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5848.CouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5848,
        )

        return self.__parent__._cast(_5848.CouplingConnectionHarmonicAnalysis)

    @property
    def cvt_belt_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5851.CVTBeltConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5851,
        )

        return self.__parent__._cast(_5851.CVTBeltConnectionHarmonicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5855.CycloidalDiscCentralBearingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5855,
        )

        return self.__parent__._cast(
            _5855.CycloidalDiscCentralBearingConnectionHarmonicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5857.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5857,
        )

        return self.__parent__._cast(
            _5857.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis
        )

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
    def gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5886.GearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5886,
        )

        return self.__parent__._cast(_5886.GearMeshHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5903.HypoidGearMeshHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5903,
        )

        return self.__parent__._cast(_5903.HypoidGearMeshHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5905.InterMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5905,
        )

        return self.__parent__._cast(
            _5905.InterMountableComponentConnectionHarmonicAnalysis
        )

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
    def part_to_part_shear_coupling_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5922.PartToPartShearCouplingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5922,
        )

        return self.__parent__._cast(
            _5922.PartToPartShearCouplingConnectionHarmonicAnalysis
        )

    @property
    def planetary_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5926.PlanetaryConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5926,
        )

        return self.__parent__._cast(_5926.PlanetaryConnectionHarmonicAnalysis)

    @property
    def ring_pins_to_disc_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5934.RingPinsToDiscConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5934,
        )

        return self.__parent__._cast(_5934.RingPinsToDiscConnectionHarmonicAnalysis)

    @property
    def rolling_ring_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5936.RollingRingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5936,
        )

        return self.__parent__._cast(_5936.RollingRingConnectionHarmonicAnalysis)

    @property
    def shaft_to_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5941.ShaftToMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5941,
        )

        return self.__parent__._cast(
            _5941.ShaftToMountableComponentConnectionHarmonicAnalysis
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
    def spring_damper_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5948.SpringDamperConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5948,
        )

        return self.__parent__._cast(_5948.SpringDamperConnectionHarmonicAnalysis)

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
    def torque_converter_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5964.TorqueConverterConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5964,
        )

        return self.__parent__._cast(_5964.TorqueConverterConnectionHarmonicAnalysis)

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
    def connection_harmonic_analysis(self: "CastSelf") -> "ConnectionHarmonicAnalysis":
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
class ConnectionHarmonicAnalysis(_7710.ConnectionStaticLoadAnalysisCase):
    """ConnectionHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2326.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2326.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analysis(self: "Self") -> "_5892.HarmonicAnalysis":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def harmonic_analyses_of_single_excitations(
        self: "Self",
    ) -> "List[_6205.HarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.HarmonicAnalysisOfSingleExcitation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HarmonicAnalysesOfSingleExcitations"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def system_deflection_results(self: "Self") -> "_2811.ConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionHarmonicAnalysis
        """
        return _Cast_ConnectionHarmonicAnalysis(self)
