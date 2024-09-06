"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.splines._1437 import (
        CustomSplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1438 import (
        CustomSplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1439 import (
        DetailedSplineJointSettings,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1440 import (
        DIN5480SplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1441 import (
        DIN5480SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1442 import (
        DudleyEffectiveLengthApproximationOption,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1443 import FitTypes
    from mastapy._private.detailed_rigid_connectors.splines._1444 import (
        GBT3478SplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1445 import (
        GBT3478SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1446 import (
        HeatTreatmentTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1447 import (
        ISO4156SplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1448 import (
        ISO4156SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1449 import (
        JISB1603SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1450 import (
        ManufacturingTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1451 import Modules
    from mastapy._private.detailed_rigid_connectors.splines._1452 import (
        PressureAngleTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1453 import RootTypes
    from mastapy._private.detailed_rigid_connectors.splines._1454 import (
        SAEFatigueLifeFactorTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1455 import (
        SAESplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1456 import (
        SAESplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1457 import SAETorqueCycles
    from mastapy._private.detailed_rigid_connectors.splines._1458 import (
        SplineDesignTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1459 import (
        FinishingMethods,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1460 import (
        SplineFitClassType,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1461 import (
        SplineFixtureTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1462 import (
        SplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1463 import (
        SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1464 import SplineMaterial
    from mastapy._private.detailed_rigid_connectors.splines._1465 import (
        SplineRatingTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1466 import (
        SplineToleranceClassTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1467 import (
        StandardSplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1468 import (
        StandardSplineJointDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.splines._1437": ["CustomSplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1438": ["CustomSplineJointDesign"],
        "_private.detailed_rigid_connectors.splines._1439": [
            "DetailedSplineJointSettings"
        ],
        "_private.detailed_rigid_connectors.splines._1440": ["DIN5480SplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1441": [
            "DIN5480SplineJointDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1442": [
            "DudleyEffectiveLengthApproximationOption"
        ],
        "_private.detailed_rigid_connectors.splines._1443": ["FitTypes"],
        "_private.detailed_rigid_connectors.splines._1444": ["GBT3478SplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1445": [
            "GBT3478SplineJointDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1446": ["HeatTreatmentTypes"],
        "_private.detailed_rigid_connectors.splines._1447": ["ISO4156SplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1448": [
            "ISO4156SplineJointDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1449": [
            "JISB1603SplineJointDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1450": ["ManufacturingTypes"],
        "_private.detailed_rigid_connectors.splines._1451": ["Modules"],
        "_private.detailed_rigid_connectors.splines._1452": ["PressureAngleTypes"],
        "_private.detailed_rigid_connectors.splines._1453": ["RootTypes"],
        "_private.detailed_rigid_connectors.splines._1454": [
            "SAEFatigueLifeFactorTypes"
        ],
        "_private.detailed_rigid_connectors.splines._1455": ["SAESplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1456": ["SAESplineJointDesign"],
        "_private.detailed_rigid_connectors.splines._1457": ["SAETorqueCycles"],
        "_private.detailed_rigid_connectors.splines._1458": ["SplineDesignTypes"],
        "_private.detailed_rigid_connectors.splines._1459": ["FinishingMethods"],
        "_private.detailed_rigid_connectors.splines._1460": ["SplineFitClassType"],
        "_private.detailed_rigid_connectors.splines._1461": ["SplineFixtureTypes"],
        "_private.detailed_rigid_connectors.splines._1462": ["SplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1463": ["SplineJointDesign"],
        "_private.detailed_rigid_connectors.splines._1464": ["SplineMaterial"],
        "_private.detailed_rigid_connectors.splines._1465": ["SplineRatingTypes"],
        "_private.detailed_rigid_connectors.splines._1466": [
            "SplineToleranceClassTypes"
        ],
        "_private.detailed_rigid_connectors.splines._1467": [
            "StandardSplineHalfDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1468": [
            "StandardSplineJointDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CustomSplineHalfDesign",
    "CustomSplineJointDesign",
    "DetailedSplineJointSettings",
    "DIN5480SplineHalfDesign",
    "DIN5480SplineJointDesign",
    "DudleyEffectiveLengthApproximationOption",
    "FitTypes",
    "GBT3478SplineHalfDesign",
    "GBT3478SplineJointDesign",
    "HeatTreatmentTypes",
    "ISO4156SplineHalfDesign",
    "ISO4156SplineJointDesign",
    "JISB1603SplineJointDesign",
    "ManufacturingTypes",
    "Modules",
    "PressureAngleTypes",
    "RootTypes",
    "SAEFatigueLifeFactorTypes",
    "SAESplineHalfDesign",
    "SAESplineJointDesign",
    "SAETorqueCycles",
    "SplineDesignTypes",
    "FinishingMethods",
    "SplineFitClassType",
    "SplineFixtureTypes",
    "SplineHalfDesign",
    "SplineJointDesign",
    "SplineMaterial",
    "SplineRatingTypes",
    "SplineToleranceClassTypes",
    "StandardSplineHalfDesign",
    "StandardSplineJointDesign",
)
