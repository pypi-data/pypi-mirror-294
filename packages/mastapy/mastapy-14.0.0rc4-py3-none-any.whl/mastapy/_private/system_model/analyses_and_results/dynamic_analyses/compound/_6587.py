"""CouplingConnectionCompoundDynamicAnalysis"""

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
    _6614,
)

_COUPLING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "CouplingConnectionCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6453,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6571,
        _6576,
        _6584,
        _6632,
        _6654,
        _6669,
    )

    Self = TypeVar("Self", bound="CouplingConnectionCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCompoundDynamicAnalysis._Cast_CouplingConnectionCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCompoundDynamicAnalysis:
    """Special nested class for casting CouplingConnectionCompoundDynamicAnalysis to subclasses."""

    __parent__: "CouplingConnectionCompoundDynamicAnalysis"

    @property
    def inter_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6614.InterMountableComponentConnectionCompoundDynamicAnalysis":
        return self.__parent__._cast(
            _6614.InterMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6584.ConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6584,
        )

        return self.__parent__._cast(_6584.ConnectionCompoundDynamicAnalysis)

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
    def clutch_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6571.ClutchConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6571,
        )

        return self.__parent__._cast(_6571.ClutchConnectionCompoundDynamicAnalysis)

    @property
    def concept_coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6576.ConceptCouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6576,
        )

        return self.__parent__._cast(
            _6576.ConceptCouplingConnectionCompoundDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6632.PartToPartShearCouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6632,
        )

        return self.__parent__._cast(
            _6632.PartToPartShearCouplingConnectionCompoundDynamicAnalysis
        )

    @property
    def spring_damper_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6654.SpringDamperConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6654,
        )

        return self.__parent__._cast(
            _6654.SpringDamperConnectionCompoundDynamicAnalysis
        )

    @property
    def torque_converter_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6669.TorqueConverterConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6669,
        )

        return self.__parent__._cast(
            _6669.TorqueConverterConnectionCompoundDynamicAnalysis
        )

    @property
    def coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "CouplingConnectionCompoundDynamicAnalysis":
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
class CouplingConnectionCompoundDynamicAnalysis(
    _6614.InterMountableComponentConnectionCompoundDynamicAnalysis
):
    """CouplingConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6453.CouplingConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingConnectionDynamicAnalysis]

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
    ) -> "List[_6453.CouplingConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingConnectionDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCompoundDynamicAnalysis
        """
        return _Cast_CouplingConnectionCompoundDynamicAnalysis(self)
