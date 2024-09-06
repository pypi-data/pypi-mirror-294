"""PartStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717

_PART_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "PartStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3863,
        _3864,
        _3865,
        _3868,
        _3869,
        _3870,
        _3871,
        _3873,
        _3875,
        _3876,
        _3877,
        _3878,
        _3880,
        _3881,
        _3882,
        _3883,
        _3885,
        _3886,
        _3888,
        _3890,
        _3891,
        _3893,
        _3894,
        _3896,
        _3897,
        _3899,
        _3901,
        _3902,
        _3905,
        _3906,
        _3907,
        _3910,
        _3912,
        _3913,
        _3914,
        _3915,
        _3917,
        _3919,
        _3920,
        _3921,
        _3922,
        _3924,
        _3925,
        _3926,
        _3928,
        _3929,
        _3932,
        _3933,
        _3935,
        _3936,
        _3938,
        _3939,
        _3940,
        _3941,
        _3942,
        _3943,
        _3944,
        _3945,
        _3948,
        _3949,
        _3951,
        _3952,
        _3953,
        _3954,
        _3955,
        _3956,
        _3958,
        _3960,
        _3961,
        _3962,
        _3963,
        _3965,
        _3967,
        _3968,
        _3970,
        _3971,
        _3972,
        _3976,
        _3977,
        _3979,
        _3980,
        _3981,
        _3982,
        _3983,
        _3984,
        _3985,
        _3986,
        _3988,
        _3989,
        _3990,
        _3991,
        _3992,
        _3994,
        _3995,
        _3997,
        _3998,
    )
    from mastapy._private.system_model.drawing import _2311
    from mastapy._private.system_model.part_model import _2525

    Self = TypeVar("Self", bound="PartStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="PartStabilityAnalysis._Cast_PartStabilityAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartStabilityAnalysis:
    """Special nested class for casting PartStabilityAnalysis to subclasses."""

    __parent__: "PartStabilityAnalysis"

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
        return self.__parent__._cast(_7717.PartStaticLoadAnalysisCase)

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
    def abstract_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3863.AbstractAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3863,
        )

        return self.__parent__._cast(_3863.AbstractAssemblyStabilityAnalysis)

    @property
    def abstract_shaft_or_housing_stability_analysis(
        self: "CastSelf",
    ) -> "_3864.AbstractShaftOrHousingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3864,
        )

        return self.__parent__._cast(_3864.AbstractShaftOrHousingStabilityAnalysis)

    @property
    def abstract_shaft_stability_analysis(
        self: "CastSelf",
    ) -> "_3865.AbstractShaftStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3865,
        )

        return self.__parent__._cast(_3865.AbstractShaftStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3868.AGMAGleasonConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3868,
        )

        return self.__parent__._cast(_3868.AGMAGleasonConicalGearSetStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3869.AGMAGleasonConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3869,
        )

        return self.__parent__._cast(_3869.AGMAGleasonConicalGearStabilityAnalysis)

    @property
    def assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3870.AssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3870,
        )

        return self.__parent__._cast(_3870.AssemblyStabilityAnalysis)

    @property
    def bearing_stability_analysis(
        self: "CastSelf",
    ) -> "_3871.BearingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3871,
        )

        return self.__parent__._cast(_3871.BearingStabilityAnalysis)

    @property
    def belt_drive_stability_analysis(
        self: "CastSelf",
    ) -> "_3873.BeltDriveStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3873,
        )

        return self.__parent__._cast(_3873.BeltDriveStabilityAnalysis)

    @property
    def bevel_differential_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3875.BevelDifferentialGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3875,
        )

        return self.__parent__._cast(_3875.BevelDifferentialGearSetStabilityAnalysis)

    @property
    def bevel_differential_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3876.BevelDifferentialGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3876,
        )

        return self.__parent__._cast(_3876.BevelDifferentialGearStabilityAnalysis)

    @property
    def bevel_differential_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3877.BevelDifferentialPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3877,
        )

        return self.__parent__._cast(_3877.BevelDifferentialPlanetGearStabilityAnalysis)

    @property
    def bevel_differential_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3878.BevelDifferentialSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3878,
        )

        return self.__parent__._cast(_3878.BevelDifferentialSunGearStabilityAnalysis)

    @property
    def bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3880.BevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3880,
        )

        return self.__parent__._cast(_3880.BevelGearSetStabilityAnalysis)

    @property
    def bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3881.BevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3881,
        )

        return self.__parent__._cast(_3881.BevelGearStabilityAnalysis)

    @property
    def bolted_joint_stability_analysis(
        self: "CastSelf",
    ) -> "_3882.BoltedJointStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3882,
        )

        return self.__parent__._cast(_3882.BoltedJointStabilityAnalysis)

    @property
    def bolt_stability_analysis(self: "CastSelf") -> "_3883.BoltStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3883,
        )

        return self.__parent__._cast(_3883.BoltStabilityAnalysis)

    @property
    def clutch_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3885.ClutchHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3885,
        )

        return self.__parent__._cast(_3885.ClutchHalfStabilityAnalysis)

    @property
    def clutch_stability_analysis(self: "CastSelf") -> "_3886.ClutchStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3886,
        )

        return self.__parent__._cast(_3886.ClutchStabilityAnalysis)

    @property
    def component_stability_analysis(
        self: "CastSelf",
    ) -> "_3888.ComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3888,
        )

        return self.__parent__._cast(_3888.ComponentStabilityAnalysis)

    @property
    def concept_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3890.ConceptCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3890,
        )

        return self.__parent__._cast(_3890.ConceptCouplingHalfStabilityAnalysis)

    @property
    def concept_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3891.ConceptCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3891,
        )

        return self.__parent__._cast(_3891.ConceptCouplingStabilityAnalysis)

    @property
    def concept_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3893.ConceptGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3893,
        )

        return self.__parent__._cast(_3893.ConceptGearSetStabilityAnalysis)

    @property
    def concept_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3894.ConceptGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3894,
        )

        return self.__parent__._cast(_3894.ConceptGearStabilityAnalysis)

    @property
    def conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3896.ConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3896,
        )

        return self.__parent__._cast(_3896.ConicalGearSetStabilityAnalysis)

    @property
    def conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3897.ConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3897,
        )

        return self.__parent__._cast(_3897.ConicalGearStabilityAnalysis)

    @property
    def connector_stability_analysis(
        self: "CastSelf",
    ) -> "_3899.ConnectorStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3899,
        )

        return self.__parent__._cast(_3899.ConnectorStabilityAnalysis)

    @property
    def coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3901.CouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3901,
        )

        return self.__parent__._cast(_3901.CouplingHalfStabilityAnalysis)

    @property
    def coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3902.CouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3902,
        )

        return self.__parent__._cast(_3902.CouplingStabilityAnalysis)

    @property
    def cvt_pulley_stability_analysis(
        self: "CastSelf",
    ) -> "_3905.CVTPulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3905,
        )

        return self.__parent__._cast(_3905.CVTPulleyStabilityAnalysis)

    @property
    def cvt_stability_analysis(self: "CastSelf") -> "_3906.CVTStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3906,
        )

        return self.__parent__._cast(_3906.CVTStabilityAnalysis)

    @property
    def cycloidal_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3907.CycloidalAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3907,
        )

        return self.__parent__._cast(_3907.CycloidalAssemblyStabilityAnalysis)

    @property
    def cycloidal_disc_stability_analysis(
        self: "CastSelf",
    ) -> "_3910.CycloidalDiscStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3910,
        )

        return self.__parent__._cast(_3910.CycloidalDiscStabilityAnalysis)

    @property
    def cylindrical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3912.CylindricalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3912,
        )

        return self.__parent__._cast(_3912.CylindricalGearSetStabilityAnalysis)

    @property
    def cylindrical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3913.CylindricalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3913,
        )

        return self.__parent__._cast(_3913.CylindricalGearStabilityAnalysis)

    @property
    def cylindrical_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3914.CylindricalPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3914,
        )

        return self.__parent__._cast(_3914.CylindricalPlanetGearStabilityAnalysis)

    @property
    def datum_stability_analysis(self: "CastSelf") -> "_3915.DatumStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3915,
        )

        return self.__parent__._cast(_3915.DatumStabilityAnalysis)

    @property
    def external_cad_model_stability_analysis(
        self: "CastSelf",
    ) -> "_3917.ExternalCADModelStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3917,
        )

        return self.__parent__._cast(_3917.ExternalCADModelStabilityAnalysis)

    @property
    def face_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3919.FaceGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3919,
        )

        return self.__parent__._cast(_3919.FaceGearSetStabilityAnalysis)

    @property
    def face_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3920.FaceGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3920,
        )

        return self.__parent__._cast(_3920.FaceGearStabilityAnalysis)

    @property
    def fe_part_stability_analysis(self: "CastSelf") -> "_3921.FEPartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3921,
        )

        return self.__parent__._cast(_3921.FEPartStabilityAnalysis)

    @property
    def flexible_pin_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3922.FlexiblePinAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3922,
        )

        return self.__parent__._cast(_3922.FlexiblePinAssemblyStabilityAnalysis)

    @property
    def gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3924.GearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3924,
        )

        return self.__parent__._cast(_3924.GearSetStabilityAnalysis)

    @property
    def gear_stability_analysis(self: "CastSelf") -> "_3925.GearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3925,
        )

        return self.__parent__._cast(_3925.GearStabilityAnalysis)

    @property
    def guide_dxf_model_stability_analysis(
        self: "CastSelf",
    ) -> "_3926.GuideDxfModelStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3926,
        )

        return self.__parent__._cast(_3926.GuideDxfModelStabilityAnalysis)

    @property
    def hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3928.HypoidGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3928,
        )

        return self.__parent__._cast(_3928.HypoidGearSetStabilityAnalysis)

    @property
    def hypoid_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3929.HypoidGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3929,
        )

        return self.__parent__._cast(_3929.HypoidGearStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3932.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3932,
        )

        return self.__parent__._cast(
            _3932.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3933.KlingelnbergCycloPalloidConicalGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3933,
        )

        return self.__parent__._cast(
            _3933.KlingelnbergCycloPalloidConicalGearStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3935.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3935,
        )

        return self.__parent__._cast(
            _3935.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3936.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3936,
        )

        return self.__parent__._cast(
            _3936.KlingelnbergCycloPalloidHypoidGearStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3938.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3938,
        )

        return self.__parent__._cast(
            _3938.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3939.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3939,
        )

        return self.__parent__._cast(
            _3939.KlingelnbergCycloPalloidSpiralBevelGearStabilityAnalysis
        )

    @property
    def mass_disc_stability_analysis(
        self: "CastSelf",
    ) -> "_3940.MassDiscStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3940,
        )

        return self.__parent__._cast(_3940.MassDiscStabilityAnalysis)

    @property
    def measurement_component_stability_analysis(
        self: "CastSelf",
    ) -> "_3941.MeasurementComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3941,
        )

        return self.__parent__._cast(_3941.MeasurementComponentStabilityAnalysis)

    @property
    def microphone_array_stability_analysis(
        self: "CastSelf",
    ) -> "_3942.MicrophoneArrayStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3942,
        )

        return self.__parent__._cast(_3942.MicrophoneArrayStabilityAnalysis)

    @property
    def microphone_stability_analysis(
        self: "CastSelf",
    ) -> "_3943.MicrophoneStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3943,
        )

        return self.__parent__._cast(_3943.MicrophoneStabilityAnalysis)

    @property
    def mountable_component_stability_analysis(
        self: "CastSelf",
    ) -> "_3944.MountableComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3944,
        )

        return self.__parent__._cast(_3944.MountableComponentStabilityAnalysis)

    @property
    def oil_seal_stability_analysis(
        self: "CastSelf",
    ) -> "_3945.OilSealStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3945,
        )

        return self.__parent__._cast(_3945.OilSealStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3948.PartToPartShearCouplingHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3948,
        )

        return self.__parent__._cast(_3948.PartToPartShearCouplingHalfStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3949.PartToPartShearCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3949,
        )

        return self.__parent__._cast(_3949.PartToPartShearCouplingStabilityAnalysis)

    @property
    def planetary_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3951.PlanetaryGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3951,
        )

        return self.__parent__._cast(_3951.PlanetaryGearSetStabilityAnalysis)

    @property
    def planet_carrier_stability_analysis(
        self: "CastSelf",
    ) -> "_3952.PlanetCarrierStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3952,
        )

        return self.__parent__._cast(_3952.PlanetCarrierStabilityAnalysis)

    @property
    def point_load_stability_analysis(
        self: "CastSelf",
    ) -> "_3953.PointLoadStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3953,
        )

        return self.__parent__._cast(_3953.PointLoadStabilityAnalysis)

    @property
    def power_load_stability_analysis(
        self: "CastSelf",
    ) -> "_3954.PowerLoadStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3954,
        )

        return self.__parent__._cast(_3954.PowerLoadStabilityAnalysis)

    @property
    def pulley_stability_analysis(self: "CastSelf") -> "_3955.PulleyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3955,
        )

        return self.__parent__._cast(_3955.PulleyStabilityAnalysis)

    @property
    def ring_pins_stability_analysis(
        self: "CastSelf",
    ) -> "_3956.RingPinsStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3956,
        )

        return self.__parent__._cast(_3956.RingPinsStabilityAnalysis)

    @property
    def rolling_ring_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3958.RollingRingAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3958,
        )

        return self.__parent__._cast(_3958.RollingRingAssemblyStabilityAnalysis)

    @property
    def rolling_ring_stability_analysis(
        self: "CastSelf",
    ) -> "_3960.RollingRingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3960,
        )

        return self.__parent__._cast(_3960.RollingRingStabilityAnalysis)

    @property
    def root_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3961.RootAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3961,
        )

        return self.__parent__._cast(_3961.RootAssemblyStabilityAnalysis)

    @property
    def shaft_hub_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3962.ShaftHubConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3962,
        )

        return self.__parent__._cast(_3962.ShaftHubConnectionStabilityAnalysis)

    @property
    def shaft_stability_analysis(self: "CastSelf") -> "_3963.ShaftStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3963,
        )

        return self.__parent__._cast(_3963.ShaftStabilityAnalysis)

    @property
    def specialised_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3965.SpecialisedAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3965,
        )

        return self.__parent__._cast(_3965.SpecialisedAssemblyStabilityAnalysis)

    @property
    def spiral_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3967.SpiralBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3967,
        )

        return self.__parent__._cast(_3967.SpiralBevelGearSetStabilityAnalysis)

    @property
    def spiral_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3968.SpiralBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3968,
        )

        return self.__parent__._cast(_3968.SpiralBevelGearStabilityAnalysis)

    @property
    def spring_damper_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3970.SpringDamperHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3970,
        )

        return self.__parent__._cast(_3970.SpringDamperHalfStabilityAnalysis)

    @property
    def spring_damper_stability_analysis(
        self: "CastSelf",
    ) -> "_3971.SpringDamperStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3971,
        )

        return self.__parent__._cast(_3971.SpringDamperStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3976.StraightBevelDiffGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3976,
        )

        return self.__parent__._cast(_3976.StraightBevelDiffGearSetStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3977.StraightBevelDiffGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3977,
        )

        return self.__parent__._cast(_3977.StraightBevelDiffGearStabilityAnalysis)

    @property
    def straight_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3979.StraightBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3979,
        )

        return self.__parent__._cast(_3979.StraightBevelGearSetStabilityAnalysis)

    @property
    def straight_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3980.StraightBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3980,
        )

        return self.__parent__._cast(_3980.StraightBevelGearStabilityAnalysis)

    @property
    def straight_bevel_planet_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3981.StraightBevelPlanetGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3981,
        )

        return self.__parent__._cast(_3981.StraightBevelPlanetGearStabilityAnalysis)

    @property
    def straight_bevel_sun_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3982.StraightBevelSunGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3982,
        )

        return self.__parent__._cast(_3982.StraightBevelSunGearStabilityAnalysis)

    @property
    def synchroniser_half_stability_analysis(
        self: "CastSelf",
    ) -> "_3983.SynchroniserHalfStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3983,
        )

        return self.__parent__._cast(_3983.SynchroniserHalfStabilityAnalysis)

    @property
    def synchroniser_part_stability_analysis(
        self: "CastSelf",
    ) -> "_3984.SynchroniserPartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3984,
        )

        return self.__parent__._cast(_3984.SynchroniserPartStabilityAnalysis)

    @property
    def synchroniser_sleeve_stability_analysis(
        self: "CastSelf",
    ) -> "_3985.SynchroniserSleeveStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3985,
        )

        return self.__parent__._cast(_3985.SynchroniserSleeveStabilityAnalysis)

    @property
    def synchroniser_stability_analysis(
        self: "CastSelf",
    ) -> "_3986.SynchroniserStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3986,
        )

        return self.__parent__._cast(_3986.SynchroniserStabilityAnalysis)

    @property
    def torque_converter_pump_stability_analysis(
        self: "CastSelf",
    ) -> "_3988.TorqueConverterPumpStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3988,
        )

        return self.__parent__._cast(_3988.TorqueConverterPumpStabilityAnalysis)

    @property
    def torque_converter_stability_analysis(
        self: "CastSelf",
    ) -> "_3989.TorqueConverterStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3989,
        )

        return self.__parent__._cast(_3989.TorqueConverterStabilityAnalysis)

    @property
    def torque_converter_turbine_stability_analysis(
        self: "CastSelf",
    ) -> "_3990.TorqueConverterTurbineStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3990,
        )

        return self.__parent__._cast(_3990.TorqueConverterTurbineStabilityAnalysis)

    @property
    def unbalanced_mass_stability_analysis(
        self: "CastSelf",
    ) -> "_3991.UnbalancedMassStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3991,
        )

        return self.__parent__._cast(_3991.UnbalancedMassStabilityAnalysis)

    @property
    def virtual_component_stability_analysis(
        self: "CastSelf",
    ) -> "_3992.VirtualComponentStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3992,
        )

        return self.__parent__._cast(_3992.VirtualComponentStabilityAnalysis)

    @property
    def worm_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3994.WormGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3994,
        )

        return self.__parent__._cast(_3994.WormGearSetStabilityAnalysis)

    @property
    def worm_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3995.WormGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3995,
        )

        return self.__parent__._cast(_3995.WormGearStabilityAnalysis)

    @property
    def zerol_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3997.ZerolBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3997,
        )

        return self.__parent__._cast(_3997.ZerolBevelGearSetStabilityAnalysis)

    @property
    def zerol_bevel_gear_stability_analysis(
        self: "CastSelf",
    ) -> "_3998.ZerolBevelGearStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3998,
        )

        return self.__parent__._cast(_3998.ZerolBevelGearStabilityAnalysis)

    @property
    def part_stability_analysis(self: "CastSelf") -> "PartStabilityAnalysis":
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
class PartStabilityAnalysis(_7717.PartStaticLoadAnalysisCase):
    """PartStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2525.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def stability_analysis(self: "Self") -> "_3972.StabilityAnalysis":
        """mastapy.system_model.analyses_and_results.stability_analyses.StabilityAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StabilityAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def create_viewable(self: "Self") -> "_2311.StabilityAnalysisViewable":
        """mastapy.system_model.drawing.StabilityAnalysisViewable"""
        method_result = pythonnet_method_call(self.wrapped, "CreateViewable")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartStabilityAnalysis
        """
        return _Cast_PartStabilityAnalysis(self)
