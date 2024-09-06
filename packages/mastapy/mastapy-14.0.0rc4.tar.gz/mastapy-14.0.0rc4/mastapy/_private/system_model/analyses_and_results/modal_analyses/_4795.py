"""ShaftToMountableComponentConnectionModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4687

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "ShaftToMountableComponentConnectionModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4708,
        _4719,
        _4729,
        _4780,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2891,
    )
    from mastapy._private.system_model.connections_and_sockets import _2349

    Self = TypeVar("Self", bound="ShaftToMountableComponentConnectionModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftToMountableComponentConnectionModalAnalysis._Cast_ShaftToMountableComponentConnectionModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnectionModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftToMountableComponentConnectionModalAnalysis:
    """Special nested class for casting ShaftToMountableComponentConnectionModalAnalysis to subclasses."""

    __parent__: "ShaftToMountableComponentConnectionModalAnalysis"

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4687.AbstractShaftToMountableComponentConnectionModalAnalysis":
        return self.__parent__._cast(
            _4687.AbstractShaftToMountableComponentConnectionModalAnalysis
        )

    @property
    def connection_modal_analysis(self: "CastSelf") -> "_4719.ConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4719,
        )

        return self.__parent__._cast(_4719.ConnectionModalAnalysis)

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
    def coaxial_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4708.CoaxialConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4708,
        )

        return self.__parent__._cast(_4708.CoaxialConnectionModalAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4729.CycloidalDiscCentralBearingConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4729,
        )

        return self.__parent__._cast(
            _4729.CycloidalDiscCentralBearingConnectionModalAnalysis
        )

    @property
    def planetary_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4780.PlanetaryConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4780,
        )

        return self.__parent__._cast(_4780.PlanetaryConnectionModalAnalysis)

    @property
    def shaft_to_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "ShaftToMountableComponentConnectionModalAnalysis":
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
class ShaftToMountableComponentConnectionModalAnalysis(
    _4687.AbstractShaftToMountableComponentConnectionModalAnalysis
):
    """ShaftToMountableComponentConnectionModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2349.ShaftToMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2891.ShaftToMountableComponentConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ShaftToMountableComponentConnectionSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ShaftToMountableComponentConnectionModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ShaftToMountableComponentConnectionModalAnalysis
        """
        return _Cast_ShaftToMountableComponentConnectionModalAnalysis(self)
