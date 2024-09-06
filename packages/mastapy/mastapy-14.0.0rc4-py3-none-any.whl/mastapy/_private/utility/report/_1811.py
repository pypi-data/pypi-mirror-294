"""CustomReportDefinitionItem"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1822

_CUSTOM_REPORT_DEFINITION_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportDefinitionItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2001
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4496,
    )
    from mastapy._private.utility.report import (
        _1793,
        _1801,
        _1802,
        _1803,
        _1804,
        _1813,
        _1814,
        _1825,
        _1828,
        _1830,
    )

    Self = TypeVar("Self", bound="CustomReportDefinitionItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportDefinitionItem._Cast_CustomReportDefinitionItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportDefinitionItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportDefinitionItem:
    """Special nested class for casting CustomReportDefinitionItem to subclasses."""

    __parent__: "CustomReportDefinitionItem"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1822.CustomReportNameableItem":
        return self.__parent__._cast(_1822.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1814.CustomReportItem":
        from mastapy._private.utility.report import _1814

        return self.__parent__._cast(_1814.CustomReportItem)

    @property
    def ad_hoc_custom_table(self: "CastSelf") -> "_1793.AdHocCustomTable":
        from mastapy._private.utility.report import _1793

        return self.__parent__._cast(_1793.AdHocCustomTable)

    @property
    def custom_chart(self: "CastSelf") -> "_1801.CustomChart":
        from mastapy._private.utility.report import _1801

        return self.__parent__._cast(_1801.CustomChart)

    @property
    def custom_drawing(self: "CastSelf") -> "_1802.CustomDrawing":
        from mastapy._private.utility.report import _1802

        return self.__parent__._cast(_1802.CustomDrawing)

    @property
    def custom_graphic(self: "CastSelf") -> "_1803.CustomGraphic":
        from mastapy._private.utility.report import _1803

        return self.__parent__._cast(_1803.CustomGraphic)

    @property
    def custom_image(self: "CastSelf") -> "_1804.CustomImage":
        from mastapy._private.utility.report import _1804

        return self.__parent__._cast(_1804.CustomImage)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1813.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1813

        return self.__parent__._cast(_1813.CustomReportHtmlItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_1825.CustomReportStatusItem":
        from mastapy._private.utility.report import _1825

        return self.__parent__._cast(_1825.CustomReportStatusItem)

    @property
    def custom_report_text(self: "CastSelf") -> "_1828.CustomReportText":
        from mastapy._private.utility.report import _1828

        return self.__parent__._cast(_1828.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_1830.CustomSubReport":
        from mastapy._private.utility.report import _1830

        return self.__parent__._cast(_1830.CustomSubReport)

    @property
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2001.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2001

        return self.__parent__._cast(_2001.LoadedBearingChartReporter)

    @property
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4496.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4496,
        )

        return self.__parent__._cast(_4496.ParametricStudyHistogram)

    @property
    def custom_report_definition_item(self: "CastSelf") -> "CustomReportDefinitionItem":
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
class CustomReportDefinitionItem(_1822.CustomReportNameableItem):
    """CustomReportDefinitionItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_DEFINITION_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportDefinitionItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportDefinitionItem
        """
        return _Cast_CustomReportDefinitionItem(self)
