"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility_gui.charts._1905 import BubbleChartDefinition
    from mastapy._private.utility_gui.charts._1906 import ConstantLine
    from mastapy._private.utility_gui.charts._1907 import CustomLineChart
    from mastapy._private.utility_gui.charts._1908 import CustomTableAndChart
    from mastapy._private.utility_gui.charts._1909 import LegacyChartMathChartDefinition
    from mastapy._private.utility_gui.charts._1910 import MatrixVisualisationDefinition
    from mastapy._private.utility_gui.charts._1911 import ModeConstantLine
    from mastapy._private.utility_gui.charts._1912 import NDChartDefinition
    from mastapy._private.utility_gui.charts._1913 import (
        ParallelCoordinatesChartDefinition,
    )
    from mastapy._private.utility_gui.charts._1914 import PointsForSurface
    from mastapy._private.utility_gui.charts._1915 import ScatterChartDefinition
    from mastapy._private.utility_gui.charts._1916 import Series2D
    from mastapy._private.utility_gui.charts._1917 import SMTAxis
    from mastapy._private.utility_gui.charts._1918 import ThreeDChartDefinition
    from mastapy._private.utility_gui.charts._1919 import ThreeDVectorChartDefinition
    from mastapy._private.utility_gui.charts._1920 import TwoDChartDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility_gui.charts._1905": ["BubbleChartDefinition"],
        "_private.utility_gui.charts._1906": ["ConstantLine"],
        "_private.utility_gui.charts._1907": ["CustomLineChart"],
        "_private.utility_gui.charts._1908": ["CustomTableAndChart"],
        "_private.utility_gui.charts._1909": ["LegacyChartMathChartDefinition"],
        "_private.utility_gui.charts._1910": ["MatrixVisualisationDefinition"],
        "_private.utility_gui.charts._1911": ["ModeConstantLine"],
        "_private.utility_gui.charts._1912": ["NDChartDefinition"],
        "_private.utility_gui.charts._1913": ["ParallelCoordinatesChartDefinition"],
        "_private.utility_gui.charts._1914": ["PointsForSurface"],
        "_private.utility_gui.charts._1915": ["ScatterChartDefinition"],
        "_private.utility_gui.charts._1916": ["Series2D"],
        "_private.utility_gui.charts._1917": ["SMTAxis"],
        "_private.utility_gui.charts._1918": ["ThreeDChartDefinition"],
        "_private.utility_gui.charts._1919": ["ThreeDVectorChartDefinition"],
        "_private.utility_gui.charts._1920": ["TwoDChartDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BubbleChartDefinition",
    "ConstantLine",
    "CustomLineChart",
    "CustomTableAndChart",
    "LegacyChartMathChartDefinition",
    "MatrixVisualisationDefinition",
    "ModeConstantLine",
    "NDChartDefinition",
    "ParallelCoordinatesChartDefinition",
    "PointsForSurface",
    "ScatterChartDefinition",
    "Series2D",
    "SMTAxis",
    "ThreeDChartDefinition",
    "ThreeDVectorChartDefinition",
    "TwoDChartDefinition",
)
