"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.convergence._1623 import ConvergenceLogger
    from mastapy._private.math_utility.convergence._1624 import DataLogger
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.convergence._1623": ["ConvergenceLogger"],
        "_private.math_utility.convergence._1624": ["DataLogger"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConvergenceLogger",
    "DataLogger",
)
