"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.report._1793 import AdHocCustomTable
    from mastapy._private.utility.report._1794 import AxisSettings
    from mastapy._private.utility.report._1795 import BlankRow
    from mastapy._private.utility.report._1796 import CadPageOrientation
    from mastapy._private.utility.report._1797 import CadPageSize
    from mastapy._private.utility.report._1798 import CadTableBorderType
    from mastapy._private.utility.report._1799 import ChartDefinition
    from mastapy._private.utility.report._1800 import SMTChartPointShape
    from mastapy._private.utility.report._1801 import CustomChart
    from mastapy._private.utility.report._1802 import CustomDrawing
    from mastapy._private.utility.report._1803 import CustomGraphic
    from mastapy._private.utility.report._1804 import CustomImage
    from mastapy._private.utility.report._1805 import CustomReport
    from mastapy._private.utility.report._1806 import CustomReportCadDrawing
    from mastapy._private.utility.report._1807 import CustomReportChart
    from mastapy._private.utility.report._1808 import CustomReportChartItem
    from mastapy._private.utility.report._1809 import CustomReportColumn
    from mastapy._private.utility.report._1810 import CustomReportColumns
    from mastapy._private.utility.report._1811 import CustomReportDefinitionItem
    from mastapy._private.utility.report._1812 import CustomReportHorizontalLine
    from mastapy._private.utility.report._1813 import CustomReportHtmlItem
    from mastapy._private.utility.report._1814 import CustomReportItem
    from mastapy._private.utility.report._1815 import CustomReportItemContainer
    from mastapy._private.utility.report._1816 import (
        CustomReportItemContainerCollection,
    )
    from mastapy._private.utility.report._1817 import (
        CustomReportItemContainerCollectionBase,
    )
    from mastapy._private.utility.report._1818 import (
        CustomReportItemContainerCollectionItem,
    )
    from mastapy._private.utility.report._1819 import CustomReportKey
    from mastapy._private.utility.report._1820 import CustomReportMultiPropertyItem
    from mastapy._private.utility.report._1821 import CustomReportMultiPropertyItemBase
    from mastapy._private.utility.report._1822 import CustomReportNameableItem
    from mastapy._private.utility.report._1823 import CustomReportNamedItem
    from mastapy._private.utility.report._1824 import CustomReportPropertyItem
    from mastapy._private.utility.report._1825 import CustomReportStatusItem
    from mastapy._private.utility.report._1826 import CustomReportTab
    from mastapy._private.utility.report._1827 import CustomReportTabs
    from mastapy._private.utility.report._1828 import CustomReportText
    from mastapy._private.utility.report._1829 import CustomRow
    from mastapy._private.utility.report._1830 import CustomSubReport
    from mastapy._private.utility.report._1831 import CustomTable
    from mastapy._private.utility.report._1832 import DefinitionBooleanCheckOptions
    from mastapy._private.utility.report._1833 import DynamicCustomReportItem
    from mastapy._private.utility.report._1834 import FontStyle
    from mastapy._private.utility.report._1835 import FontWeight
    from mastapy._private.utility.report._1836 import HeadingSize
    from mastapy._private.utility.report._1837 import SimpleChartDefinition
    from mastapy._private.utility.report._1838 import UserTextRow
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.report._1793": ["AdHocCustomTable"],
        "_private.utility.report._1794": ["AxisSettings"],
        "_private.utility.report._1795": ["BlankRow"],
        "_private.utility.report._1796": ["CadPageOrientation"],
        "_private.utility.report._1797": ["CadPageSize"],
        "_private.utility.report._1798": ["CadTableBorderType"],
        "_private.utility.report._1799": ["ChartDefinition"],
        "_private.utility.report._1800": ["SMTChartPointShape"],
        "_private.utility.report._1801": ["CustomChart"],
        "_private.utility.report._1802": ["CustomDrawing"],
        "_private.utility.report._1803": ["CustomGraphic"],
        "_private.utility.report._1804": ["CustomImage"],
        "_private.utility.report._1805": ["CustomReport"],
        "_private.utility.report._1806": ["CustomReportCadDrawing"],
        "_private.utility.report._1807": ["CustomReportChart"],
        "_private.utility.report._1808": ["CustomReportChartItem"],
        "_private.utility.report._1809": ["CustomReportColumn"],
        "_private.utility.report._1810": ["CustomReportColumns"],
        "_private.utility.report._1811": ["CustomReportDefinitionItem"],
        "_private.utility.report._1812": ["CustomReportHorizontalLine"],
        "_private.utility.report._1813": ["CustomReportHtmlItem"],
        "_private.utility.report._1814": ["CustomReportItem"],
        "_private.utility.report._1815": ["CustomReportItemContainer"],
        "_private.utility.report._1816": ["CustomReportItemContainerCollection"],
        "_private.utility.report._1817": ["CustomReportItemContainerCollectionBase"],
        "_private.utility.report._1818": ["CustomReportItemContainerCollectionItem"],
        "_private.utility.report._1819": ["CustomReportKey"],
        "_private.utility.report._1820": ["CustomReportMultiPropertyItem"],
        "_private.utility.report._1821": ["CustomReportMultiPropertyItemBase"],
        "_private.utility.report._1822": ["CustomReportNameableItem"],
        "_private.utility.report._1823": ["CustomReportNamedItem"],
        "_private.utility.report._1824": ["CustomReportPropertyItem"],
        "_private.utility.report._1825": ["CustomReportStatusItem"],
        "_private.utility.report._1826": ["CustomReportTab"],
        "_private.utility.report._1827": ["CustomReportTabs"],
        "_private.utility.report._1828": ["CustomReportText"],
        "_private.utility.report._1829": ["CustomRow"],
        "_private.utility.report._1830": ["CustomSubReport"],
        "_private.utility.report._1831": ["CustomTable"],
        "_private.utility.report._1832": ["DefinitionBooleanCheckOptions"],
        "_private.utility.report._1833": ["DynamicCustomReportItem"],
        "_private.utility.report._1834": ["FontStyle"],
        "_private.utility.report._1835": ["FontWeight"],
        "_private.utility.report._1836": ["HeadingSize"],
        "_private.utility.report._1837": ["SimpleChartDefinition"],
        "_private.utility.report._1838": ["UserTextRow"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdHocCustomTable",
    "AxisSettings",
    "BlankRow",
    "CadPageOrientation",
    "CadPageSize",
    "CadTableBorderType",
    "ChartDefinition",
    "SMTChartPointShape",
    "CustomChart",
    "CustomDrawing",
    "CustomGraphic",
    "CustomImage",
    "CustomReport",
    "CustomReportCadDrawing",
    "CustomReportChart",
    "CustomReportChartItem",
    "CustomReportColumn",
    "CustomReportColumns",
    "CustomReportDefinitionItem",
    "CustomReportHorizontalLine",
    "CustomReportHtmlItem",
    "CustomReportItem",
    "CustomReportItemContainer",
    "CustomReportItemContainerCollection",
    "CustomReportItemContainerCollectionBase",
    "CustomReportItemContainerCollectionItem",
    "CustomReportKey",
    "CustomReportMultiPropertyItem",
    "CustomReportMultiPropertyItemBase",
    "CustomReportNameableItem",
    "CustomReportNamedItem",
    "CustomReportPropertyItem",
    "CustomReportStatusItem",
    "CustomReportTab",
    "CustomReportTabs",
    "CustomReportText",
    "CustomRow",
    "CustomSubReport",
    "CustomTable",
    "DefinitionBooleanCheckOptions",
    "DynamicCustomReportItem",
    "FontStyle",
    "FontWeight",
    "HeadingSize",
    "SimpleChartDefinition",
    "UserTextRow",
)
