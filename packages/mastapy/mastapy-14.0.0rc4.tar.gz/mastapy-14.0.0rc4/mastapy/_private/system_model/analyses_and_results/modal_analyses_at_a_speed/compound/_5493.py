"""VirtualComponentCompoundModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5448,
)

_VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "VirtualComponentCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5362,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5394,
        _5444,
        _5445,
        _5450,
        _5457,
        _5458,
        _5492,
    )

    Self = TypeVar("Self", bound="VirtualComponentCompoundModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentCompoundModalAnalysisAtASpeed._Cast_VirtualComponentCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentCompoundModalAnalysisAtASpeed:
    """Special nested class for casting VirtualComponentCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "VirtualComponentCompoundModalAnalysisAtASpeed"

    @property
    def mountable_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5448.MountableComponentCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(
            _5448.MountableComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5394.ComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5394,
        )

        return self.__parent__._cast(_5394.ComponentCompoundModalAnalysisAtASpeed)

    @property
    def part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5450.PartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5450,
        )

        return self.__parent__._cast(_5450.PartCompoundModalAnalysisAtASpeed)

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
    def mass_disc_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5444.MassDiscCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5444,
        )

        return self.__parent__._cast(_5444.MassDiscCompoundModalAnalysisAtASpeed)

    @property
    def measurement_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5445.MeasurementComponentCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5445,
        )

        return self.__parent__._cast(
            _5445.MeasurementComponentCompoundModalAnalysisAtASpeed
        )

    @property
    def point_load_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5457.PointLoadCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5457,
        )

        return self.__parent__._cast(_5457.PointLoadCompoundModalAnalysisAtASpeed)

    @property
    def power_load_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5458.PowerLoadCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5458,
        )

        return self.__parent__._cast(_5458.PowerLoadCompoundModalAnalysisAtASpeed)

    @property
    def unbalanced_mass_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5492.UnbalancedMassCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5492,
        )

        return self.__parent__._cast(_5492.UnbalancedMassCompoundModalAnalysisAtASpeed)

    @property
    def virtual_component_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "VirtualComponentCompoundModalAnalysisAtASpeed":
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
class VirtualComponentCompoundModalAnalysisAtASpeed(
    _5448.MountableComponentCompoundModalAnalysisAtASpeed
):
    """VirtualComponentCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5362.VirtualComponentModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.VirtualComponentModalAnalysisAtASpeed]

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5362.VirtualComponentModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.VirtualComponentModalAnalysisAtASpeed]

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
    def cast_to(self: "Self") -> "_Cast_VirtualComponentCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentCompoundModalAnalysisAtASpeed
        """
        return _Cast_VirtualComponentCompoundModalAnalysisAtASpeed(self)
