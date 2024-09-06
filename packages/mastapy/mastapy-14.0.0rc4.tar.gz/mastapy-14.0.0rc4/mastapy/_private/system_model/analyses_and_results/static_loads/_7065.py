"""KlingelnbergCycloPalloidHypoidGearSetLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7062

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "KlingelnbergCycloPalloidHypoidGearSetLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6954,
        _6996,
        _7043,
        _7063,
        _7064,
        _7078,
        _7102,
    )
    from mastapy._private.system_model.part_model.gears import _2596

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearSetLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearSetLoadCase._Cast_KlingelnbergCycloPalloidHypoidGearSetLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearSetLoadCase:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSetLoadCase to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearSetLoadCase"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7062.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        return self.__parent__._cast(
            _7062.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_6996.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6996,
        )

        return self.__parent__._cast(_6996.ConicalGearSetLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7043.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7043,
        )

        return self.__parent__._cast(_7043.GearSetLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7102.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7102,
        )

        return self.__parent__._cast(_7102.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6954.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6954,
        )

        return self.__parent__._cast(_6954.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7078.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7078,
        )

        return self.__parent__._cast(_7078.PartLoadCase)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearSetLoadCase":
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
class KlingelnbergCycloPalloidHypoidGearSetLoadCase(
    _7062.KlingelnbergCycloPalloidConicalGearSetLoadCase
):
    """KlingelnbergCycloPalloidHypoidGearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2596.KlingelnbergCycloPalloidHypoidGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def klingelnberg_cyclo_palloid_conical_gears_load_case(
        self: "Self",
    ) -> "List[_7063.KlingelnbergCycloPalloidHypoidGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalGearsLoadCase"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_load_case(
        self: "Self",
    ) -> "List[_7063.KlingelnbergCycloPalloidHypoidGearLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearsLoadCase"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_conical_meshes_load_case(
        self: "Self",
    ) -> "List[_7064.KlingelnbergCycloPalloidHypoidGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalMeshesLoadCase"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_load_case(
        self: "Self",
    ) -> "List[_7064.KlingelnbergCycloPalloidHypoidGearMeshLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidMeshesLoadCase"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearSetLoadCase
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearSetLoadCase(self)
