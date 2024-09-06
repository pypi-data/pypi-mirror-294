"""SpecialisedAssemblyCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6012,
)

_SPECIALISED_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "SpecialisedAssemblyCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5943,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6018,
        _6022,
        _6025,
        _6030,
        _6032,
        _6033,
        _6038,
        _6043,
        _6046,
        _6049,
        _6053,
        _6055,
        _6061,
        _6067,
        _6069,
        _6072,
        _6076,
        _6080,
        _6083,
        _6086,
        _6089,
        _6093,
        _6094,
        _6098,
        _6105,
        _6115,
        _6116,
        _6121,
        _6124,
        _6127,
        _6131,
        _6139,
        _6142,
    )

    Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundHarmonicAnalysis._Cast_SpecialisedAssemblyCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundHarmonicAnalysis:
    """Special nested class for casting SpecialisedAssemblyCompoundHarmonicAnalysis to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundHarmonicAnalysis"

    @property
    def abstract_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6012.AbstractAssemblyCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6012.AbstractAssemblyCompoundHarmonicAnalysis)

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6093.PartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6093,
        )

        return self.__parent__._cast(_6093.PartCompoundHarmonicAnalysis)

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
    def agma_gleason_conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6018.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6018,
        )

        return self.__parent__._cast(
            _6018.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis
        )

    @property
    def belt_drive_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6022.BeltDriveCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6022,
        )

        return self.__parent__._cast(_6022.BeltDriveCompoundHarmonicAnalysis)

    @property
    def bevel_differential_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6025.BevelDifferentialGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6025,
        )

        return self.__parent__._cast(
            _6025.BevelDifferentialGearSetCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6030.BevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6030,
        )

        return self.__parent__._cast(_6030.BevelGearSetCompoundHarmonicAnalysis)

    @property
    def bolted_joint_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6032.BoltedJointCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6032,
        )

        return self.__parent__._cast(_6032.BoltedJointCompoundHarmonicAnalysis)

    @property
    def clutch_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6033.ClutchCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6033,
        )

        return self.__parent__._cast(_6033.ClutchCompoundHarmonicAnalysis)

    @property
    def concept_coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6038.ConceptCouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6038,
        )

        return self.__parent__._cast(_6038.ConceptCouplingCompoundHarmonicAnalysis)

    @property
    def concept_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6043.ConceptGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6043,
        )

        return self.__parent__._cast(_6043.ConceptGearSetCompoundHarmonicAnalysis)

    @property
    def conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6046.ConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6046,
        )

        return self.__parent__._cast(_6046.ConicalGearSetCompoundHarmonicAnalysis)

    @property
    def coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6049.CouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6049,
        )

        return self.__parent__._cast(_6049.CouplingCompoundHarmonicAnalysis)

    @property
    def cvt_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6053.CVTCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6053,
        )

        return self.__parent__._cast(_6053.CVTCompoundHarmonicAnalysis)

    @property
    def cycloidal_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6055.CycloidalAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6055,
        )

        return self.__parent__._cast(_6055.CycloidalAssemblyCompoundHarmonicAnalysis)

    @property
    def cylindrical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6061.CylindricalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6061,
        )

        return self.__parent__._cast(_6061.CylindricalGearSetCompoundHarmonicAnalysis)

    @property
    def face_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6067.FaceGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6067,
        )

        return self.__parent__._cast(_6067.FaceGearSetCompoundHarmonicAnalysis)

    @property
    def flexible_pin_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6069.FlexiblePinAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6069,
        )

        return self.__parent__._cast(_6069.FlexiblePinAssemblyCompoundHarmonicAnalysis)

    @property
    def gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6072.GearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6072,
        )

        return self.__parent__._cast(_6072.GearSetCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6076.HypoidGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6076,
        )

        return self.__parent__._cast(_6076.HypoidGearSetCompoundHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6080.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6080,
        )

        return self.__parent__._cast(
            _6080.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6083.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6083,
        )

        return self.__parent__._cast(
            _6083.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6086.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6086,
        )

        return self.__parent__._cast(
            _6086.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis
        )

    @property
    def microphone_array_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6089.MicrophoneArrayCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6089,
        )

        return self.__parent__._cast(_6089.MicrophoneArrayCompoundHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6094.PartToPartShearCouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6094,
        )

        return self.__parent__._cast(
            _6094.PartToPartShearCouplingCompoundHarmonicAnalysis
        )

    @property
    def planetary_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6098.PlanetaryGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6098,
        )

        return self.__parent__._cast(_6098.PlanetaryGearSetCompoundHarmonicAnalysis)

    @property
    def rolling_ring_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6105.RollingRingAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6105,
        )

        return self.__parent__._cast(_6105.RollingRingAssemblyCompoundHarmonicAnalysis)

    @property
    def spiral_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6115.SpiralBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6115,
        )

        return self.__parent__._cast(_6115.SpiralBevelGearSetCompoundHarmonicAnalysis)

    @property
    def spring_damper_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6116.SpringDamperCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6116,
        )

        return self.__parent__._cast(_6116.SpringDamperCompoundHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6121.StraightBevelDiffGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6121,
        )

        return self.__parent__._cast(
            _6121.StraightBevelDiffGearSetCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6124.StraightBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6124,
        )

        return self.__parent__._cast(_6124.StraightBevelGearSetCompoundHarmonicAnalysis)

    @property
    def synchroniser_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6127.SynchroniserCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6127,
        )

        return self.__parent__._cast(_6127.SynchroniserCompoundHarmonicAnalysis)

    @property
    def torque_converter_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6131.TorqueConverterCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6131,
        )

        return self.__parent__._cast(_6131.TorqueConverterCompoundHarmonicAnalysis)

    @property
    def worm_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6139.WormGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6139,
        )

        return self.__parent__._cast(_6139.WormGearSetCompoundHarmonicAnalysis)

    @property
    def zerol_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6142.ZerolBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6142,
        )

        return self.__parent__._cast(_6142.ZerolBevelGearSetCompoundHarmonicAnalysis)

    @property
    def specialised_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundHarmonicAnalysis":
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
class SpecialisedAssemblyCompoundHarmonicAnalysis(
    _6012.AbstractAssemblyCompoundHarmonicAnalysis
):
    """SpecialisedAssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5943.SpecialisedAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.SpecialisedAssemblyHarmonicAnalysis]

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
    ) -> "List[_5943.SpecialisedAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.SpecialisedAssemblyHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssemblyCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundHarmonicAnalysis
        """
        return _Cast_SpecialisedAssemblyCompoundHarmonicAnalysis(self)
