"""ShaftToMountableComponentConnectionCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6015,
)

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ShaftToMountableComponentConnectionCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5941,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6036,
        _6047,
        _6056,
        _6097,
    )

    Self = TypeVar(
        "Self", bound="ShaftToMountableComponentConnectionCompoundHarmonicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftToMountableComponentConnectionCompoundHarmonicAnalysis._Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnectionCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis:
    """Special nested class for casting ShaftToMountableComponentConnectionCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ShaftToMountableComponentConnectionCompoundHarmonicAnalysis"

    @property
    def abstract_shaft_to_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6015.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
        return self.__parent__._cast(
            _6015.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6047.ConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6047,
        )

        return self.__parent__._cast(_6047.ConnectionCompoundHarmonicAnalysis)

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
    def coaxial_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6036.CoaxialConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6036,
        )

        return self.__parent__._cast(_6036.CoaxialConnectionCompoundHarmonicAnalysis)

    @property
    def cycloidal_disc_central_bearing_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6056.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6056,
        )

        return self.__parent__._cast(
            _6056.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis
        )

    @property
    def planetary_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6097.PlanetaryConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6097,
        )

        return self.__parent__._cast(_6097.PlanetaryConnectionCompoundHarmonicAnalysis)

    @property
    def shaft_to_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
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
class ShaftToMountableComponentConnectionCompoundHarmonicAnalysis(
    _6015.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis
):
    """ShaftToMountableComponentConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_HARMONIC_ANALYSIS
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
    ) -> "List[_5941.ShaftToMountableComponentConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ShaftToMountableComponentConnectionHarmonicAnalysis]

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
    ) -> "List[_5941.ShaftToMountableComponentConnectionHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ShaftToMountableComponentConnectionHarmonicAnalysis]

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
    ) -> "_Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis
        """
        return _Cast_ShaftToMountableComponentConnectionCompoundHarmonicAnalysis(self)
