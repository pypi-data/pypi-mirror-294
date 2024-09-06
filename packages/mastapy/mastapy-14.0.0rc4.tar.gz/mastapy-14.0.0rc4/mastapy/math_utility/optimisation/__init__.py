"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.math_utility.optimisation._1587 import AbstractOptimisable
    from mastapy._private.math_utility.optimisation._1588 import (
        DesignSpaceSearchStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1589 import InputSetter
    from mastapy._private.math_utility.optimisation._1590 import Optimisable
    from mastapy._private.math_utility.optimisation._1591 import OptimisationHistory
    from mastapy._private.math_utility.optimisation._1592 import OptimizationInput
    from mastapy._private.math_utility.optimisation._1593 import OptimizationVariable
    from mastapy._private.math_utility.optimisation._1594 import (
        ParetoOptimisationFilter,
    )
    from mastapy._private.math_utility.optimisation._1595 import ParetoOptimisationInput
    from mastapy._private.math_utility.optimisation._1596 import (
        ParetoOptimisationOutput,
    )
    from mastapy._private.math_utility.optimisation._1597 import (
        ParetoOptimisationStrategy,
    )
    from mastapy._private.math_utility.optimisation._1598 import (
        ParetoOptimisationStrategyBars,
    )
    from mastapy._private.math_utility.optimisation._1599 import (
        ParetoOptimisationStrategyChartInformation,
    )
    from mastapy._private.math_utility.optimisation._1600 import (
        ParetoOptimisationStrategyDatabase,
    )
    from mastapy._private.math_utility.optimisation._1601 import (
        ParetoOptimisationVariable,
    )
    from mastapy._private.math_utility.optimisation._1602 import (
        ParetoOptimisationVariableBase,
    )
    from mastapy._private.math_utility.optimisation._1603 import (
        PropertyTargetForDominantCandidateSearch,
    )
    from mastapy._private.math_utility.optimisation._1604 import (
        ReportingOptimizationInput,
    )
    from mastapy._private.math_utility.optimisation._1605 import (
        SpecifyOptimisationInputAs,
    )
    from mastapy._private.math_utility.optimisation._1606 import TargetingPropertyTo
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.math_utility.optimisation._1587": ["AbstractOptimisable"],
        "_private.math_utility.optimisation._1588": [
            "DesignSpaceSearchStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1589": ["InputSetter"],
        "_private.math_utility.optimisation._1590": ["Optimisable"],
        "_private.math_utility.optimisation._1591": ["OptimisationHistory"],
        "_private.math_utility.optimisation._1592": ["OptimizationInput"],
        "_private.math_utility.optimisation._1593": ["OptimizationVariable"],
        "_private.math_utility.optimisation._1594": ["ParetoOptimisationFilter"],
        "_private.math_utility.optimisation._1595": ["ParetoOptimisationInput"],
        "_private.math_utility.optimisation._1596": ["ParetoOptimisationOutput"],
        "_private.math_utility.optimisation._1597": ["ParetoOptimisationStrategy"],
        "_private.math_utility.optimisation._1598": ["ParetoOptimisationStrategyBars"],
        "_private.math_utility.optimisation._1599": [
            "ParetoOptimisationStrategyChartInformation"
        ],
        "_private.math_utility.optimisation._1600": [
            "ParetoOptimisationStrategyDatabase"
        ],
        "_private.math_utility.optimisation._1601": ["ParetoOptimisationVariable"],
        "_private.math_utility.optimisation._1602": ["ParetoOptimisationVariableBase"],
        "_private.math_utility.optimisation._1603": [
            "PropertyTargetForDominantCandidateSearch"
        ],
        "_private.math_utility.optimisation._1604": ["ReportingOptimizationInput"],
        "_private.math_utility.optimisation._1605": ["SpecifyOptimisationInputAs"],
        "_private.math_utility.optimisation._1606": ["TargetingPropertyTo"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractOptimisable",
    "DesignSpaceSearchStrategyDatabase",
    "InputSetter",
    "Optimisable",
    "OptimisationHistory",
    "OptimizationInput",
    "OptimizationVariable",
    "ParetoOptimisationFilter",
    "ParetoOptimisationInput",
    "ParetoOptimisationOutput",
    "ParetoOptimisationStrategy",
    "ParetoOptimisationStrategyBars",
    "ParetoOptimisationStrategyChartInformation",
    "ParetoOptimisationStrategyDatabase",
    "ParetoOptimisationVariable",
    "ParetoOptimisationVariableBase",
    "PropertyTargetForDominantCandidateSearch",
    "ReportingOptimizationInput",
    "SpecifyOptimisationInputAs",
    "TargetingPropertyTo",
)
