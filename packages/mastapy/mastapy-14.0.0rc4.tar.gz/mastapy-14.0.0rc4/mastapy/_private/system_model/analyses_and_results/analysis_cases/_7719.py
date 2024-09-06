"""StaticLoadAnalysisCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7704

_STATIC_LOAD_ANALYSIS_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases",
    "StaticLoadAnalysisCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2734
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7427,
        _7429,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7159,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7706,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6726,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6468,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5863,
        _5892,
        _5896,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6205,
        _6223,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4737,
        _4768,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5316,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5025,
        _5053,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4228
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3916,
        _3972,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6952
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3123,
        _3179,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3707,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3444,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2911,
        _2918,
    )

    Self = TypeVar("Self", bound="StaticLoadAnalysisCase")
    CastSelf = TypeVar(
        "CastSelf", bound="StaticLoadAnalysisCase._Cast_StaticLoadAnalysisCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StaticLoadAnalysisCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StaticLoadAnalysisCase:
    """Special nested class for casting StaticLoadAnalysisCase to subclasses."""

    __parent__: "StaticLoadAnalysisCase"

    @property
    def analysis_case(self: "CastSelf") -> "_7704.AnalysisCase":
        return self.__parent__._cast(_7704.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2734.Context":
        from mastapy._private.system_model.analyses_and_results import _2734

        return self.__parent__._cast(_2734.Context)

    @property
    def system_deflection(self: "CastSelf") -> "_2911.SystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2911,
        )

        return self.__parent__._cast(_2911.SystemDeflection)

    @property
    def torsional_system_deflection(
        self: "CastSelf",
    ) -> "_2918.TorsionalSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2918,
        )

        return self.__parent__._cast(_2918.TorsionalSystemDeflection)

    @property
    def dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3123.DynamicModelForSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3123,
        )

        return self.__parent__._cast(
            _3123.DynamicModelForSteadyStateSynchronousResponse
        )

    @property
    def steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3179.SteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3179,
        )

        return self.__parent__._cast(_3179.SteadyStateSynchronousResponse)

    @property
    def steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3444.SteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3444,
        )

        return self.__parent__._cast(_3444.SteadyStateSynchronousResponseOnAShaft)

    @property
    def steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3707.SteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3707,
        )

        return self.__parent__._cast(_3707.SteadyStateSynchronousResponseAtASpeed)

    @property
    def dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_3916.DynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3916,
        )

        return self.__parent__._cast(_3916.DynamicModelForStabilityAnalysis)

    @property
    def stability_analysis(self: "CastSelf") -> "_3972.StabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3972,
        )

        return self.__parent__._cast(_3972.StabilityAnalysis)

    @property
    def power_flow(self: "CastSelf") -> "_4228.PowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4228

        return self.__parent__._cast(_4228.PowerFlow)

    @property
    def dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_4737.DynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4737,
        )

        return self.__parent__._cast(_4737.DynamicModelForModalAnalysis)

    @property
    def modal_analysis(self: "CastSelf") -> "_4768.ModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4768,
        )

        return self.__parent__._cast(_4768.ModalAnalysis)

    @property
    def dynamic_model_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5025.DynamicModelAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5025,
        )

        return self.__parent__._cast(_5025.DynamicModelAtAStiffness)

    @property
    def modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5053.ModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5053,
        )

        return self.__parent__._cast(_5053.ModalAnalysisAtAStiffness)

    @property
    def modal_analysis_at_a_speed(self: "CastSelf") -> "_5316.ModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5316,
        )

        return self.__parent__._cast(_5316.ModalAnalysisAtASpeed)

    @property
    def dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5863.DynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5863,
        )

        return self.__parent__._cast(_5863.DynamicModelForHarmonicAnalysis)

    @property
    def harmonic_analysis(self: "CastSelf") -> "_5892.HarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5892,
        )

        return self.__parent__._cast(_5892.HarmonicAnalysis)

    @property
    def harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_5896.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5896,
        )

        return self.__parent__._cast(
            _5896.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6205.HarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6205,
        )

        return self.__parent__._cast(_6205.HarmonicAnalysisOfSingleExcitation)

    @property
    def modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6223.ModalAnalysisForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6223,
        )

        return self.__parent__._cast(_6223.ModalAnalysisForHarmonicAnalysis)

    @property
    def dynamic_analysis(self: "CastSelf") -> "_6468.DynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6468,
        )

        return self.__parent__._cast(_6468.DynamicAnalysis)

    @property
    def critical_speed_analysis(self: "CastSelf") -> "_6726.CriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6726,
        )

        return self.__parent__._cast(_6726.CriticalSpeedAnalysis)

    @property
    def advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7159.AdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7159,
        )

        return self.__parent__._cast(_7159.AdvancedTimeSteppingAnalysisForModulation)

    @property
    def advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7427.AdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7427,
        )

        return self.__parent__._cast(_7427.AdvancedSystemDeflection)

    @property
    def advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_7429.AdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7429,
        )

        return self.__parent__._cast(_7429.AdvancedSystemDeflectionSubAnalysis)

    @property
    def compound_analysis_case(self: "CastSelf") -> "_7706.CompoundAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7706,
        )

        return self.__parent__._cast(_7706.CompoundAnalysisCase)

    @property
    def fe_analysis(self: "CastSelf") -> "_7713.FEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7713,
        )

        return self.__parent__._cast(_7713.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "StaticLoadAnalysisCase":
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
class StaticLoadAnalysisCase(_7704.AnalysisCase):
    """StaticLoadAnalysisCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATIC_LOAD_ANALYSIS_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def load_case(self: "Self") -> "_6952.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StaticLoadAnalysisCase":
        """Cast to another type.

        Returns:
            _Cast_StaticLoadAnalysisCase
        """
        return _Cast_StaticLoadAnalysisCase(self)
