"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.enums._1872 import BearingForceArrowOption
    from mastapy._private.utility.enums._1873 import TableAndChartOptions
    from mastapy._private.utility.enums._1874 import ThreeDViewContourOption
    from mastapy._private.utility.enums._1875 import (
        ThreeDViewContourOptionFirstSelection,
    )
    from mastapy._private.utility.enums._1876 import (
        ThreeDViewContourOptionSecondSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.enums._1872": ["BearingForceArrowOption"],
        "_private.utility.enums._1873": ["TableAndChartOptions"],
        "_private.utility.enums._1874": ["ThreeDViewContourOption"],
        "_private.utility.enums._1875": ["ThreeDViewContourOptionFirstSelection"],
        "_private.utility.enums._1876": ["ThreeDViewContourOptionSecondSelection"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingForceArrowOption",
    "TableAndChartOptions",
    "ThreeDViewContourOption",
    "ThreeDViewContourOptionFirstSelection",
    "ThreeDViewContourOptionSecondSelection",
)
