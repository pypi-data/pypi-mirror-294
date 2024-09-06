"""ShaftToMountableComponentConnectionCompoundSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _2940,
)

_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "ShaftToMountableComponentConnectionCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2891,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2961,
        _2972,
        _2981,
        _3023,
    )

    Self = TypeVar(
        "Self", bound="ShaftToMountableComponentConnectionCompoundSystemDeflection"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftToMountableComponentConnectionCompoundSystemDeflection._Cast_ShaftToMountableComponentConnectionCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftToMountableComponentConnectionCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftToMountableComponentConnectionCompoundSystemDeflection:
    """Special nested class for casting ShaftToMountableComponentConnectionCompoundSystemDeflection to subclasses."""

    __parent__: "ShaftToMountableComponentConnectionCompoundSystemDeflection"

    @property
    def abstract_shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2940.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection":
        return self.__parent__._cast(
            _2940.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2972.ConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2972,
        )

        return self.__parent__._cast(_2972.ConnectionCompoundSystemDeflection)

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
    def coaxial_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2961.CoaxialConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2961,
        )

        return self.__parent__._cast(_2961.CoaxialConnectionCompoundSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2981.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2981,
        )

        return self.__parent__._cast(
            _2981.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection
        )

    @property
    def planetary_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3023.PlanetaryConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3023,
        )

        return self.__parent__._cast(_3023.PlanetaryConnectionCompoundSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "ShaftToMountableComponentConnectionCompoundSystemDeflection":
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
class ShaftToMountableComponentConnectionCompoundSystemDeflection(
    _2940.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection
):
    """ShaftToMountableComponentConnectionCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION
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
    ) -> "List[_2891.ShaftToMountableComponentConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftToMountableComponentConnectionSystemDeflection]

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
    ) -> "List[_2891.ShaftToMountableComponentConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftToMountableComponentConnectionSystemDeflection]

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
    ) -> "_Cast_ShaftToMountableComponentConnectionCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ShaftToMountableComponentConnectionCompoundSystemDeflection
        """
        return _Cast_ShaftToMountableComponentConnectionCompoundSystemDeflection(self)
