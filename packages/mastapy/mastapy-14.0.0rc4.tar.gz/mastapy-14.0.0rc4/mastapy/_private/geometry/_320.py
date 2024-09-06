"""DrawStyleBase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DRAW_STYLE_BASE = python_net_import("SMT.MastaAPI.Geometry", "DrawStyleBase")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.geometry import _319
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6727,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6469,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5893,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5585
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4770
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4183,
        _4229,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4130
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3973,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3180,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2912,
    )
    from mastapy._private.system_model.drawing import _2300, _2306

    Self = TypeVar("Self", bound="DrawStyleBase")
    CastSelf = TypeVar("CastSelf", bound="DrawStyleBase._Cast_DrawStyleBase")


__docformat__ = "restructuredtext en"
__all__ = ("DrawStyleBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DrawStyleBase:
    """Special nested class for casting DrawStyleBase to subclasses."""

    __parent__: "DrawStyleBase"

    @property
    def draw_style(self: "CastSelf") -> "_319.DrawStyle":
        from mastapy._private.geometry import _319

        return self.__parent__._cast(_319.DrawStyle)

    @property
    def contour_draw_style(self: "CastSelf") -> "_2300.ContourDrawStyle":
        from mastapy._private.system_model.drawing import _2300

        return self.__parent__._cast(_2300.ContourDrawStyle)

    @property
    def model_view_options_draw_style(
        self: "CastSelf",
    ) -> "_2306.ModelViewOptionsDrawStyle":
        from mastapy._private.system_model.drawing import _2306

        return self.__parent__._cast(_2306.ModelViewOptionsDrawStyle)

    @property
    def system_deflection_draw_style(
        self: "CastSelf",
    ) -> "_2912.SystemDeflectionDrawStyle":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2912,
        )

        return self.__parent__._cast(_2912.SystemDeflectionDrawStyle)

    @property
    def steady_state_synchronous_response_draw_style(
        self: "CastSelf",
    ) -> "_3180.SteadyStateSynchronousResponseDrawStyle":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3180,
        )

        return self.__parent__._cast(_3180.SteadyStateSynchronousResponseDrawStyle)

    @property
    def stability_analysis_draw_style(
        self: "CastSelf",
    ) -> "_3973.StabilityAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3973,
        )

        return self.__parent__._cast(_3973.StabilityAnalysisDrawStyle)

    @property
    def rotor_dynamics_draw_style(self: "CastSelf") -> "_4130.RotorDynamicsDrawStyle":
        from mastapy._private.system_model.analyses_and_results.rotor_dynamics import (
            _4130,
        )

        return self.__parent__._cast(_4130.RotorDynamicsDrawStyle)

    @property
    def cylindrical_gear_geometric_entity_draw_style(
        self: "CastSelf",
    ) -> "_4183.CylindricalGearGeometricEntityDrawStyle":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4183

        return self.__parent__._cast(_4183.CylindricalGearGeometricEntityDrawStyle)

    @property
    def power_flow_draw_style(self: "CastSelf") -> "_4229.PowerFlowDrawStyle":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4229

        return self.__parent__._cast(_4229.PowerFlowDrawStyle)

    @property
    def modal_analysis_draw_style(self: "CastSelf") -> "_4770.ModalAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4770,
        )

        return self.__parent__._cast(_4770.ModalAnalysisDrawStyle)

    @property
    def mbd_analysis_draw_style(self: "CastSelf") -> "_5585.MBDAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5585,
        )

        return self.__parent__._cast(_5585.MBDAnalysisDrawStyle)

    @property
    def harmonic_analysis_draw_style(
        self: "CastSelf",
    ) -> "_5893.HarmonicAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5893,
        )

        return self.__parent__._cast(_5893.HarmonicAnalysisDrawStyle)

    @property
    def dynamic_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6469.DynamicAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6469,
        )

        return self.__parent__._cast(_6469.DynamicAnalysisDrawStyle)

    @property
    def critical_speed_analysis_draw_style(
        self: "CastSelf",
    ) -> "_6727.CriticalSpeedAnalysisDrawStyle":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6727,
        )

        return self.__parent__._cast(_6727.CriticalSpeedAnalysisDrawStyle)

    @property
    def draw_style_base(self: "CastSelf") -> "DrawStyleBase":
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
class DrawStyleBase(_0.APIBase):
    """DrawStyleBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DRAW_STYLE_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def show_microphones(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowMicrophones")

        if temp is None:
            return False

        return temp

    @show_microphones.setter
    @enforce_parameter_types
    def show_microphones(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowMicrophones", bool(value) if value is not None else False
        )

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
    def cast_to(self: "Self") -> "_Cast_DrawStyleBase":
        """Cast to another type.

        Returns:
            _Cast_DrawStyleBase
        """
        return _Cast_DrawStyleBase(self)
