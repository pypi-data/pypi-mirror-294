"""CVTHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5820

_CVT_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "CVTHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5809,
        _5921,
        _5943,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2818,
    )
    from mastapy._private.system_model.part_model.couplings import _2645

    Self = TypeVar("Self", bound="CVTHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="CVTHarmonicAnalysis._Cast_CVTHarmonicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTHarmonicAnalysis:
    """Special nested class for casting CVTHarmonicAnalysis to subclasses."""

    __parent__: "CVTHarmonicAnalysis"

    @property
    def belt_drive_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5820.BeltDriveHarmonicAnalysis":
        return self.__parent__._cast(_5820.BeltDriveHarmonicAnalysis)

    @property
    def specialised_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5943.SpecialisedAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5943,
        )

        return self.__parent__._cast(_5943.SpecialisedAssemblyHarmonicAnalysis)

    @property
    def abstract_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5809.AbstractAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5809,
        )

        return self.__parent__._cast(_5809.AbstractAssemblyHarmonicAnalysis)

    @property
    def part_harmonic_analysis(self: "CastSelf") -> "_5921.PartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5921,
        )

        return self.__parent__._cast(_5921.PartHarmonicAnalysis)

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
    def cvt_harmonic_analysis(self: "CastSelf") -> "CVTHarmonicAnalysis":
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
class CVTHarmonicAnalysis(_5820.BeltDriveHarmonicAnalysis):
    """CVTHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2645.CVT":
        """mastapy.system_model.part_model.couplings.CVT

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: "Self") -> "_2818.CVTSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CVTSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CVTHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CVTHarmonicAnalysis
        """
        return _Cast_CVTHarmonicAnalysis(self)
