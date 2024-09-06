"""ZerolBevelGearCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4858,
)

_ZEROL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "ZerolBevelGearCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4828
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4846,
        _4867,
        _4874,
        _4900,
        _4921,
        _4923,
    )
    from mastapy._private.system_model.part_model.gears import _2610

    Self = TypeVar("Self", bound="ZerolBevelGearCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGearCompoundModalAnalysis._Cast_ZerolBevelGearCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearCompoundModalAnalysis:
    """Special nested class for casting ZerolBevelGearCompoundModalAnalysis to subclasses."""

    __parent__: "ZerolBevelGearCompoundModalAnalysis"

    @property
    def bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4858.BevelGearCompoundModalAnalysis":
        return self.__parent__._cast(_4858.BevelGearCompoundModalAnalysis)

    @property
    def agma_gleason_conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4846.AGMAGleasonConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4846,
        )

        return self.__parent__._cast(_4846.AGMAGleasonConicalGearCompoundModalAnalysis)

    @property
    def conical_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4874.ConicalGearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4874,
        )

        return self.__parent__._cast(_4874.ConicalGearCompoundModalAnalysis)

    @property
    def gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4900.GearCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4900,
        )

        return self.__parent__._cast(_4900.GearCompoundModalAnalysis)

    @property
    def mountable_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4921.MountableComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4921,
        )

        return self.__parent__._cast(_4921.MountableComponentCompoundModalAnalysis)

    @property
    def component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4867.ComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4867,
        )

        return self.__parent__._cast(_4867.ComponentCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4923.PartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4923,
        )

        return self.__parent__._cast(_4923.PartCompoundModalAnalysis)

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
    def zerol_bevel_gear_compound_modal_analysis(
        self: "CastSelf",
    ) -> "ZerolBevelGearCompoundModalAnalysis":
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
class ZerolBevelGearCompoundModalAnalysis(_4858.BevelGearCompoundModalAnalysis):
    """ZerolBevelGearCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_COMPOUND_MODAL_ANALYSIS

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
    ) -> "List[_4828.ZerolBevelGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearModalAnalysis]

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
    ) -> "List[_4828.ZerolBevelGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ZerolBevelGearModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearCompoundModalAnalysis
        """
        return _Cast_ZerolBevelGearCompoundModalAnalysis(self)
