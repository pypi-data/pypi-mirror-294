"""CouplingHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _6245,
)

_COUPLING_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "CouplingHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6143,
        _6166,
        _6171,
        _6226,
        _6229,
        _6251,
        _6265,
    )
    from mastapy._private.system_model.part_model.couplings import _2642

    Self = TypeVar("Self", bound="CouplingHarmonicAnalysisOfSingleExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHarmonicAnalysisOfSingleExcitation._Cast_CouplingHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting CouplingHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "CouplingHarmonicAnalysisOfSingleExcitation"

    @property
    def specialised_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6245.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(
            _6245.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_assembly_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6143.AbstractAssemblyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6143,
        )

        return self.__parent__._cast(
            _6143.AbstractAssemblyHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6226.PartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6226,
        )

        return self.__parent__._cast(_6226.PartHarmonicAnalysisOfSingleExcitation)

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
    def clutch_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6166.ClutchHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6166,
        )

        return self.__parent__._cast(_6166.ClutchHarmonicAnalysisOfSingleExcitation)

    @property
    def concept_coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6171.ConceptCouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6171,
        )

        return self.__parent__._cast(
            _6171.ConceptCouplingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_to_part_shear_coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6229.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6229,
        )

        return self.__parent__._cast(
            _6229.PartToPartShearCouplingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6251.SpringDamperHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6251,
        )

        return self.__parent__._cast(
            _6251.SpringDamperHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6265.TorqueConverterHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6265,
        )

        return self.__parent__._cast(
            _6265.TorqueConverterHarmonicAnalysisOfSingleExcitation
        )

    @property
    def coupling_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "CouplingHarmonicAnalysisOfSingleExcitation":
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
class CouplingHarmonicAnalysisOfSingleExcitation(
    _6245.SpecialisedAssemblyHarmonicAnalysisOfSingleExcitation
):
    """CouplingHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2642.Coupling":
        """mastapy.system_model.part_model.couplings.Coupling

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_CouplingHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_CouplingHarmonicAnalysisOfSingleExcitation(self)
