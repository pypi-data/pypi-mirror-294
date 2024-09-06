"""KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis"""

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
    _6080,
)

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
        "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5914,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6012,
        _6046,
        _6072,
        _6084,
        _6085,
        _6093,
        _6112,
    )
    from mastapy._private.system_model.part_model.gears import _2598

    Self = TypeVar(
        "Self",
        bound="KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis._Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6080.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis":
        return self.__parent__._cast(
            _6080.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis
        )

    @property
    def conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6046.ConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6046,
        )

        return self.__parent__._cast(_6046.ConicalGearSetCompoundHarmonicAnalysis)

    @property
    def gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6072.GearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6072,
        )

        return self.__parent__._cast(_6072.GearSetCompoundHarmonicAnalysis)

    @property
    def specialised_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6112.SpecialisedAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6112,
        )

        return self.__parent__._cast(_6112.SpecialisedAssemblyCompoundHarmonicAnalysis)

    @property
    def abstract_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6012.AbstractAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6012,
        )

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
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis":
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
class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis(
    _6080.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis
):
    """KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS
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
    ) -> "_2598.KlingelnbergCycloPalloidSpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(
        self: "Self",
    ) -> "_2598.KlingelnbergCycloPalloidSpiralBevelGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5914.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]

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
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_harmonic_analysis(
        self: "Self",
    ) -> "List[_6084.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidSpiralBevelGearsCompoundHarmonicAnalysis",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_harmonic_analysis(
        self: "Self",
    ) -> "List[_6085.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "KlingelnbergCycloPalloidSpiralBevelMeshesCompoundHarmonicAnalysis",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5914.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis(
            self
        )
