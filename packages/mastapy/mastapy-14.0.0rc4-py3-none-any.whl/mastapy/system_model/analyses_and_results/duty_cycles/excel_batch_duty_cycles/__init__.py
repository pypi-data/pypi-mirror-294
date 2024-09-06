"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6680 import (
        ExcelBatchDutyCycleCreator,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6681 import (
        ExcelBatchDutyCycleSpectraCreatorDetails,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6682 import (
        ExcelFileDetails,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6683 import (
        ExcelSheet,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6684 import (
        ExcelSheetDesignStateSelector,
    )
    from mastapy._private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6685 import (
        MASTAFileDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6680": [
            "ExcelBatchDutyCycleCreator"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6681": [
            "ExcelBatchDutyCycleSpectraCreatorDetails"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6682": [
            "ExcelFileDetails"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6683": [
            "ExcelSheet"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6684": [
            "ExcelSheetDesignStateSelector"
        ],
        "_private.system_model.analyses_and_results.duty_cycles.excel_batch_duty_cycles._6685": [
            "MASTAFileDetails"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ExcelBatchDutyCycleCreator",
    "ExcelBatchDutyCycleSpectraCreatorDetails",
    "ExcelFileDetails",
    "ExcelSheet",
    "ExcelSheetDesignStateSelector",
    "MASTAFileDetails",
)
