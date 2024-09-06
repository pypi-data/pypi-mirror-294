"""AbstractShaftOrHousingCompoundSystemDeflection"""

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
    _2962,
)

_ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "AbstractShaftOrHousingCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2770,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2938,
        _2982,
        _2994,
        _3019,
        _3035,
    )

    Self = TypeVar("Self", bound="AbstractShaftOrHousingCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftOrHousingCompoundSystemDeflection._Cast_AbstractShaftOrHousingCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftOrHousingCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftOrHousingCompoundSystemDeflection:
    """Special nested class for casting AbstractShaftOrHousingCompoundSystemDeflection to subclasses."""

    __parent__: "AbstractShaftOrHousingCompoundSystemDeflection"

    @property
    def component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2962.ComponentCompoundSystemDeflection":
        return self.__parent__._cast(_2962.ComponentCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3019.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3019,
        )

        return self.__parent__._cast(_3019.PartCompoundSystemDeflection)

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
    def abstract_shaft_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2938.AbstractShaftCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2938,
        )

        return self.__parent__._cast(_2938.AbstractShaftCompoundSystemDeflection)

    @property
    def cycloidal_disc_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2982.CycloidalDiscCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2982,
        )

        return self.__parent__._cast(_2982.CycloidalDiscCompoundSystemDeflection)

    @property
    def fe_part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2994.FEPartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2994,
        )

        return self.__parent__._cast(_2994.FEPartCompoundSystemDeflection)

    @property
    def shaft_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3035.ShaftCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3035,
        )

        return self.__parent__._cast(_3035.ShaftCompoundSystemDeflection)

    @property
    def abstract_shaft_or_housing_compound_system_deflection(
        self: "CastSelf",
    ) -> "AbstractShaftOrHousingCompoundSystemDeflection":
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
class AbstractShaftOrHousingCompoundSystemDeflection(
    _2962.ComponentCompoundSystemDeflection
):
    """AbstractShaftOrHousingCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_OR_HOUSING_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_2770.AbstractShaftOrHousingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AbstractShaftOrHousingSystemDeflection]

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
    ) -> "List[_2770.AbstractShaftOrHousingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AbstractShaftOrHousingSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_AbstractShaftOrHousingCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftOrHousingCompoundSystemDeflection
        """
        return _Cast_AbstractShaftOrHousingCompoundSystemDeflection(self)
