"""ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed"""

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
    _5372,
)

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
        "ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5337,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5393,
        _5404,
        _5413,
        _5454,
    )

    Self = TypeVar(
        "Self", bound="ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed._Cast_ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed:
    """Special nested class for casting ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed"

    @property
    def abstract_shaft_to_mountable_component_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_5372.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed"
    ):
        return self.__parent__._cast(
            _5372.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5404.ConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5404,
        )

        return self.__parent__._cast(_5404.ConnectionCompoundModalAnalysisAtASpeed)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7708.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7708,
        )

        return self.__parent__._cast(_7708.ConnectionCompoundAnalysis)

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
    def coaxial_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5393.CoaxialConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5393,
        )

        return self.__parent__._cast(
            _5393.CoaxialConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5413.CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5413,
        )

        return self.__parent__._cast(
            _5413.CycloidalDiscCentralBearingConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def planetary_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5454.PlanetaryConnectionCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5454,
        )

        return self.__parent__._cast(
            _5454.PlanetaryConnectionCompoundModalAnalysisAtASpeed
        )

    @property
    def shaft_to_mountable_component_connection_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed":
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
class ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed(
    _5372.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed
):
    """ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5337.ShaftToMountableComponentConnectionModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.ShaftToMountableComponentConnectionModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5337.ShaftToMountableComponentConnectionModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.ShaftToMountableComponentConnectionModalAnalysisAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed
        """
        return _Cast_ShaftToMountableComponentConnectionCompoundModalAnalysisAtASpeed(
            self
        )
