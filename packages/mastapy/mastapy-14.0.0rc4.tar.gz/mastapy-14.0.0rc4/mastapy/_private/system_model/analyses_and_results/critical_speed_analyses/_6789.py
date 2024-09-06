"""SpecialisedAssemblyCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6686,
)

_SPECIALISED_ASSEMBLY_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "SpecialisedAssemblyCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6692,
        _6696,
        _6699,
        _6704,
        _6706,
        _6708,
        _6713,
        _6717,
        _6720,
        _6724,
        _6730,
        _6732,
        _6738,
        _6744,
        _6746,
        _6749,
        _6753,
        _6757,
        _6760,
        _6763,
        _6766,
        _6770,
        _6772,
        _6775,
        _6782,
        _6792,
        _6794,
        _6798,
        _6801,
        _6804,
        _6809,
        _6816,
        _6819,
    )
    from mastapy._private.system_model.part_model import _2533

    Self = TypeVar("Self", bound="SpecialisedAssemblyCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCriticalSpeedAnalysis._Cast_SpecialisedAssemblyCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCriticalSpeedAnalysis:
    """Special nested class for casting SpecialisedAssemblyCriticalSpeedAnalysis to subclasses."""

    __parent__: "SpecialisedAssemblyCriticalSpeedAnalysis"

    @property
    def abstract_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6686.AbstractAssemblyCriticalSpeedAnalysis":
        return self.__parent__._cast(_6686.AbstractAssemblyCriticalSpeedAnalysis)

    @property
    def part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6770.PartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6770,
        )

        return self.__parent__._cast(_6770.PartCriticalSpeedAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

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
    def agma_gleason_conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6692.AGMAGleasonConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6692,
        )

        return self.__parent__._cast(
            _6692.AGMAGleasonConicalGearSetCriticalSpeedAnalysis
        )

    @property
    def belt_drive_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6696.BeltDriveCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6696,
        )

        return self.__parent__._cast(_6696.BeltDriveCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6699.BevelDifferentialGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6699,
        )

        return self.__parent__._cast(
            _6699.BevelDifferentialGearSetCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6704.BevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6704,
        )

        return self.__parent__._cast(_6704.BevelGearSetCriticalSpeedAnalysis)

    @property
    def bolted_joint_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6706.BoltedJointCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6706,
        )

        return self.__parent__._cast(_6706.BoltedJointCriticalSpeedAnalysis)

    @property
    def clutch_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6708.ClutchCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6708,
        )

        return self.__parent__._cast(_6708.ClutchCriticalSpeedAnalysis)

    @property
    def concept_coupling_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6713.ConceptCouplingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6713,
        )

        return self.__parent__._cast(_6713.ConceptCouplingCriticalSpeedAnalysis)

    @property
    def concept_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6717.ConceptGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6717,
        )

        return self.__parent__._cast(_6717.ConceptGearSetCriticalSpeedAnalysis)

    @property
    def conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6720.ConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6720,
        )

        return self.__parent__._cast(_6720.ConicalGearSetCriticalSpeedAnalysis)

    @property
    def coupling_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6724.CouplingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6724,
        )

        return self.__parent__._cast(_6724.CouplingCriticalSpeedAnalysis)

    @property
    def cvt_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6730.CVTCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6730,
        )

        return self.__parent__._cast(_6730.CVTCriticalSpeedAnalysis)

    @property
    def cycloidal_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6732.CycloidalAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6732,
        )

        return self.__parent__._cast(_6732.CycloidalAssemblyCriticalSpeedAnalysis)

    @property
    def cylindrical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6738.CylindricalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6738,
        )

        return self.__parent__._cast(_6738.CylindricalGearSetCriticalSpeedAnalysis)

    @property
    def face_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6744.FaceGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6744,
        )

        return self.__parent__._cast(_6744.FaceGearSetCriticalSpeedAnalysis)

    @property
    def flexible_pin_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6746.FlexiblePinAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6746,
        )

        return self.__parent__._cast(_6746.FlexiblePinAssemblyCriticalSpeedAnalysis)

    @property
    def gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6749.GearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6749,
        )

        return self.__parent__._cast(_6749.GearSetCriticalSpeedAnalysis)

    @property
    def hypoid_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6753.HypoidGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6753,
        )

        return self.__parent__._cast(_6753.HypoidGearSetCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6757.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6757,
        )

        return self.__parent__._cast(
            _6757.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6760.KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6760,
        )

        return self.__parent__._cast(
            _6760.KlingelnbergCycloPalloidHypoidGearSetCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6763.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6763,
        )

        return self.__parent__._cast(
            _6763.KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis
        )

    @property
    def microphone_array_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6766.MicrophoneArrayCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6766,
        )

        return self.__parent__._cast(_6766.MicrophoneArrayCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6772.PartToPartShearCouplingCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6772,
        )

        return self.__parent__._cast(_6772.PartToPartShearCouplingCriticalSpeedAnalysis)

    @property
    def planetary_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6775.PlanetaryGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6775,
        )

        return self.__parent__._cast(_6775.PlanetaryGearSetCriticalSpeedAnalysis)

    @property
    def rolling_ring_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6782.RollingRingAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6782,
        )

        return self.__parent__._cast(_6782.RollingRingAssemblyCriticalSpeedAnalysis)

    @property
    def spiral_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6792.SpiralBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6792,
        )

        return self.__parent__._cast(_6792.SpiralBevelGearSetCriticalSpeedAnalysis)

    @property
    def spring_damper_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6794.SpringDamperCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6794,
        )

        return self.__parent__._cast(_6794.SpringDamperCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6798.StraightBevelDiffGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6798,
        )

        return self.__parent__._cast(
            _6798.StraightBevelDiffGearSetCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6801.StraightBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6801,
        )

        return self.__parent__._cast(_6801.StraightBevelGearSetCriticalSpeedAnalysis)

    @property
    def synchroniser_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6804.SynchroniserCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6804,
        )

        return self.__parent__._cast(_6804.SynchroniserCriticalSpeedAnalysis)

    @property
    def torque_converter_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6809.TorqueConverterCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6809,
        )

        return self.__parent__._cast(_6809.TorqueConverterCriticalSpeedAnalysis)

    @property
    def worm_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6816.WormGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6816,
        )

        return self.__parent__._cast(_6816.WormGearSetCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6819.ZerolBevelGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6819,
        )

        return self.__parent__._cast(_6819.ZerolBevelGearSetCriticalSpeedAnalysis)

    @property
    def specialised_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCriticalSpeedAnalysis":
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
class SpecialisedAssemblyCriticalSpeedAnalysis(
    _6686.AbstractAssemblyCriticalSpeedAnalysis
):
    """SpecialisedAssemblyCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2533.SpecialisedAssembly":
        """mastapy.system_model.part_model.SpecialisedAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssemblyCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCriticalSpeedAnalysis
        """
        return _Cast_SpecialisedAssemblyCriticalSpeedAnalysis(self)
