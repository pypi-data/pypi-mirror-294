"""TorqueConverterTurbineCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4038,
)

_TORQUE_CONVERTER_TURBINE_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "TorqueConverterTurbineCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3990,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4024,
        _4078,
        _4080,
    )
    from mastapy._private.system_model.part_model.couplings import _2673

    Self = TypeVar("Self", bound="TorqueConverterTurbineCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorqueConverterTurbineCompoundStabilityAnalysis._Cast_TorqueConverterTurbineCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterTurbineCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterTurbineCompoundStabilityAnalysis:
    """Special nested class for casting TorqueConverterTurbineCompoundStabilityAnalysis to subclasses."""

    __parent__: "TorqueConverterTurbineCompoundStabilityAnalysis"

    @property
    def coupling_half_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4038.CouplingHalfCompoundStabilityAnalysis":
        return self.__parent__._cast(_4038.CouplingHalfCompoundStabilityAnalysis)

    @property
    def mountable_component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4078.MountableComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4078,
        )

        return self.__parent__._cast(_4078.MountableComponentCompoundStabilityAnalysis)

    @property
    def component_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4024.ComponentCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4024,
        )

        return self.__parent__._cast(_4024.ComponentCompoundStabilityAnalysis)

    @property
    def part_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4080.PartCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4080,
        )

        return self.__parent__._cast(_4080.PartCompoundStabilityAnalysis)

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
    def torque_converter_turbine_compound_stability_analysis(
        self: "CastSelf",
    ) -> "TorqueConverterTurbineCompoundStabilityAnalysis":
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
class TorqueConverterTurbineCompoundStabilityAnalysis(
    _4038.CouplingHalfCompoundStabilityAnalysis
):
    """TorqueConverterTurbineCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_TURBINE_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2673.TorqueConverterTurbine":
        """mastapy.system_model.part_model.couplings.TorqueConverterTurbine

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3990.TorqueConverterTurbineStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.TorqueConverterTurbineStabilityAnalysis]

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
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3990.TorqueConverterTurbineStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.TorqueConverterTurbineStabilityAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_TorqueConverterTurbineCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterTurbineCompoundStabilityAnalysis
        """
        return _Cast_TorqueConverterTurbineCompoundStabilityAnalysis(self)
