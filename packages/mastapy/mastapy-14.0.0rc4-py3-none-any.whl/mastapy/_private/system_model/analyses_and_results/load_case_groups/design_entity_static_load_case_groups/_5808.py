"""PartStaticLoadCaseGroup"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
    _5806,
)

_PART_STATIC_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups",
    "PartStaticLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
        _5803,
        _5804,
        _5807,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7078
    from mastapy._private.system_model.part_model import _2525

    Self = TypeVar("Self", bound="PartStaticLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="PartStaticLoadCaseGroup._Cast_PartStaticLoadCaseGroup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartStaticLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartStaticLoadCaseGroup:
    """Special nested class for casting PartStaticLoadCaseGroup to subclasses."""

    __parent__: "PartStaticLoadCaseGroup"

    @property
    def design_entity_static_load_case_group(
        self: "CastSelf",
    ) -> "_5806.DesignEntityStaticLoadCaseGroup":
        return self.__parent__._cast(_5806.DesignEntityStaticLoadCaseGroup)

    @property
    def abstract_assembly_static_load_case_group(
        self: "CastSelf",
    ) -> "_5803.AbstractAssemblyStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5803,
        )

        return self.__parent__._cast(_5803.AbstractAssemblyStaticLoadCaseGroup)

    @property
    def component_static_load_case_group(
        self: "CastSelf",
    ) -> "_5804.ComponentStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5804,
        )

        return self.__parent__._cast(_5804.ComponentStaticLoadCaseGroup)

    @property
    def gear_set_static_load_case_group(
        self: "CastSelf",
    ) -> "_5807.GearSetStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import (
            _5807,
        )

        return self.__parent__._cast(_5807.GearSetStaticLoadCaseGroup)

    @property
    def part_static_load_case_group(self: "CastSelf") -> "PartStaticLoadCaseGroup":
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
class PartStaticLoadCaseGroup(_5806.DesignEntityStaticLoadCaseGroup):
    """PartStaticLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_STATIC_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def part(self: "Self") -> "_2525.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Part")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def part_load_cases(self: "Self") -> "List[_7078.PartLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.PartLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def clear_user_specified_excitation_data_for_all_load_cases(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ClearUserSpecifiedExcitationDataForAllLoadCases"
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartStaticLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_PartStaticLoadCaseGroup
        """
        return _Cast_PartStaticLoadCaseGroup(self)
