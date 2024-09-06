"""AbstractShaftToMountableComponentConnectionHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5846

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "AbstractShaftToMountableComponentConnectionHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5834,
        _5855,
        _5857,
        _5926,
        _5941,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2772,
    )
    from mastapy._private.system_model.connections_and_sockets import _2319

    Self = TypeVar(
        "Self", bound="AbstractShaftToMountableComponentConnectionHarmonicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionHarmonicAnalysis._Cast_AbstractShaftToMountableComponentConnectionHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionHarmonicAnalysis:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionHarmonicAnalysis to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionHarmonicAnalysis"

    @property
    def connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5846.ConnectionHarmonicAnalysis":
        return self.__parent__._cast(_5846.ConnectionHarmonicAnalysis)

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
    def coaxial_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5834.CoaxialConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5834,
        )

        return self.__parent__._cast(_5834.CoaxialConnectionHarmonicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5855.CycloidalDiscCentralBearingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5855,
        )

        return self.__parent__._cast(
            _5855.CycloidalDiscCentralBearingConnectionHarmonicAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5857.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5857,
        )

        return self.__parent__._cast(
            _5857.CycloidalDiscPlanetaryBearingConnectionHarmonicAnalysis
        )

    @property
    def planetary_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5926.PlanetaryConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5926,
        )

        return self.__parent__._cast(_5926.PlanetaryConnectionHarmonicAnalysis)

    @property
    def shaft_to_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5941.ShaftToMountableComponentConnectionHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5941,
        )

        return self.__parent__._cast(
            _5941.ShaftToMountableComponentConnectionHarmonicAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_harmonic_analysis(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionHarmonicAnalysis":
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
class AbstractShaftToMountableComponentConnectionHarmonicAnalysis(
    _5846.ConnectionHarmonicAnalysis
):
    """AbstractShaftToMountableComponentConnectionHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_HARMONIC_ANALYSIS
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
    def system_deflection_results(
        self: "Self",
    ) -> "_2772.AbstractShaftToMountableComponentConnectionSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.AbstractShaftToMountableComponentConnectionSystemDeflection

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
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionHarmonicAnalysis
        """
        return _Cast_AbstractShaftToMountableComponentConnectionHarmonicAnalysis(self)
