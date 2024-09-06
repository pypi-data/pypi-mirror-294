"""ConnectorCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6628,
)

_CONNECTOR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "ConnectorCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6452,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6557,
        _6574,
        _6629,
        _6630,
        _6647,
    )

    Self = TypeVar("Self", bound="ConnectorCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectorCompoundDynamicAnalysis._Cast_ConnectorCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorCompoundDynamicAnalysis:
    """Special nested class for casting ConnectorCompoundDynamicAnalysis to subclasses."""

    __parent__: "ConnectorCompoundDynamicAnalysis"

    @property
    def mountable_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6628.MountableComponentCompoundDynamicAnalysis":
        return self.__parent__._cast(_6628.MountableComponentCompoundDynamicAnalysis)

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6574.ComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6574,
        )

        return self.__parent__._cast(_6574.ComponentCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6630.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6630,
        )

        return self.__parent__._cast(_6630.PartCompoundDynamicAnalysis)

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
    def bearing_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6557.BearingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6557,
        )

        return self.__parent__._cast(_6557.BearingCompoundDynamicAnalysis)

    @property
    def oil_seal_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6629.OilSealCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6629,
        )

        return self.__parent__._cast(_6629.OilSealCompoundDynamicAnalysis)

    @property
    def shaft_hub_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6647.ShaftHubConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6647,
        )

        return self.__parent__._cast(_6647.ShaftHubConnectionCompoundDynamicAnalysis)

    @property
    def connector_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "ConnectorCompoundDynamicAnalysis":
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
class ConnectorCompoundDynamicAnalysis(_6628.MountableComponentCompoundDynamicAnalysis):
    """ConnectorCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6452.ConnectorDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectorDynamicAnalysis]

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
    ) -> "List[_6452.ConnectorDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.ConnectorDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ConnectorCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConnectorCompoundDynamicAnalysis
        """
        return _Cast_ConnectorCompoundDynamicAnalysis(self)
