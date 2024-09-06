"""SpecialisedAssemblyCompoundStabilityAnalysis"""

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
    _3999,
)

_SPECIALISED_ASSEMBLY_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "SpecialisedAssemblyCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3965,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4005,
        _4009,
        _4012,
        _4017,
        _4019,
        _4020,
        _4025,
        _4030,
        _4033,
        _4036,
        _4040,
        _4042,
        _4048,
        _4054,
        _4056,
        _4059,
        _4063,
        _4067,
        _4070,
        _4073,
        _4076,
        _4080,
        _4081,
        _4085,
        _4092,
        _4102,
        _4103,
        _4108,
        _4111,
        _4114,
        _4118,
        _4126,
        _4129,
    )

    Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundStabilityAnalysis._Cast_SpecialisedAssemblyCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundStabilityAnalysis:
    """Special nested class for casting SpecialisedAssemblyCompoundStabilityAnalysis to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundStabilityAnalysis"

    @property
    def abstract_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_3999.AbstractAssemblyCompoundStabilityAnalysis":
        return self.__parent__._cast(_3999.AbstractAssemblyCompoundStabilityAnalysis)

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4080.PartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4080,
        )

        return self.__parent__._cast(_4080.PartCompoundStabilityAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7715.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.PartCompoundAnalysis)

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
    def agma_gleason_conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4005.AGMAGleasonConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4005,
        )

        return self.__parent__._cast(
            _4005.AGMAGleasonConicalGearSetCompoundStabilityAnalysis
        )

    @property
    def belt_drive_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4009.BeltDriveCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4009,
        )

        return self.__parent__._cast(_4009.BeltDriveCompoundStabilityAnalysis)

    @property
    def bevel_differential_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4012.BevelDifferentialGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4012,
        )

        return self.__parent__._cast(
            _4012.BevelDifferentialGearSetCompoundStabilityAnalysis
        )

    @property
    def bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4017.BevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4017,
        )

        return self.__parent__._cast(_4017.BevelGearSetCompoundStabilityAnalysis)

    @property
    def bolted_joint_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4019.BoltedJointCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4019,
        )

        return self.__parent__._cast(_4019.BoltedJointCompoundStabilityAnalysis)

    @property
    def clutch_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4020.ClutchCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4020,
        )

        return self.__parent__._cast(_4020.ClutchCompoundStabilityAnalysis)

    @property
    def concept_coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4025.ConceptCouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4025,
        )

        return self.__parent__._cast(_4025.ConceptCouplingCompoundStabilityAnalysis)

    @property
    def concept_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4030.ConceptGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4030,
        )

        return self.__parent__._cast(_4030.ConceptGearSetCompoundStabilityAnalysis)

    @property
    def conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4033.ConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4033,
        )

        return self.__parent__._cast(_4033.ConicalGearSetCompoundStabilityAnalysis)

    @property
    def coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4036.CouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4036,
        )

        return self.__parent__._cast(_4036.CouplingCompoundStabilityAnalysis)

    @property
    def cvt_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4040.CVTCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4040,
        )

        return self.__parent__._cast(_4040.CVTCompoundStabilityAnalysis)

    @property
    def cycloidal_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4042.CycloidalAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4042,
        )

        return self.__parent__._cast(_4042.CycloidalAssemblyCompoundStabilityAnalysis)

    @property
    def cylindrical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4048.CylindricalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4048,
        )

        return self.__parent__._cast(_4048.CylindricalGearSetCompoundStabilityAnalysis)

    @property
    def face_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4054.FaceGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4054,
        )

        return self.__parent__._cast(_4054.FaceGearSetCompoundStabilityAnalysis)

    @property
    def flexible_pin_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4056.FlexiblePinAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4056,
        )

        return self.__parent__._cast(_4056.FlexiblePinAssemblyCompoundStabilityAnalysis)

    @property
    def gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4059.GearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4059,
        )

        return self.__parent__._cast(_4059.GearSetCompoundStabilityAnalysis)

    @property
    def hypoid_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4063.HypoidGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4063,
        )

        return self.__parent__._cast(_4063.HypoidGearSetCompoundStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4067.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4067,
        )

        return self.__parent__._cast(
            _4067.KlingelnbergCycloPalloidConicalGearSetCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4070.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4070,
        )

        return self.__parent__._cast(
            _4070.KlingelnbergCycloPalloidHypoidGearSetCompoundStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4073.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4073,
        )

        return self.__parent__._cast(
            _4073.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundStabilityAnalysis
        )

    @property
    def microphone_array_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4076.MicrophoneArrayCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4076,
        )

        return self.__parent__._cast(_4076.MicrophoneArrayCompoundStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4081.PartToPartShearCouplingCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4081,
        )

        return self.__parent__._cast(
            _4081.PartToPartShearCouplingCompoundStabilityAnalysis
        )

    @property
    def planetary_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4085.PlanetaryGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4085,
        )

        return self.__parent__._cast(_4085.PlanetaryGearSetCompoundStabilityAnalysis)

    @property
    def rolling_ring_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4092.RollingRingAssemblyCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4092,
        )

        return self.__parent__._cast(_4092.RollingRingAssemblyCompoundStabilityAnalysis)

    @property
    def spiral_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4102.SpiralBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4102,
        )

        return self.__parent__._cast(_4102.SpiralBevelGearSetCompoundStabilityAnalysis)

    @property
    def spring_damper_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4103.SpringDamperCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4103,
        )

        return self.__parent__._cast(_4103.SpringDamperCompoundStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4108.StraightBevelDiffGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4108,
        )

        return self.__parent__._cast(
            _4108.StraightBevelDiffGearSetCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4111.StraightBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4111,
        )

        return self.__parent__._cast(
            _4111.StraightBevelGearSetCompoundStabilityAnalysis
        )

    @property
    def synchroniser_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4114.SynchroniserCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4114,
        )

        return self.__parent__._cast(_4114.SynchroniserCompoundStabilityAnalysis)

    @property
    def torque_converter_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4118.TorqueConverterCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4118,
        )

        return self.__parent__._cast(_4118.TorqueConverterCompoundStabilityAnalysis)

    @property
    def worm_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4126.WormGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4126,
        )

        return self.__parent__._cast(_4126.WormGearSetCompoundStabilityAnalysis)

    @property
    def zerol_bevel_gear_set_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4129.ZerolBevelGearSetCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4129,
        )

        return self.__parent__._cast(_4129.ZerolBevelGearSetCompoundStabilityAnalysis)

    @property
    def specialised_assembly_compound_stability_analysis(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundStabilityAnalysis":
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
class SpecialisedAssemblyCompoundStabilityAnalysis(
    _3999.AbstractAssemblyCompoundStabilityAnalysis
):
    """SpecialisedAssemblyCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_3965.SpecialisedAssemblyStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.SpecialisedAssemblyStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3965.SpecialisedAssemblyStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.SpecialisedAssemblyStabilityAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssemblyCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundStabilityAnalysis
        """
        return _Cast_SpecialisedAssemblyCompoundStabilityAnalysis(self)
