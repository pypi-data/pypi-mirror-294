"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1471 import (
        AGMA6123SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1472 import (
        AGMA6123SplineJointRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1473 import (
        DIN5466SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1474 import (
        DIN5466SplineRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1475 import (
        GBT17855SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1476 import (
        GBT17855SplineJointRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1477 import (
        SAESplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1478 import (
        SAESplineJointRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1479 import (
        SplineHalfRating,
    )
    from mastapy._private.detailed_rigid_connectors.splines.ratings._1480 import (
        SplineJointRating,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.splines.ratings._1471": [
            "AGMA6123SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1472": [
            "AGMA6123SplineJointRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1473": [
            "DIN5466SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1474": [
            "DIN5466SplineRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1475": [
            "GBT17855SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1476": [
            "GBT17855SplineJointRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1477": [
            "SAESplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1478": [
            "SAESplineJointRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1479": [
            "SplineHalfRating"
        ],
        "_private.detailed_rigid_connectors.splines.ratings._1480": [
            "SplineJointRating"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMA6123SplineHalfRating",
    "AGMA6123SplineJointRating",
    "DIN5466SplineHalfRating",
    "DIN5466SplineRating",
    "GBT17855SplineHalfRating",
    "GBT17855SplineJointRating",
    "SAESplineHalfRating",
    "SAESplineJointRating",
    "SplineHalfRating",
    "SplineJointRating",
)
