"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.version_comparer._2467 import DesignResults
    from mastapy._private.system_model.fe.version_comparer._2468 import (
        FESubstructureResults,
    )
    from mastapy._private.system_model.fe.version_comparer._2469 import (
        FESubstructureVersionComparer,
    )
    from mastapy._private.system_model.fe.version_comparer._2470 import LoadCaseResults
    from mastapy._private.system_model.fe.version_comparer._2471 import LoadCasesToRun
    from mastapy._private.system_model.fe.version_comparer._2472 import (
        NodeComparisonResult,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.version_comparer._2467": ["DesignResults"],
        "_private.system_model.fe.version_comparer._2468": ["FESubstructureResults"],
        "_private.system_model.fe.version_comparer._2469": [
            "FESubstructureVersionComparer"
        ],
        "_private.system_model.fe.version_comparer._2470": ["LoadCaseResults"],
        "_private.system_model.fe.version_comparer._2471": ["LoadCasesToRun"],
        "_private.system_model.fe.version_comparer._2472": ["NodeComparisonResult"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DesignResults",
    "FESubstructureResults",
    "FESubstructureVersionComparer",
    "LoadCaseResults",
    "LoadCasesToRun",
    "NodeComparisonResult",
)
