"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.tolerances._1954 import BearingConnectionComponent
    from mastapy._private.bearings.tolerances._1955 import InternalClearanceClass
    from mastapy._private.bearings.tolerances._1956 import BearingToleranceClass
    from mastapy._private.bearings.tolerances._1957 import (
        BearingToleranceDefinitionOptions,
    )
    from mastapy._private.bearings.tolerances._1958 import FitType
    from mastapy._private.bearings.tolerances._1959 import InnerRingTolerance
    from mastapy._private.bearings.tolerances._1960 import InnerSupportTolerance
    from mastapy._private.bearings.tolerances._1961 import InterferenceDetail
    from mastapy._private.bearings.tolerances._1962 import InterferenceTolerance
    from mastapy._private.bearings.tolerances._1963 import ITDesignation
    from mastapy._private.bearings.tolerances._1964 import MountingSleeveDiameterDetail
    from mastapy._private.bearings.tolerances._1965 import OuterRingTolerance
    from mastapy._private.bearings.tolerances._1966 import OuterSupportTolerance
    from mastapy._private.bearings.tolerances._1967 import RaceRoundnessAtAngle
    from mastapy._private.bearings.tolerances._1968 import RadialSpecificationMethod
    from mastapy._private.bearings.tolerances._1969 import RingDetail
    from mastapy._private.bearings.tolerances._1970 import RingTolerance
    from mastapy._private.bearings.tolerances._1971 import RoundnessSpecification
    from mastapy._private.bearings.tolerances._1972 import RoundnessSpecificationType
    from mastapy._private.bearings.tolerances._1973 import SupportDetail
    from mastapy._private.bearings.tolerances._1974 import SupportMaterialSource
    from mastapy._private.bearings.tolerances._1975 import SupportTolerance
    from mastapy._private.bearings.tolerances._1976 import (
        SupportToleranceLocationDesignation,
    )
    from mastapy._private.bearings.tolerances._1977 import ToleranceCombination
    from mastapy._private.bearings.tolerances._1978 import TypeOfFit
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.tolerances._1954": ["BearingConnectionComponent"],
        "_private.bearings.tolerances._1955": ["InternalClearanceClass"],
        "_private.bearings.tolerances._1956": ["BearingToleranceClass"],
        "_private.bearings.tolerances._1957": ["BearingToleranceDefinitionOptions"],
        "_private.bearings.tolerances._1958": ["FitType"],
        "_private.bearings.tolerances._1959": ["InnerRingTolerance"],
        "_private.bearings.tolerances._1960": ["InnerSupportTolerance"],
        "_private.bearings.tolerances._1961": ["InterferenceDetail"],
        "_private.bearings.tolerances._1962": ["InterferenceTolerance"],
        "_private.bearings.tolerances._1963": ["ITDesignation"],
        "_private.bearings.tolerances._1964": ["MountingSleeveDiameterDetail"],
        "_private.bearings.tolerances._1965": ["OuterRingTolerance"],
        "_private.bearings.tolerances._1966": ["OuterSupportTolerance"],
        "_private.bearings.tolerances._1967": ["RaceRoundnessAtAngle"],
        "_private.bearings.tolerances._1968": ["RadialSpecificationMethod"],
        "_private.bearings.tolerances._1969": ["RingDetail"],
        "_private.bearings.tolerances._1970": ["RingTolerance"],
        "_private.bearings.tolerances._1971": ["RoundnessSpecification"],
        "_private.bearings.tolerances._1972": ["RoundnessSpecificationType"],
        "_private.bearings.tolerances._1973": ["SupportDetail"],
        "_private.bearings.tolerances._1974": ["SupportMaterialSource"],
        "_private.bearings.tolerances._1975": ["SupportTolerance"],
        "_private.bearings.tolerances._1976": ["SupportToleranceLocationDesignation"],
        "_private.bearings.tolerances._1977": ["ToleranceCombination"],
        "_private.bearings.tolerances._1978": ["TypeOfFit"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BearingConnectionComponent",
    "InternalClearanceClass",
    "BearingToleranceClass",
    "BearingToleranceDefinitionOptions",
    "FitType",
    "InnerRingTolerance",
    "InnerSupportTolerance",
    "InterferenceDetail",
    "InterferenceTolerance",
    "ITDesignation",
    "MountingSleeveDiameterDetail",
    "OuterRingTolerance",
    "OuterSupportTolerance",
    "RaceRoundnessAtAngle",
    "RadialSpecificationMethod",
    "RingDetail",
    "RingTolerance",
    "RoundnessSpecification",
    "RoundnessSpecificationType",
    "SupportDetail",
    "SupportMaterialSource",
    "SupportTolerance",
    "SupportToleranceLocationDesignation",
    "ToleranceCombination",
    "TypeOfFit",
)
