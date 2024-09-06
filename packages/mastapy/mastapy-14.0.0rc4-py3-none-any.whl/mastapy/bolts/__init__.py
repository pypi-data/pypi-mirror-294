"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bolts._1513 import AxialLoadType
    from mastapy._private.bolts._1514 import BoltedJointMaterial
    from mastapy._private.bolts._1515 import BoltedJointMaterialDatabase
    from mastapy._private.bolts._1516 import BoltGeometry
    from mastapy._private.bolts._1517 import BoltGeometryDatabase
    from mastapy._private.bolts._1518 import BoltMaterial
    from mastapy._private.bolts._1519 import BoltMaterialDatabase
    from mastapy._private.bolts._1520 import BoltSection
    from mastapy._private.bolts._1521 import BoltShankType
    from mastapy._private.bolts._1522 import BoltTypes
    from mastapy._private.bolts._1523 import ClampedSection
    from mastapy._private.bolts._1524 import ClampedSectionMaterialDatabase
    from mastapy._private.bolts._1525 import DetailedBoltDesign
    from mastapy._private.bolts._1526 import DetailedBoltedJointDesign
    from mastapy._private.bolts._1527 import HeadCapTypes
    from mastapy._private.bolts._1528 import JointGeometries
    from mastapy._private.bolts._1529 import JointTypes
    from mastapy._private.bolts._1530 import LoadedBolt
    from mastapy._private.bolts._1531 import RolledBeforeOrAfterHeatTreatment
    from mastapy._private.bolts._1532 import StandardSizes
    from mastapy._private.bolts._1533 import StrengthGrades
    from mastapy._private.bolts._1534 import ThreadTypes
    from mastapy._private.bolts._1535 import TighteningTechniques
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bolts._1513": ["AxialLoadType"],
        "_private.bolts._1514": ["BoltedJointMaterial"],
        "_private.bolts._1515": ["BoltedJointMaterialDatabase"],
        "_private.bolts._1516": ["BoltGeometry"],
        "_private.bolts._1517": ["BoltGeometryDatabase"],
        "_private.bolts._1518": ["BoltMaterial"],
        "_private.bolts._1519": ["BoltMaterialDatabase"],
        "_private.bolts._1520": ["BoltSection"],
        "_private.bolts._1521": ["BoltShankType"],
        "_private.bolts._1522": ["BoltTypes"],
        "_private.bolts._1523": ["ClampedSection"],
        "_private.bolts._1524": ["ClampedSectionMaterialDatabase"],
        "_private.bolts._1525": ["DetailedBoltDesign"],
        "_private.bolts._1526": ["DetailedBoltedJointDesign"],
        "_private.bolts._1527": ["HeadCapTypes"],
        "_private.bolts._1528": ["JointGeometries"],
        "_private.bolts._1529": ["JointTypes"],
        "_private.bolts._1530": ["LoadedBolt"],
        "_private.bolts._1531": ["RolledBeforeOrAfterHeatTreatment"],
        "_private.bolts._1532": ["StandardSizes"],
        "_private.bolts._1533": ["StrengthGrades"],
        "_private.bolts._1534": ["ThreadTypes"],
        "_private.bolts._1535": ["TighteningTechniques"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AxialLoadType",
    "BoltedJointMaterial",
    "BoltedJointMaterialDatabase",
    "BoltGeometry",
    "BoltGeometryDatabase",
    "BoltMaterial",
    "BoltMaterialDatabase",
    "BoltSection",
    "BoltShankType",
    "BoltTypes",
    "ClampedSection",
    "ClampedSectionMaterialDatabase",
    "DetailedBoltDesign",
    "DetailedBoltedJointDesign",
    "HeadCapTypes",
    "JointGeometries",
    "JointTypes",
    "LoadedBolt",
    "RolledBeforeOrAfterHeatTreatment",
    "StandardSizes",
    "StrengthGrades",
    "ThreadTypes",
    "TighteningTechniques",
)
