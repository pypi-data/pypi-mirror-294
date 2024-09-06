"""PlanetaryGearSetModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4734

_PLANETARY_GEAR_SET_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "PlanetaryGearSetModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4684,
        _4749,
        _4776,
        _4796,
    )
    from mastapy._private.system_model.part_model.gears import _2599

    Self = TypeVar("Self", bound="PlanetaryGearSetModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlanetaryGearSetModalAnalysis._Cast_PlanetaryGearSetModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryGearSetModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryGearSetModalAnalysis:
    """Special nested class for casting PlanetaryGearSetModalAnalysis to subclasses."""

    __parent__: "PlanetaryGearSetModalAnalysis"

    @property
    def cylindrical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4734.CylindricalGearSetModalAnalysis":
        return self.__parent__._cast(_4734.CylindricalGearSetModalAnalysis)

    @property
    def gear_set_modal_analysis(self: "CastSelf") -> "_4749.GearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4749,
        )

        return self.__parent__._cast(_4749.GearSetModalAnalysis)

    @property
    def specialised_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4796.SpecialisedAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4796,
        )

        return self.__parent__._cast(_4796.SpecialisedAssemblyModalAnalysis)

    @property
    def abstract_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4684.AbstractAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4684,
        )

        return self.__parent__._cast(_4684.AbstractAssemblyModalAnalysis)

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4776.PartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4776,
        )

        return self.__parent__._cast(_4776.PartModalAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7714.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2741.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2741

        return self.__parent__._cast(_2741.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2737.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2737

        return self.__parent__._cast(_2737.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2735.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.DesignEntityAnalysis)

    @property
    def planetary_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "PlanetaryGearSetModalAnalysis":
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
class PlanetaryGearSetModalAnalysis(_4734.CylindricalGearSetModalAnalysis):
    """PlanetaryGearSetModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_GEAR_SET_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2599.PlanetaryGearSet":
        """mastapy.system_model.part_model.gears.PlanetaryGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetaryGearSetModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryGearSetModalAnalysis
        """
        return _Cast_PlanetaryGearSetModalAnalysis(self)
