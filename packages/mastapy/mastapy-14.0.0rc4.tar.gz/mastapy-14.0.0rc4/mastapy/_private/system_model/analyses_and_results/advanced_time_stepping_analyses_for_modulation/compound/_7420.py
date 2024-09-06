"""ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _7308,
)

_ZEROL_BEVEL_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7289,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7296,
        _7317,
        _7324,
        _7350,
        _7371,
        _7373,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.part_model.gears import _2610

    Self = TypeVar(
        "Self", bound="ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation"

    @property
    def bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7308.BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7308.BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> (
        "_7296.AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7296,
        )

        return self.__parent__._cast(
            _7296.AGMAGleasonConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7324.ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7324,
        )

        return self.__parent__._cast(
            _7324.ConicalGearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7350.GearCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7350,
        )

        return self.__parent__._cast(
            _7350.GearCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mountable_component_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7371.MountableComponentCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7371,
        )

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
    def zerol_bevel_gear_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
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
class ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation(
    _7308.BevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
):
    """ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ZEROL_BEVEL_GEAR_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2610.ZerolBevelGear":
        """mastapy.system_model.part_model.gears.ZerolBevelGear

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
    ) -> "List[_7289.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "List[_7289.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "_Cast_ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_ZerolBevelGearCompoundAdvancedTimeSteppingAnalysisForModulation(
            self
        )
