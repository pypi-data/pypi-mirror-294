"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5789 import (
        AbstractDesignStateLoadCaseGroup,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5790 import (
        AbstractLoadCaseGroup,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5791 import (
        AbstractStaticLoadCaseGroup,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5792 import (
        ClutchEngagementStatus,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5793 import (
        ConceptSynchroGearEngagementStatus,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5794 import (
        DesignState,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5795 import (
        DutyCycle,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5796 import (
        GenericClutchEngagementStatus,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5797 import (
        LoadCaseGroupHistograms,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5798 import (
        SubGroupInSingleDesignState,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5799 import (
        SystemOptimisationGearSet,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5800 import (
        SystemOptimiserGearSetOptimisation,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5801 import (
        SystemOptimiserTargets,
    )
    from mastapy._private.system_model.analyses_and_results.load_case_groups._5802 import (
        TimeSeriesLoadCaseGroup,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.load_case_groups._5789": [
            "AbstractDesignStateLoadCaseGroup"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5790": [
            "AbstractLoadCaseGroup"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5791": [
            "AbstractStaticLoadCaseGroup"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5792": [
            "ClutchEngagementStatus"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5793": [
            "ConceptSynchroGearEngagementStatus"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5794": [
            "DesignState"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5795": [
            "DutyCycle"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5796": [
            "GenericClutchEngagementStatus"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5797": [
            "LoadCaseGroupHistograms"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5798": [
            "SubGroupInSingleDesignState"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5799": [
            "SystemOptimisationGearSet"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5800": [
            "SystemOptimiserGearSetOptimisation"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5801": [
            "SystemOptimiserTargets"
        ],
        "_private.system_model.analyses_and_results.load_case_groups._5802": [
            "TimeSeriesLoadCaseGroup"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractDesignStateLoadCaseGroup",
    "AbstractLoadCaseGroup",
    "AbstractStaticLoadCaseGroup",
    "ClutchEngagementStatus",
    "ConceptSynchroGearEngagementStatus",
    "DesignState",
    "DutyCycle",
    "GenericClutchEngagementStatus",
    "LoadCaseGroupHistograms",
    "SubGroupInSingleDesignState",
    "SystemOptimisationGearSet",
    "SystemOptimiserGearSetOptimisation",
    "SystemOptimiserTargets",
    "TimeSeriesLoadCaseGroup",
)
