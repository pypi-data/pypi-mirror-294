"""ConnectionFEAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710

_CONNECTION_FE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases", "ConnectionFEAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7707
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6419,
        _6421,
        _6425,
        _6428,
        _6433,
        _6437,
        _6440,
        _6442,
        _6446,
        _6449,
        _6451,
        _6453,
        _6456,
        _6460,
        _6462,
        _6464,
        _6472,
        _6477,
        _6481,
        _6483,
        _6485,
        _6488,
        _6491,
        _6500,
        _6503,
        _6510,
        _6512,
        _6517,
        _6520,
        _6522,
        _6526,
        _6529,
        _6537,
        _6544,
        _6547,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2772,
        _2773,
        _2783,
        _2785,
        _2790,
        _2795,
        _2798,
        _2801,
        _2804,
        _2808,
        _2811,
        _2813,
        _2816,
        _2820,
        _2821,
        _2823,
        _2824,
        _2825,
        _2838,
        _2843,
        _2847,
        _2851,
        _2852,
        _2855,
        _2858,
        _2872,
        _2875,
        _2881,
        _2884,
        _2891,
        _2893,
        _2896,
        _2899,
        _2902,
        _2914,
        _2922,
        _2925,
    )

    Self = TypeVar("Self", bound="ConnectionFEAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ConnectionFEAnalysis._Cast_ConnectionFEAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionFEAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionFEAnalysis:
    """Special nested class for casting ConnectionFEAnalysis to subclasses."""

    __parent__: "ConnectionFEAnalysis"

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
    def abstract_shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2772.AbstractShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2772,
        )

        return self.__parent__._cast(
            _2772.AbstractShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2773.AGMAGleasonConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2773,
        )

        return self.__parent__._cast(_2773.AGMAGleasonConicalGearMeshSystemDeflection)

    @property
    def belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2783.BeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2783,
        )

        return self.__parent__._cast(_2783.BeltConnectionSystemDeflection)

    @property
    def bevel_differential_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2785.BevelDifferentialGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2785,
        )

        return self.__parent__._cast(_2785.BevelDifferentialGearMeshSystemDeflection)

    @property
    def bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2790.BevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2790,
        )

        return self.__parent__._cast(_2790.BevelGearMeshSystemDeflection)

    @property
    def clutch_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2795.ClutchConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2795,
        )

        return self.__parent__._cast(_2795.ClutchConnectionSystemDeflection)

    @property
    def coaxial_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2798.CoaxialConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2798,
        )

        return self.__parent__._cast(_2798.CoaxialConnectionSystemDeflection)

    @property
    def concept_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2801.ConceptCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2801,
        )

        return self.__parent__._cast(_2801.ConceptCouplingConnectionSystemDeflection)

    @property
    def concept_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2804.ConceptGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2804,
        )

        return self.__parent__._cast(_2804.ConceptGearMeshSystemDeflection)

    @property
    def conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2808.ConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2808,
        )

        return self.__parent__._cast(_2808.ConicalGearMeshSystemDeflection)

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2811.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2811,
        )

        return self.__parent__._cast(_2811.ConnectionSystemDeflection)

    @property
    def coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2813.CouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2813,
        )

        return self.__parent__._cast(_2813.CouplingConnectionSystemDeflection)

    @property
    def cvt_belt_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2816.CVTBeltConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2816,
        )

        return self.__parent__._cast(_2816.CVTBeltConnectionSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2820.CycloidalDiscCentralBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2820,
        )

        return self.__parent__._cast(
            _2820.CycloidalDiscCentralBearingConnectionSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2821.CycloidalDiscPlanetaryBearingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2821,
        )

        return self.__parent__._cast(
            _2821.CycloidalDiscPlanetaryBearingConnectionSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2823.CylindricalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2823,
        )

        return self.__parent__._cast(_2823.CylindricalGearMeshSystemDeflection)

    @property
    def cylindrical_gear_mesh_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2824.CylindricalGearMeshSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2824,
        )

        return self.__parent__._cast(_2824.CylindricalGearMeshSystemDeflectionTimestep)

    @property
    def cylindrical_gear_mesh_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2825.CylindricalGearMeshSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2825,
        )

        return self.__parent__._cast(
            _2825.CylindricalGearMeshSystemDeflectionWithLTCAResults
        )

    @property
    def face_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2838.FaceGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2838,
        )

        return self.__parent__._cast(_2838.FaceGearMeshSystemDeflection)

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2843.GearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2843,
        )

        return self.__parent__._cast(_2843.GearMeshSystemDeflection)

    @property
    def hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2847.HypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2847,
        )

        return self.__parent__._cast(_2847.HypoidGearMeshSystemDeflection)

    @property
    def inter_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2851.InterMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2851,
        )

        return self.__parent__._cast(
            _2851.InterMountableComponentConnectionSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2852.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2852,
        )

        return self.__parent__._cast(
            _2852.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2855.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2855,
        )

        return self.__parent__._cast(
            _2855.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2858.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2858,
        )

        return self.__parent__._cast(
            _2858.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2872.PartToPartShearCouplingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2872,
        )

        return self.__parent__._cast(
            _2872.PartToPartShearCouplingConnectionSystemDeflection
        )

    @property
    def planetary_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2875.PlanetaryConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2875,
        )

        return self.__parent__._cast(_2875.PlanetaryConnectionSystemDeflection)

    @property
    def ring_pins_to_disc_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2881.RingPinsToDiscConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2881,
        )

        return self.__parent__._cast(_2881.RingPinsToDiscConnectionSystemDeflection)

    @property
    def rolling_ring_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2884.RollingRingConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2884,
        )

        return self.__parent__._cast(_2884.RollingRingConnectionSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2891.ShaftToMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2891,
        )

        return self.__parent__._cast(
            _2891.ShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2893.SpiralBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2893,
        )

        return self.__parent__._cast(_2893.SpiralBevelGearMeshSystemDeflection)

    @property
    def spring_damper_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2896.SpringDamperConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2896,
        )

        return self.__parent__._cast(_2896.SpringDamperConnectionSystemDeflection)

    @property
    def straight_bevel_diff_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2899.StraightBevelDiffGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2899,
        )

        return self.__parent__._cast(_2899.StraightBevelDiffGearMeshSystemDeflection)

    @property
    def straight_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2902.StraightBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2902,
        )

        return self.__parent__._cast(_2902.StraightBevelGearMeshSystemDeflection)

    @property
    def torque_converter_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2914.TorqueConverterConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2914,
        )

        return self.__parent__._cast(_2914.TorqueConverterConnectionSystemDeflection)

    @property
    def worm_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2922.WormGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2922,
        )

        return self.__parent__._cast(_2922.WormGearMeshSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_2925.ZerolBevelGearMeshSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2925,
        )

        return self.__parent__._cast(_2925.ZerolBevelGearMeshSystemDeflection)

    @property
    def abstract_shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6419.AbstractShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6419,
        )

        return self.__parent__._cast(
            _6419.AbstractShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def agma_gleason_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6421.AGMAGleasonConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6421,
        )

        return self.__parent__._cast(_6421.AGMAGleasonConicalGearMeshDynamicAnalysis)

    @property
    def belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6425.BeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6425,
        )

        return self.__parent__._cast(_6425.BeltConnectionDynamicAnalysis)

    @property
    def bevel_differential_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6428.BevelDifferentialGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6428,
        )

        return self.__parent__._cast(_6428.BevelDifferentialGearMeshDynamicAnalysis)

    @property
    def bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6433.BevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6433,
        )

        return self.__parent__._cast(_6433.BevelGearMeshDynamicAnalysis)

    @property
    def clutch_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6437.ClutchConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6437,
        )

        return self.__parent__._cast(_6437.ClutchConnectionDynamicAnalysis)

    @property
    def coaxial_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6440.CoaxialConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6440,
        )

        return self.__parent__._cast(_6440.CoaxialConnectionDynamicAnalysis)

    @property
    def concept_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6442.ConceptCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6442,
        )

        return self.__parent__._cast(_6442.ConceptCouplingConnectionDynamicAnalysis)

    @property
    def concept_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6446.ConceptGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6446,
        )

        return self.__parent__._cast(_6446.ConceptGearMeshDynamicAnalysis)

    @property
    def conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6449.ConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6449,
        )

        return self.__parent__._cast(_6449.ConicalGearMeshDynamicAnalysis)

    @property
    def connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6451.ConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6451,
        )

        return self.__parent__._cast(_6451.ConnectionDynamicAnalysis)

    @property
    def coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6453.CouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6453,
        )

        return self.__parent__._cast(_6453.CouplingConnectionDynamicAnalysis)

    @property
    def cvt_belt_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6456.CVTBeltConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6456,
        )

        return self.__parent__._cast(_6456.CVTBeltConnectionDynamicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6460.CycloidalDiscCentralBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6460,
        )

        return self.__parent__._cast(
            _6460.CycloidalDiscCentralBearingConnectionDynamicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6462.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6462,
        )

        return self.__parent__._cast(
            _6462.CycloidalDiscPlanetaryBearingConnectionDynamicAnalysis
        )

    @property
    def cylindrical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6464.CylindricalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6464,
        )

        return self.__parent__._cast(_6464.CylindricalGearMeshDynamicAnalysis)

    @property
    def face_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6472.FaceGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6472,
        )

        return self.__parent__._cast(_6472.FaceGearMeshDynamicAnalysis)

    @property
    def gear_mesh_dynamic_analysis(self: "CastSelf") -> "_6477.GearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6477,
        )

        return self.__parent__._cast(_6477.GearMeshDynamicAnalysis)

    @property
    def hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6481.HypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6481,
        )

        return self.__parent__._cast(_6481.HypoidGearMeshDynamicAnalysis)

    @property
    def inter_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6483.InterMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6483,
        )

        return self.__parent__._cast(
            _6483.InterMountableComponentConnectionDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6485.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6485,
        )

        return self.__parent__._cast(
            _6485.KlingelnbergCycloPalloidConicalGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6488.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6488,
        )

        return self.__parent__._cast(
            _6488.KlingelnbergCycloPalloidHypoidGearMeshDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6491.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6491,
        )

        return self.__parent__._cast(
            _6491.KlingelnbergCycloPalloidSpiralBevelGearMeshDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6500.PartToPartShearCouplingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6500,
        )

        return self.__parent__._cast(
            _6500.PartToPartShearCouplingConnectionDynamicAnalysis
        )

    @property
    def planetary_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6503.PlanetaryConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6503,
        )

        return self.__parent__._cast(_6503.PlanetaryConnectionDynamicAnalysis)

    @property
    def ring_pins_to_disc_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6510.RingPinsToDiscConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6510,
        )

        return self.__parent__._cast(_6510.RingPinsToDiscConnectionDynamicAnalysis)

    @property
    def rolling_ring_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6512.RollingRingConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6512,
        )

        return self.__parent__._cast(_6512.RollingRingConnectionDynamicAnalysis)

    @property
    def shaft_to_mountable_component_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6517.ShaftToMountableComponentConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6517,
        )

        return self.__parent__._cast(
            _6517.ShaftToMountableComponentConnectionDynamicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6520.SpiralBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6520,
        )

        return self.__parent__._cast(_6520.SpiralBevelGearMeshDynamicAnalysis)

    @property
    def spring_damper_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6522.SpringDamperConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6522,
        )

        return self.__parent__._cast(_6522.SpringDamperConnectionDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6526.StraightBevelDiffGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6526,
        )

        return self.__parent__._cast(_6526.StraightBevelDiffGearMeshDynamicAnalysis)

    @property
    def straight_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6529.StraightBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6529,
        )

        return self.__parent__._cast(_6529.StraightBevelGearMeshDynamicAnalysis)

    @property
    def torque_converter_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6537.TorqueConverterConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6537,
        )

        return self.__parent__._cast(_6537.TorqueConverterConnectionDynamicAnalysis)

    @property
    def worm_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6544.WormGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6544,
        )

        return self.__parent__._cast(_6544.WormGearMeshDynamicAnalysis)

    @property
    def zerol_bevel_gear_mesh_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6547.ZerolBevelGearMeshDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6547,
        )

        return self.__parent__._cast(_6547.ZerolBevelGearMeshDynamicAnalysis)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "ConnectionFEAnalysis":
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
class ConnectionFEAnalysis(_7710.ConnectionStaticLoadAnalysisCase):
    """ConnectionFEAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_FE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectionFEAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectionFEAnalysis
        """
        return _Cast_ConnectionFEAnalysis(self)
