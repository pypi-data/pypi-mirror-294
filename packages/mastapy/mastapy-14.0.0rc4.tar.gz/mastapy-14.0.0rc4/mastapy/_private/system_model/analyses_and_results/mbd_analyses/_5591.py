"""MountableComponentMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5529

_MOUNTABLE_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "MountableComponentMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5505,
        _5510,
        _5515,
        _5517,
        _5518,
        _5520,
        _5525,
        _5531,
        _5534,
        _5537,
        _5540,
        _5542,
        _5546,
        _5552,
        _5554,
        _5558,
        _5564,
        _5568,
        _5576,
        _5579,
        _5582,
        _5584,
        _5588,
        _5593,
        _5594,
        _5596,
        _5600,
        _5601,
        _5602,
        _5603,
        _5604,
        _5608,
        _5612,
        _5618,
        _5622,
        _5625,
        _5628,
        _5630,
        _5631,
        _5632,
        _5634,
        _5635,
        _5639,
        _5641,
        _5642,
        _5643,
        _5646,
        _5649,
    )
    from mastapy._private.system_model.part_model import _2521

    Self = TypeVar("Self", bound="MountableComponentMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentMultibodyDynamicsAnalysis._Cast_MountableComponentMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentMultibodyDynamicsAnalysis:
    """Special nested class for casting MountableComponentMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "MountableComponentMultibodyDynamicsAnalysis"

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5529.ComponentMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5529.ComponentMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5594.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5594,
        )

        return self.__parent__._cast(_5594.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7718.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartTimeSeriesLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7714.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2741.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2741

        return self.__parent__._cast(_2741.PartAnalysis)

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
    def agma_gleason_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5505.AGMAGleasonConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5505,
        )

        return self.__parent__._cast(
            _5505.AGMAGleasonConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def bearing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5510.BearingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5510,
        )

        return self.__parent__._cast(_5510.BearingMultibodyDynamicsAnalysis)

    @property
    def bevel_differential_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5515.BevelDifferentialGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5515,
        )

        return self.__parent__._cast(
            _5515.BevelDifferentialGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5517.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5517,
        )

        return self.__parent__._cast(
            _5517.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5518.BevelDifferentialSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5518,
        )

        return self.__parent__._cast(
            _5518.BevelDifferentialSunGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5520.BevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5520,
        )

        return self.__parent__._cast(_5520.BevelGearMultibodyDynamicsAnalysis)

    @property
    def clutch_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5525.ClutchHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5525,
        )

        return self.__parent__._cast(_5525.ClutchHalfMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5531.ConceptCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5531,
        )

        return self.__parent__._cast(_5531.ConceptCouplingHalfMultibodyDynamicsAnalysis)

    @property
    def concept_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5534.ConceptGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5534,
        )

        return self.__parent__._cast(_5534.ConceptGearMultibodyDynamicsAnalysis)

    @property
    def conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5537.ConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5537,
        )

        return self.__parent__._cast(_5537.ConicalGearMultibodyDynamicsAnalysis)

    @property
    def connector_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5540.ConnectorMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5540,
        )

        return self.__parent__._cast(_5540.ConnectorMultibodyDynamicsAnalysis)

    @property
    def coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5542.CouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5542,
        )

        return self.__parent__._cast(_5542.CouplingHalfMultibodyDynamicsAnalysis)

    @property
    def cvt_pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5546.CVTPulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5546,
        )

        return self.__parent__._cast(_5546.CVTPulleyMultibodyDynamicsAnalysis)

    @property
    def cylindrical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5552.CylindricalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5552,
        )

        return self.__parent__._cast(_5552.CylindricalGearMultibodyDynamicsAnalysis)

    @property
    def cylindrical_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5554.CylindricalPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5554,
        )

        return self.__parent__._cast(
            _5554.CylindricalPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def face_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5558.FaceGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5558,
        )

        return self.__parent__._cast(_5558.FaceGearMultibodyDynamicsAnalysis)

    @property
    def gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5564.GearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5564,
        )

        return self.__parent__._cast(_5564.GearMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5568.HypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5568,
        )

        return self.__parent__._cast(_5568.HypoidGearMultibodyDynamicsAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5576.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5576,
        )

        return self.__parent__._cast(
            _5576.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5579.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5579,
        )

        return self.__parent__._cast(
            _5579.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5582.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5582,
        )

        return self.__parent__._cast(
            _5582.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis
        )

    @property
    def mass_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5584.MassDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5584,
        )

        return self.__parent__._cast(_5584.MassDiscMultibodyDynamicsAnalysis)

    @property
    def measurement_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5588.MeasurementComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5588,
        )

        return self.__parent__._cast(
            _5588.MeasurementComponentMultibodyDynamicsAnalysis
        )

    @property
    def oil_seal_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5593.OilSealMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5593,
        )

        return self.__parent__._cast(_5593.OilSealMultibodyDynamicsAnalysis)

    @property
    def part_to_part_shear_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5596.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5596,
        )

        return self.__parent__._cast(
            _5596.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis
        )

    @property
    def planet_carrier_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5600.PlanetCarrierMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5600,
        )

        return self.__parent__._cast(_5600.PlanetCarrierMultibodyDynamicsAnalysis)

    @property
    def point_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5601.PointLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5601,
        )

        return self.__parent__._cast(_5601.PointLoadMultibodyDynamicsAnalysis)

    @property
    def power_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5602.PowerLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5602,
        )

        return self.__parent__._cast(_5602.PowerLoadMultibodyDynamicsAnalysis)

    @property
    def pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5603.PulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5603,
        )

        return self.__parent__._cast(_5603.PulleyMultibodyDynamicsAnalysis)

    @property
    def ring_pins_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5604.RingPinsMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5604,
        )

        return self.__parent__._cast(_5604.RingPinsMultibodyDynamicsAnalysis)

    @property
    def rolling_ring_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5608.RollingRingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5608,
        )

        return self.__parent__._cast(_5608.RollingRingMultibodyDynamicsAnalysis)

    @property
    def shaft_hub_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5612.ShaftHubConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5612,
        )

        return self.__parent__._cast(_5612.ShaftHubConnectionMultibodyDynamicsAnalysis)

    @property
    def spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5618.SpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5618,
        )

        return self.__parent__._cast(_5618.SpiralBevelGearMultibodyDynamicsAnalysis)

    @property
    def spring_damper_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5622.SpringDamperHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5622,
        )

        return self.__parent__._cast(_5622.SpringDamperHalfMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_diff_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5625.StraightBevelDiffGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5625,
        )

        return self.__parent__._cast(
            _5625.StraightBevelDiffGearMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5628.StraightBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5628,
        )

        return self.__parent__._cast(_5628.StraightBevelGearMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5630.StraightBevelPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5630,
        )

        return self.__parent__._cast(
            _5630.StraightBevelPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5631.StraightBevelSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5631,
        )

        return self.__parent__._cast(
            _5631.StraightBevelSunGearMultibodyDynamicsAnalysis
        )

    @property
    def synchroniser_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5632.SynchroniserHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5632,
        )

        return self.__parent__._cast(_5632.SynchroniserHalfMultibodyDynamicsAnalysis)

    @property
    def synchroniser_part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5634.SynchroniserPartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5634,
        )

        return self.__parent__._cast(_5634.SynchroniserPartMultibodyDynamicsAnalysis)

    @property
    def synchroniser_sleeve_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5635.SynchroniserSleeveMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5635,
        )

        return self.__parent__._cast(_5635.SynchroniserSleeveMultibodyDynamicsAnalysis)

    @property
    def torque_converter_pump_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5639.TorqueConverterPumpMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5639,
        )

        return self.__parent__._cast(_5639.TorqueConverterPumpMultibodyDynamicsAnalysis)

    @property
    def torque_converter_turbine_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5641.TorqueConverterTurbineMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5641,
        )

        return self.__parent__._cast(
            _5641.TorqueConverterTurbineMultibodyDynamicsAnalysis
        )

    @property
    def unbalanced_mass_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5642.UnbalancedMassMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5642,
        )

        return self.__parent__._cast(_5642.UnbalancedMassMultibodyDynamicsAnalysis)

    @property
    def virtual_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5643.VirtualComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5643,
        )

        return self.__parent__._cast(_5643.VirtualComponentMultibodyDynamicsAnalysis)

    @property
    def worm_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5646.WormGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5646,
        )

        return self.__parent__._cast(_5646.WormGearMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5649.ZerolBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5649,
        )

        return self.__parent__._cast(_5649.ZerolBevelGearMultibodyDynamicsAnalysis)

    @property
    def mountable_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "MountableComponentMultibodyDynamicsAnalysis":
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
class MountableComponentMultibodyDynamicsAnalysis(
    _5529.ComponentMultibodyDynamicsAnalysis
):
    """MountableComponentMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def elastic_acceleration_force(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticAccelerationForce")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def elastic_acceleration_moment(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticAccelerationMoment")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def elastic_quadratic_velocity_force(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticQuadraticVelocityForce")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def elastic_quadratic_velocity_moment(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticQuadraticVelocityMoment")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    def reference_acceleration_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceAccelerationTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def reference_quadratic_velocity_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceQuadraticVelocityTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    def component_design(self: "Self") -> "_2521.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponentMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentMultibodyDynamicsAnalysis
        """
        return _Cast_MountableComponentMultibodyDynamicsAnalysis(self)
