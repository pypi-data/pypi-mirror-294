"""VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _7371,
)

_VIRTUAL_COMPONENT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7285,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7317,
        _7367,
        _7368,
        _7373,
        _7380,
        _7381,
        _7415,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )

    Self = TypeVar(
        "Self",
        bound="VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation"

    @property
    def mountable_component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7371.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7371.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7317.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7317,
        )

        return self.__parent__._cast(
            _7317.ComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7373.PartCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7373,
        )

        return self.__parent__._cast(
            _7373.PartCompoundAdvancedTimeSteppingAnalysisForModulation
        )

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
    def mass_disc_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7367.MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7367,
        )

        return self.__parent__._cast(
            _7367.MassDiscCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def measurement_component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7368.MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7368,
        )

        return self.__parent__._cast(
            _7368.MeasurementComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def point_load_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7380.PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7380,
        )

        return self.__parent__._cast(
            _7380.PointLoadCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def power_load_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7381.PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7381,
        )

        return self.__parent__._cast(
            _7381.PowerLoadCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def unbalanced_mass_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7415.UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7415,
        )

        return self.__parent__._cast(
            _7415.UnbalancedMassCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def virtual_component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
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
class VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation(
    _7371.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation
):
    """VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _VIRTUAL_COMPONENT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_7285.VirtualComponentAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.VirtualComponentAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "List[_7285.VirtualComponentAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.VirtualComponentAdvancedTimeSteppingAnalysisForModulation]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_VirtualComponentCompoundAdvancedTimeSteppingAnalysisForModulation(
            self
        )
