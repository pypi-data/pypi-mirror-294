"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7704 import (
        AnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7705 import (
        AbstractAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7706 import (
        CompoundAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7707 import (
        ConnectionAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7708 import (
        ConnectionCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7709 import (
        ConnectionFEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7710 import (
        ConnectionStaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7711 import (
        ConnectionTimeSeriesLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7712 import (
        DesignEntityCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7713 import (
        FEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7714 import (
        PartAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7715 import (
        PartCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7716 import (
        PartFEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7717 import (
        PartStaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7718 import (
        PartTimeSeriesLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7719 import (
        StaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7720 import (
        TimeSeriesLoadAnalysisCase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.analysis_cases._7704": [
            "AnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7705": [
            "AbstractAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7706": [
            "CompoundAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7707": [
            "ConnectionAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7708": [
            "ConnectionCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7709": [
            "ConnectionFEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7710": [
            "ConnectionStaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7711": [
            "ConnectionTimeSeriesLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7712": [
            "DesignEntityCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7713": [
            "FEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7714": [
            "PartAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7715": [
            "PartCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7716": [
            "PartFEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7717": [
            "PartStaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7718": [
            "PartTimeSeriesLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7719": [
            "StaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7720": [
            "TimeSeriesLoadAnalysisCase"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AnalysisCase",
    "AbstractAnalysisOptions",
    "CompoundAnalysisCase",
    "ConnectionAnalysisCase",
    "ConnectionCompoundAnalysis",
    "ConnectionFEAnalysis",
    "ConnectionStaticLoadAnalysisCase",
    "ConnectionTimeSeriesLoadAnalysisCase",
    "DesignEntityCompoundAnalysis",
    "FEAnalysis",
    "PartAnalysisCase",
    "PartCompoundAnalysis",
    "PartFEAnalysis",
    "PartStaticLoadAnalysisCase",
    "PartTimeSeriesLoadAnalysisCase",
    "StaticLoadAnalysisCase",
    "TimeSeriesLoadAnalysisCase",
)
