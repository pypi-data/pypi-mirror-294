"""CouplingHalfCompoundSystemDeflection"""

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
    _3017,
)

_COUPLING_HALF_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "CouplingHalfCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2814,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2960,
        _2962,
        _2965,
        _2979,
        _3019,
        _3022,
        _3028,
        _3032,
        _3045,
        _3055,
        _3056,
        _3057,
        _3060,
        _3061,
    )

    Self = TypeVar("Self", bound="CouplingHalfCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfCompoundSystemDeflection._Cast_CouplingHalfCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfCompoundSystemDeflection:
    """Special nested class for casting CouplingHalfCompoundSystemDeflection to subclasses."""

    __parent__: "CouplingHalfCompoundSystemDeflection"

    @property
    def mountable_component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3017.MountableComponentCompoundSystemDeflection":
        return self.__parent__._cast(_3017.MountableComponentCompoundSystemDeflection)

    @property
    def component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2962.ComponentCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2962,
        )

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
    def clutch_half_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2960.ClutchHalfCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2960,
        )

        return self.__parent__._cast(_2960.ClutchHalfCompoundSystemDeflection)

    @property
    def concept_coupling_half_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2965.ConceptCouplingHalfCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2965,
        )

        return self.__parent__._cast(_2965.ConceptCouplingHalfCompoundSystemDeflection)

    @property
    def cvt_pulley_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2979.CVTPulleyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2979,
        )

        return self.__parent__._cast(_2979.CVTPulleyCompoundSystemDeflection)

    @property
    def part_to_part_shear_coupling_half_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3022.PartToPartShearCouplingHalfCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3022,
        )

        return self.__parent__._cast(
            _3022.PartToPartShearCouplingHalfCompoundSystemDeflection
        )

    @property
    def pulley_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3028.PulleyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3028,
        )

        return self.__parent__._cast(_3028.PulleyCompoundSystemDeflection)

    @property
    def rolling_ring_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3032.RollingRingCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3032,
        )

        return self.__parent__._cast(_3032.RollingRingCompoundSystemDeflection)

    @property
    def spring_damper_half_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3045.SpringDamperHalfCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3045,
        )

        return self.__parent__._cast(_3045.SpringDamperHalfCompoundSystemDeflection)

    @property
    def synchroniser_half_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3055.SynchroniserHalfCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3055,
        )

        return self.__parent__._cast(_3055.SynchroniserHalfCompoundSystemDeflection)

    @property
    def synchroniser_part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3056.SynchroniserPartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3056,
        )

        return self.__parent__._cast(_3056.SynchroniserPartCompoundSystemDeflection)

    @property
    def synchroniser_sleeve_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3057.SynchroniserSleeveCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3057,
        )

        return self.__parent__._cast(_3057.SynchroniserSleeveCompoundSystemDeflection)

    @property
    def torque_converter_pump_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3060.TorqueConverterPumpCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3060,
        )

        return self.__parent__._cast(_3060.TorqueConverterPumpCompoundSystemDeflection)

    @property
    def torque_converter_turbine_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3061.TorqueConverterTurbineCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3061,
        )

        return self.__parent__._cast(
            _3061.TorqueConverterTurbineCompoundSystemDeflection
        )

    @property
    def coupling_half_compound_system_deflection(
        self: "CastSelf",
    ) -> "CouplingHalfCompoundSystemDeflection":
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
class CouplingHalfCompoundSystemDeflection(
    _3017.MountableComponentCompoundSystemDeflection
):
    """CouplingHalfCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_2814.CouplingHalfSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CouplingHalfSystemDeflection]

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
    ) -> "List[_2814.CouplingHalfSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CouplingHalfSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_CouplingHalfCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfCompoundSystemDeflection
        """
        return _Cast_CouplingHalfCompoundSystemDeflection(self)
