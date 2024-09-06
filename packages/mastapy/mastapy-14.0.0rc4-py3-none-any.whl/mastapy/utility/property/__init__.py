"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.utility.property._1889 import DeletableCollectionMember
    from mastapy._private.utility.property._1890 import DutyCyclePropertySummary
    from mastapy._private.utility.property._1891 import DutyCyclePropertySummaryForce
    from mastapy._private.utility.property._1892 import (
        DutyCyclePropertySummaryPercentage,
    )
    from mastapy._private.utility.property._1893 import (
        DutyCyclePropertySummarySmallAngle,
    )
    from mastapy._private.utility.property._1894 import DutyCyclePropertySummaryStress
    from mastapy._private.utility.property._1895 import (
        DutyCyclePropertySummaryVeryShortLength,
    )
    from mastapy._private.utility.property._1896 import EnumWithBoolean
    from mastapy._private.utility.property._1897 import (
        NamedRangeWithOverridableMinAndMax,
    )
    from mastapy._private.utility.property._1898 import TypedObjectsWithOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.utility.property._1889": ["DeletableCollectionMember"],
        "_private.utility.property._1890": ["DutyCyclePropertySummary"],
        "_private.utility.property._1891": ["DutyCyclePropertySummaryForce"],
        "_private.utility.property._1892": ["DutyCyclePropertySummaryPercentage"],
        "_private.utility.property._1893": ["DutyCyclePropertySummarySmallAngle"],
        "_private.utility.property._1894": ["DutyCyclePropertySummaryStress"],
        "_private.utility.property._1895": ["DutyCyclePropertySummaryVeryShortLength"],
        "_private.utility.property._1896": ["EnumWithBoolean"],
        "_private.utility.property._1897": ["NamedRangeWithOverridableMinAndMax"],
        "_private.utility.property._1898": ["TypedObjectsWithOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DeletableCollectionMember",
    "DutyCyclePropertySummary",
    "DutyCyclePropertySummaryForce",
    "DutyCyclePropertySummaryPercentage",
    "DutyCyclePropertySummarySmallAngle",
    "DutyCyclePropertySummaryStress",
    "DutyCyclePropertySummaryVeryShortLength",
    "EnumWithBoolean",
    "NamedRangeWithOverridableMinAndMax",
    "TypedObjectsWithOption",
)
