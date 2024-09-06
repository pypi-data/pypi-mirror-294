"""ConicalGearSetCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5166,
)

_CONICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "ConicalGearSetCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5007,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5106,
        _5112,
        _5119,
        _5124,
        _5170,
        _5174,
        _5177,
        _5180,
        _5187,
        _5206,
        _5209,
        _5215,
        _5218,
        _5236,
    )

    Self = TypeVar("Self", bound="ConicalGearSetCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetCompoundModalAnalysisAtAStiffness._Cast_ConicalGearSetCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting ConicalGearSetCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "ConicalGearSetCompoundModalAnalysisAtAStiffness"

    @property
    def gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5166.GearSetCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5166.GearSetCompoundModalAnalysisAtAStiffness)

    @property
    def specialised_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5206.SpecialisedAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5206,
        )

        return self.__parent__._cast(
            _5206.SpecialisedAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def abstract_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5106.AbstractAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5106,
        )

        return self.__parent__._cast(
            _5106.AbstractAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5187.PartCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5187,
        )

        return self.__parent__._cast(_5187.PartCompoundModalAnalysisAtAStiffness)

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
    def agma_gleason_conical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5112.AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5112,
        )

        return self.__parent__._cast(
            _5112.AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_differential_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5119.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5119,
        )

        return self.__parent__._cast(
            _5119.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5124.BevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5124,
        )

        return self.__parent__._cast(
            _5124.BevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def hypoid_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5170.HypoidGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5170,
        )

        return self.__parent__._cast(
            _5170.HypoidGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5174.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5174,
        )

        return self.__parent__._cast(
            _5174.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5177.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5177,
        )

        return self.__parent__._cast(
            _5177.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5180.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5180,
        )

        return self.__parent__._cast(
            _5180.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5209.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5209,
        )

        return self.__parent__._cast(
            _5209.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5215.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5215,
        )

        return self.__parent__._cast(
            _5215.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5218.StraightBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5218,
        )

        return self.__parent__._cast(
            _5218.StraightBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def zerol_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5236.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5236,
        )

        return self.__parent__._cast(
            _5236.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "ConicalGearSetCompoundModalAnalysisAtAStiffness":
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
class ConicalGearSetCompoundModalAnalysisAtAStiffness(
    _5166.GearSetCompoundModalAnalysisAtAStiffness
):
    """ConicalGearSetCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5007.ConicalGearSetModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ConicalGearSetModalAnalysisAtAStiffness]

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
    ) -> "List[_5007.ConicalGearSetModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.ConicalGearSetModalAnalysisAtAStiffness]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConicalGearSetCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetCompoundModalAnalysisAtAStiffness
        """
        return _Cast_ConicalGearSetCompoundModalAnalysisAtAStiffness(self)
