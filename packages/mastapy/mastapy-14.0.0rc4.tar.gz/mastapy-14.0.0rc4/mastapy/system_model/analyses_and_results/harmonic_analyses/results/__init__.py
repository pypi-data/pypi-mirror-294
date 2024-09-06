"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5977 import (
        ConnectedComponentType,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5978 import (
        ExcitationSourceSelection,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5979 import (
        ExcitationSourceSelectionBase,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5980 import (
        ExcitationSourceSelectionGroup,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5981 import (
        HarmonicSelection,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5982 import (
        ModalContributionDisplayMethod,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5983 import (
        ModalContributionFilteringMethod,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5984 import (
        ResultLocationSelectionGroup,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5985 import (
        ResultLocationSelectionGroups,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._5986 import (
        ResultNodeSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5977": [
            "ConnectedComponentType"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5978": [
            "ExcitationSourceSelection"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5979": [
            "ExcitationSourceSelectionBase"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5980": [
            "ExcitationSourceSelectionGroup"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5981": [
            "HarmonicSelection"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5982": [
            "ModalContributionDisplayMethod"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5983": [
            "ModalContributionFilteringMethod"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5984": [
            "ResultLocationSelectionGroup"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5985": [
            "ResultLocationSelectionGroups"
        ],
        "_private.system_model.analyses_and_results.harmonic_analyses.results._5986": [
            "ResultNodeSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConnectedComponentType",
    "ExcitationSourceSelection",
    "ExcitationSourceSelectionBase",
    "ExcitationSourceSelectionGroup",
    "HarmonicSelection",
    "ModalContributionDisplayMethod",
    "ModalContributionFilteringMethod",
    "ResultLocationSelectionGroup",
    "ResultLocationSelectionGroups",
    "ResultNodeSelection",
)
