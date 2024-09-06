"""Context"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CONTEXT = python_net_import("SMT.MastaAPI.SystemModel.AnalysesAndResults", "Context")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2254
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7427,
        _7429,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7159,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7704,
        _7706,
        _7713,
        _7719,
        _7720,
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
        _5901,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6205,
        _6223,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5592
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
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4497,
        _4498,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4228
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3916,
        _3972,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6951,
        _6952,
        _6953,
        _6959,
    )
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
    from mastapy._private.utility import _1632

    Self = TypeVar("Self", bound="Context")
    CastSelf = TypeVar("CastSelf", bound="Context._Cast_Context")


__docformat__ = "restructuredtext en"
__all__ = ("Context",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Context:
    """Special nested class for casting Context to subclasses."""

    __parent__: "Context"

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
    def parametric_study_static_load(
        self: "CastSelf",
    ) -> "_4497.ParametricStudyStaticLoad":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4497,
        )

        return self.__parent__._cast(_4497.ParametricStudyStaticLoad)

    @property
    def parametric_study_tool(self: "CastSelf") -> "_4498.ParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4498,
        )

        return self.__parent__._cast(_4498.ParametricStudyTool)

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
    def multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5592.MultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5592,
        )

        return self.__parent__._cast(_5592.MultibodyDynamicsAnalysis)

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
    def harmonic_analysis_with_varying_stiffness_static_load_case(
        self: "CastSelf",
    ) -> "_5901.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5901,
        )

        return self.__parent__._cast(
            _5901.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase
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
    def load_case(self: "CastSelf") -> "_6951.LoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6951,
        )

        return self.__parent__._cast(_6951.LoadCase)

    @property
    def static_load_case(self: "CastSelf") -> "_6952.StaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6952,
        )

        return self.__parent__._cast(_6952.StaticLoadCase)

    @property
    def time_series_load_case(self: "CastSelf") -> "_6953.TimeSeriesLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6953,
        )

        return self.__parent__._cast(_6953.TimeSeriesLoadCase)

    @property
    def advanced_time_stepping_analysis_for_modulation_static_load_case(
        self: "CastSelf",
    ) -> "_6959.AdvancedTimeSteppingAnalysisForModulationStaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6959,
        )

        return self.__parent__._cast(
            _6959.AdvancedTimeSteppingAnalysisForModulationStaticLoadCase
        )

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
    def analysis_case(self: "CastSelf") -> "_7704.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7704,
        )

        return self.__parent__._cast(_7704.AnalysisCase)

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
    def static_load_analysis_case(self: "CastSelf") -> "_7719.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.StaticLoadAnalysisCase)

    @property
    def time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.TimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.TimeSeriesLoadAnalysisCase)

    @property
    def context(self: "CastSelf") -> "Context":
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
class Context(_0.APIBase):
    """Context

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONTEXT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def save_history_information(self: "Self") -> "_1632.FileHistoryItem":
        """mastapy.utility.FileHistoryItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SaveHistoryInformation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def design_properties(self: "Self") -> "_2254.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_Context":
        """Cast to another type.

        Returns:
            _Cast_Context
        """
        return _Cast_Context(self)
