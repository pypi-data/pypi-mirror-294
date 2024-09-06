"""CustomReportItem"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CUSTOM_REPORT_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2000, _2001, _2004, _2012
    from mastapy._private.gears.gear_designs.cylindrical import _1067
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4831,
        _4835,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4496,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _2935,
    )
    from mastapy._private.utility.report import (
        _1793,
        _1801,
        _1802,
        _1803,
        _1804,
        _1805,
        _1806,
        _1807,
        _1809,
        _1810,
        _1811,
        _1812,
        _1813,
        _1815,
        _1816,
        _1817,
        _1818,
        _1820,
        _1821,
        _1822,
        _1823,
        _1825,
        _1826,
        _1827,
        _1828,
        _1830,
        _1831,
        _1833,
    )
    from mastapy._private.utility_gui.charts import _1907, _1908

    Self = TypeVar("Self", bound="CustomReportItem")
    CastSelf = TypeVar("CastSelf", bound="CustomReportItem._Cast_CustomReportItem")


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportItem:
    """Special nested class for casting CustomReportItem to subclasses."""

    __parent__: "CustomReportItem"

    @property
    def shaft_damage_results_table_and_chart(
        self: "CastSelf",
    ) -> "_20.ShaftDamageResultsTableAndChart":
        from mastapy._private.shafts import _20

        return self.__parent__._cast(_20.ShaftDamageResultsTableAndChart)

    @property
    def cylindrical_gear_table_with_mg_charts(
        self: "CastSelf",
    ) -> "_1067.CylindricalGearTableWithMGCharts":
        from mastapy._private.gears.gear_designs.cylindrical import _1067

        return self.__parent__._cast(_1067.CylindricalGearTableWithMGCharts)

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
    def custom_report(self: "CastSelf") -> "_1805.CustomReport":
        from mastapy._private.utility.report import _1805

        return self.__parent__._cast(_1805.CustomReport)

    @property
    def custom_report_cad_drawing(self: "CastSelf") -> "_1806.CustomReportCadDrawing":
        from mastapy._private.utility.report import _1806

        return self.__parent__._cast(_1806.CustomReportCadDrawing)

    @property
    def custom_report_chart(self: "CastSelf") -> "_1807.CustomReportChart":
        from mastapy._private.utility.report import _1807

        return self.__parent__._cast(_1807.CustomReportChart)

    @property
    def custom_report_column(self: "CastSelf") -> "_1809.CustomReportColumn":
        from mastapy._private.utility.report import _1809

        return self.__parent__._cast(_1809.CustomReportColumn)

    @property
    def custom_report_columns(self: "CastSelf") -> "_1810.CustomReportColumns":
        from mastapy._private.utility.report import _1810

        return self.__parent__._cast(_1810.CustomReportColumns)

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1811.CustomReportDefinitionItem":
        from mastapy._private.utility.report import _1811

        return self.__parent__._cast(_1811.CustomReportDefinitionItem)

    @property
    def custom_report_horizontal_line(
        self: "CastSelf",
    ) -> "_1812.CustomReportHorizontalLine":
        from mastapy._private.utility.report import _1812

        return self.__parent__._cast(_1812.CustomReportHorizontalLine)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1813.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1813

        return self.__parent__._cast(_1813.CustomReportHtmlItem)

    @property
    def custom_report_item_container(
        self: "CastSelf",
    ) -> "_1815.CustomReportItemContainer":
        from mastapy._private.utility.report import _1815

        return self.__parent__._cast(_1815.CustomReportItemContainer)

    @property
    def custom_report_item_container_collection(
        self: "CastSelf",
    ) -> "_1816.CustomReportItemContainerCollection":
        from mastapy._private.utility.report import _1816

        return self.__parent__._cast(_1816.CustomReportItemContainerCollection)

    @property
    def custom_report_item_container_collection_base(
        self: "CastSelf",
    ) -> "_1817.CustomReportItemContainerCollectionBase":
        from mastapy._private.utility.report import _1817

        return self.__parent__._cast(_1817.CustomReportItemContainerCollectionBase)

    @property
    def custom_report_item_container_collection_item(
        self: "CastSelf",
    ) -> "_1818.CustomReportItemContainerCollectionItem":
        from mastapy._private.utility.report import _1818

        return self.__parent__._cast(_1818.CustomReportItemContainerCollectionItem)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1820.CustomReportMultiPropertyItem":
        from mastapy._private.utility.report import _1820

        return self.__parent__._cast(_1820.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1821.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1821

        return self.__parent__._cast(_1821.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1822.CustomReportNameableItem":
        from mastapy._private.utility.report import _1822

        return self.__parent__._cast(_1822.CustomReportNameableItem)

    @property
    def custom_report_named_item(self: "CastSelf") -> "_1823.CustomReportNamedItem":
        from mastapy._private.utility.report import _1823

        return self.__parent__._cast(_1823.CustomReportNamedItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_1825.CustomReportStatusItem":
        from mastapy._private.utility.report import _1825

        return self.__parent__._cast(_1825.CustomReportStatusItem)

    @property
    def custom_report_tab(self: "CastSelf") -> "_1826.CustomReportTab":
        from mastapy._private.utility.report import _1826

        return self.__parent__._cast(_1826.CustomReportTab)

    @property
    def custom_report_tabs(self: "CastSelf") -> "_1827.CustomReportTabs":
        from mastapy._private.utility.report import _1827

        return self.__parent__._cast(_1827.CustomReportTabs)

    @property
    def custom_report_text(self: "CastSelf") -> "_1828.CustomReportText":
        from mastapy._private.utility.report import _1828

        return self.__parent__._cast(_1828.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_1830.CustomSubReport":
        from mastapy._private.utility.report import _1830

        return self.__parent__._cast(_1830.CustomSubReport)

    @property
    def custom_table(self: "CastSelf") -> "_1831.CustomTable":
        from mastapy._private.utility.report import _1831

        return self.__parent__._cast(_1831.CustomTable)

    @property
    def dynamic_custom_report_item(self: "CastSelf") -> "_1833.DynamicCustomReportItem":
        from mastapy._private.utility.report import _1833

        return self.__parent__._cast(_1833.DynamicCustomReportItem)

    @property
    def custom_line_chart(self: "CastSelf") -> "_1907.CustomLineChart":
        from mastapy._private.utility_gui.charts import _1907

        return self.__parent__._cast(_1907.CustomLineChart)

    @property
    def custom_table_and_chart(self: "CastSelf") -> "_1908.CustomTableAndChart":
        from mastapy._private.utility_gui.charts import _1908

        return self.__parent__._cast(_1908.CustomTableAndChart)

    @property
    def loaded_ball_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2000.LoadedBallElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2000

        return self.__parent__._cast(_2000.LoadedBallElementChartReporter)

    @property
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2001.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2001

        return self.__parent__._cast(_2001.LoadedBearingChartReporter)

    @property
    def loaded_bearing_temperature_chart(
        self: "CastSelf",
    ) -> "_2004.LoadedBearingTemperatureChart":
        from mastapy._private.bearings.bearing_results import _2004

        return self.__parent__._cast(_2004.LoadedBearingTemperatureChart)

    @property
    def loaded_roller_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2012.LoadedRollerElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2012

        return self.__parent__._cast(_2012.LoadedRollerElementChartReporter)

    @property
    def shaft_system_deflection_sections_report(
        self: "CastSelf",
    ) -> "_2935.ShaftSystemDeflectionSectionsReport":
        from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
            _2935,
        )

        return self.__parent__._cast(_2935.ShaftSystemDeflectionSectionsReport)

    @property
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4496.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4496,
        )

        return self.__parent__._cast(_4496.ParametricStudyHistogram)

    @property
    def campbell_diagram_report(self: "CastSelf") -> "_4831.CampbellDiagramReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4831,
        )

        return self.__parent__._cast(_4831.CampbellDiagramReport)

    @property
    def per_mode_results_report(self: "CastSelf") -> "_4835.PerModeResultsReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4835,
        )

        return self.__parent__._cast(_4835.PerModeResultsReport)

    @property
    def custom_report_item(self: "CastSelf") -> "CustomReportItem":
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
class CustomReportItem(_0.APIBase):
    """CustomReportItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def is_main_report_item(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsMainReportItem")

        if temp is None:
            return False

        return temp

    @is_main_report_item.setter
    @enforce_parameter_types
    def is_main_report_item(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsMainReportItem",
            bool(value) if value is not None else False,
        )

    @property
    def item_type(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ItemType")

        if temp is None:
            return ""

        return temp

    def add_condition(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddCondition")

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportItem
        """
        return _Cast_CustomReportItem(self)
