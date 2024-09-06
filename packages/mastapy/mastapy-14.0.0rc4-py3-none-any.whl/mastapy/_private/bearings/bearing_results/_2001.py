"""LoadedBearingChartReporter"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1804

_LOADED_BEARING_CHART_REPORTER = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedBearingChartReporter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1803, _1811, _1814, _1822

    Self = TypeVar("Self", bound="LoadedBearingChartReporter")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedBearingChartReporter._Cast_LoadedBearingChartReporter"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBearingChartReporter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBearingChartReporter:
    """Special nested class for casting LoadedBearingChartReporter to subclasses."""

    __parent__: "LoadedBearingChartReporter"

    @property
    def custom_image(self: "CastSelf") -> "_1804.CustomImage":
        return self.__parent__._cast(_1804.CustomImage)

    @property
    def custom_graphic(self: "CastSelf") -> "_1803.CustomGraphic":
        from mastapy._private.utility.report import _1803

        return self.__parent__._cast(_1803.CustomGraphic)

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1811.CustomReportDefinitionItem":
        from mastapy._private.utility.report import _1811

        return self.__parent__._cast(_1811.CustomReportDefinitionItem)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1822.CustomReportNameableItem":
        from mastapy._private.utility.report import _1822

        return self.__parent__._cast(_1822.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1814.CustomReportItem":
        from mastapy._private.utility.report import _1814

        return self.__parent__._cast(_1814.CustomReportItem)

    @property
    def loaded_bearing_chart_reporter(self: "CastSelf") -> "LoadedBearingChartReporter":
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
class LoadedBearingChartReporter(_1804.CustomImage):
    """LoadedBearingChartReporter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BEARING_CHART_REPORTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def property_(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "Property")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @property_.setter
    @enforce_parameter_types
    def property_(self: "Self", value: "str") -> None:
        wrapper_type = list_with_selected_item.ListWithSelectedItem_str.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else ""
        )
        pythonnet_property_set(self.wrapped, "Property", value)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedBearingChartReporter":
        """Cast to another type.

        Returns:
            _Cast_LoadedBearingChartReporter
        """
        return _Cast_LoadedBearingChartReporter(self)
