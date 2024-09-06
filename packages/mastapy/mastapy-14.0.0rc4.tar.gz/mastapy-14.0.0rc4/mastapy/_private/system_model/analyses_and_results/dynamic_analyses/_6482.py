"""HypoidGearSetDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6422

_HYPOID_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "HypoidGearSetDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7716,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6416,
        _6450,
        _6478,
        _6480,
        _6481,
        _6499,
        _6518,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7055
    from mastapy._private.system_model.part_model.gears import _2592

    Self = TypeVar("Self", bound="HypoidGearSetDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HypoidGearSetDynamicAnalysis._Cast_HypoidGearSetDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearSetDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearSetDynamicAnalysis:
    """Special nested class for casting HypoidGearSetDynamicAnalysis to subclasses."""

    __parent__: "HypoidGearSetDynamicAnalysis"

    @property
    def agma_gleason_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6422.AGMAGleasonConicalGearSetDynamicAnalysis":
        return self.__parent__._cast(_6422.AGMAGleasonConicalGearSetDynamicAnalysis)

    @property
    def conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6450.ConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6450,
        )

        return self.__parent__._cast(_6450.ConicalGearSetDynamicAnalysis)

    @property
    def gear_set_dynamic_analysis(self: "CastSelf") -> "_6478.GearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6478,
        )

        return self.__parent__._cast(_6478.GearSetDynamicAnalysis)

    @property
    def specialised_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6518.SpecialisedAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6518,
        )

        return self.__parent__._cast(_6518.SpecialisedAssemblyDynamicAnalysis)

    @property
    def abstract_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6416.AbstractAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6416,
        )

        return self.__parent__._cast(_6416.AbstractAssemblyDynamicAnalysis)

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6499.PartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6499,
        )

        return self.__parent__._cast(_6499.PartDynamicAnalysis)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7716.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7716,
        )

        return self.__parent__._cast(_7716.PartFEAnalysis)

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
    def hypoid_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "HypoidGearSetDynamicAnalysis":
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
class HypoidGearSetDynamicAnalysis(_6422.AGMAGleasonConicalGearSetDynamicAnalysis):
    """HypoidGearSetDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_GEAR_SET_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2592.HypoidGearSet":
        """mastapy.system_model.part_model.gears.HypoidGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_7055.HypoidGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def agma_gleason_conical_gears_dynamic_analysis(
        self: "Self",
    ) -> "List[_6480.HypoidGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalGearsDynamicAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def hypoid_gears_dynamic_analysis(
        self: "Self",
    ) -> "List[_6480.HypoidGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearsDynamicAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def agma_gleason_conical_meshes_dynamic_analysis(
        self: "Self",
    ) -> "List[_6481.HypoidGearMeshDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearMeshDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalMeshesDynamicAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def hypoid_meshes_dynamic_analysis(
        self: "Self",
    ) -> "List[_6481.HypoidGearMeshDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.HypoidGearMeshDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidMeshesDynamicAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidGearSetDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearSetDynamicAnalysis
        """
        return _Cast_HypoidGearSetDynamicAnalysis(self)
