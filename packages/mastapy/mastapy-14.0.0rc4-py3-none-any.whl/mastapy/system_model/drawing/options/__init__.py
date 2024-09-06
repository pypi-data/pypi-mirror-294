"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.drawing.options._2315 import (
        AdvancedTimeSteppingAnalysisForModulationModeViewOptions,
    )
    from mastapy._private.system_model.drawing.options._2316 import (
        ExcitationAnalysisViewOption,
    )
    from mastapy._private.system_model.drawing.options._2317 import (
        ModalContributionViewOptions,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.drawing.options._2315": [
            "AdvancedTimeSteppingAnalysisForModulationModeViewOptions"
        ],
        "_private.system_model.drawing.options._2316": ["ExcitationAnalysisViewOption"],
        "_private.system_model.drawing.options._2317": ["ModalContributionViewOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AdvancedTimeSteppingAnalysisForModulationModeViewOptions",
    "ExcitationAnalysisViewOption",
    "ModalContributionViewOptions",
)
