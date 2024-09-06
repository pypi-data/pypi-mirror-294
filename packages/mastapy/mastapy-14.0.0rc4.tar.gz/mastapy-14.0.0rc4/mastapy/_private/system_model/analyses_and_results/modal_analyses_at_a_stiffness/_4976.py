"""AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _5008,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness",
        "AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _4997,
        _5017,
        _5019,
        _5060,
        _5074,
    )
    from mastapy._private.system_model.connections_and_sockets import _2319

    Self = TypeVar(
        "Self",
        bound="AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness._Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness"

    @property
    def connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5008.ConnectionModalAnalysisAtAStiffness":
        return self.__parent__._cast(_5008.ConnectionModalAnalysisAtAStiffness)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7710.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7707.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7707,
        )

        return self.__parent__._cast(_7707.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2733.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2733

        return self.__parent__._cast(_2733.ConnectionAnalysis)

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
    def coaxial_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_4997.CoaxialConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _4997,
        )

        return self.__parent__._cast(_4997.CoaxialConnectionModalAnalysisAtAStiffness)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5017.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5017,
        )

        return self.__parent__._cast(
            _5017.CycloidalDiscCentralBearingConnectionModalAnalysisAtAStiffness
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5019.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5019,
        )

        return self.__parent__._cast(
            _5019.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness
        )

    @property
    def planetary_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5060.PlanetaryConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5060,
        )

        return self.__parent__._cast(_5060.PlanetaryConnectionModalAnalysisAtAStiffness)

    @property
    def shaft_to_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5074.ShaftToMountableComponentConnectionModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5074,
        )

        return self.__parent__._cast(
            _5074.ShaftToMountableComponentConnectionModalAnalysisAtAStiffness
        )

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness":
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
class AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness(
    _5008.ConnectionModalAnalysisAtAStiffness
):
    """AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_STIFFNESS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(
        self: "Self",
    ) -> "_2319.AbstractShaftToMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness
        """
        return (
            _Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtAStiffness(
                self
            )
        )
