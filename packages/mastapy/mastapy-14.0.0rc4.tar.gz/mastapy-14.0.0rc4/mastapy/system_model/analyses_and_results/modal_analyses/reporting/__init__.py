"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4830 import (
        CalculateFullFEResultsForMode,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4831 import (
        CampbellDiagramReport,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4832 import (
        ComponentPerModeResult,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4833 import (
        DesignEntityModalAnalysisGroupResults,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4834 import (
        ModalCMSResultsForModeAndFE,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4835 import (
        PerModeResultsReport,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4836 import (
        RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4837 import (
        RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4838 import (
        RigidlyConnectedDesignEntityGroupModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4839 import (
        ShaftPerModeResult,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4840 import (
        SingleExcitationResultsModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4841 import (
        SingleModeResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4830": [
            "CalculateFullFEResultsForMode"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4831": [
            "CampbellDiagramReport"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4832": [
            "ComponentPerModeResult"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4833": [
            "DesignEntityModalAnalysisGroupResults"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4834": [
            "ModalCMSResultsForModeAndFE"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4835": [
            "PerModeResultsReport"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4836": [
            "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4837": [
            "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4838": [
            "RigidlyConnectedDesignEntityGroupModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4839": [
            "ShaftPerModeResult"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4840": [
            "SingleExcitationResultsModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4841": [
            "SingleModeResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CalculateFullFEResultsForMode",
    "CampbellDiagramReport",
    "ComponentPerModeResult",
    "DesignEntityModalAnalysisGroupResults",
    "ModalCMSResultsForModeAndFE",
    "PerModeResultsReport",
    "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis",
    "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis",
    "RigidlyConnectedDesignEntityGroupModalAnalysis",
    "ShaftPerModeResult",
    "SingleExcitationResultsModalAnalysis",
    "SingleModeResults",
)
