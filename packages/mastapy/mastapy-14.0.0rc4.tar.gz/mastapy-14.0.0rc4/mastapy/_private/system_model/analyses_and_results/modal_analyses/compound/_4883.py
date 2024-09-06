"""CVTCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4852,
)

_CVT_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "CVTCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4726
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4842,
        _4923,
        _4942,
    )

    Self = TypeVar("Self", bound="CVTCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="CVTCompoundModalAnalysis._Cast_CVTCompoundModalAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTCompoundModalAnalysis:
    """Special nested class for casting CVTCompoundModalAnalysis to subclasses."""

    __parent__: "CVTCompoundModalAnalysis"

    @property
    def belt_drive_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4852.BeltDriveCompoundModalAnalysis":
        return self.__parent__._cast(_4852.BeltDriveCompoundModalAnalysis)

    @property
    def specialised_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4942.SpecialisedAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4942,
        )

        return self.__parent__._cast(_4942.SpecialisedAssemblyCompoundModalAnalysis)

    @property
    def abstract_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4842.AbstractAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4842,
        )

        return self.__parent__._cast(_4842.AbstractAssemblyCompoundModalAnalysis)

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
    def cvt_compound_modal_analysis(self: "CastSelf") -> "CVTCompoundModalAnalysis":
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
class CVTCompoundModalAnalysis(_4852.BeltDriveCompoundModalAnalysis):
    """CVTCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases_ready(self: "Self") -> "List[_4726.CVTModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.CVTModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_4726.CVTModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.CVTModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CVTCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CVTCompoundModalAnalysis
        """
        return _Cast_CVTCompoundModalAnalysis(self)
