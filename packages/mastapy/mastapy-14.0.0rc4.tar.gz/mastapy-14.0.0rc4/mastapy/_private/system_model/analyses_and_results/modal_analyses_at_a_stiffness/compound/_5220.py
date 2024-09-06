"""StraightBevelSunGearCompoundModalAnalysisAtAStiffness"""

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
    _5213,
)

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "StraightBevelSunGearCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5089,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5110,
        _5122,
        _5131,
        _5138,
        _5164,
        _5185,
        _5187,
    )

    Self = TypeVar(
        "Self", bound="StraightBevelSunGearCompoundModalAnalysisAtAStiffness"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelSunGearCompoundModalAnalysisAtAStiffness._Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGearCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting StraightBevelSunGearCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "StraightBevelSunGearCompoundModalAnalysisAtAStiffness"

    @property
    def straight_bevel_diff_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5213.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5213.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5122.BevelGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5122,
        )

        return self.__parent__._cast(_5122.BevelGearCompoundModalAnalysisAtAStiffness)

    @property
    def agma_gleason_conical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5110.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5110,
        )

        return self.__parent__._cast(
            _5110.AGMAGleasonConicalGearCompoundModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5138.ConicalGearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5138,
        )

        return self.__parent__._cast(_5138.ConicalGearCompoundModalAnalysisAtAStiffness)

    @property
    def gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5164.GearCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5164,
        )

        return self.__parent__._cast(_5164.GearCompoundModalAnalysisAtAStiffness)

    @property
    def mountable_component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5185.MountableComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5185,
        )

        return self.__parent__._cast(
            _5185.MountableComponentCompoundModalAnalysisAtAStiffness
        )

    @property
    def component_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5131.ComponentCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5131,
        )

        return self.__parent__._cast(_5131.ComponentCompoundModalAnalysisAtAStiffness)

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
    def straight_bevel_sun_gear_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "StraightBevelSunGearCompoundModalAnalysisAtAStiffness":
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
class StraightBevelSunGearCompoundModalAnalysisAtAStiffness(
    _5213.StraightBevelDiffGearCompoundModalAnalysisAtAStiffness
):
    """StraightBevelSunGearCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5089.StraightBevelSunGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.StraightBevelSunGearModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5089.StraightBevelSunGearModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.StraightBevelSunGearModalAnalysisAtAStiffness]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness
        """
        return _Cast_StraightBevelSunGearCompoundModalAnalysisAtAStiffness(self)
