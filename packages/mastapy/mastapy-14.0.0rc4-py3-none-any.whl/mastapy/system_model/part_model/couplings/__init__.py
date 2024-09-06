"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.couplings._2634 import BeltDrive
    from mastapy._private.system_model.part_model.couplings._2635 import BeltDriveType
    from mastapy._private.system_model.part_model.couplings._2636 import Clutch
    from mastapy._private.system_model.part_model.couplings._2637 import ClutchHalf
    from mastapy._private.system_model.part_model.couplings._2638 import ClutchType
    from mastapy._private.system_model.part_model.couplings._2639 import ConceptCoupling
    from mastapy._private.system_model.part_model.couplings._2640 import (
        ConceptCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2641 import (
        ConceptCouplingHalfPositioning,
    )
    from mastapy._private.system_model.part_model.couplings._2642 import Coupling
    from mastapy._private.system_model.part_model.couplings._2643 import CouplingHalf
    from mastapy._private.system_model.part_model.couplings._2644 import (
        CrowningSpecification,
    )
    from mastapy._private.system_model.part_model.couplings._2645 import CVT
    from mastapy._private.system_model.part_model.couplings._2646 import CVTPulley
    from mastapy._private.system_model.part_model.couplings._2647 import (
        PartToPartShearCoupling,
    )
    from mastapy._private.system_model.part_model.couplings._2648 import (
        PartToPartShearCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2649 import (
        PitchErrorFlankOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2650 import Pulley
    from mastapy._private.system_model.part_model.couplings._2651 import (
        RigidConnectorStiffnessType,
    )
    from mastapy._private.system_model.part_model.couplings._2652 import (
        RigidConnectorTiltStiffnessTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2653 import (
        RigidConnectorToothLocation,
    )
    from mastapy._private.system_model.part_model.couplings._2654 import (
        RigidConnectorToothSpacingType,
    )
    from mastapy._private.system_model.part_model.couplings._2655 import (
        RigidConnectorTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2656 import RollingRing
    from mastapy._private.system_model.part_model.couplings._2657 import (
        RollingRingAssembly,
    )
    from mastapy._private.system_model.part_model.couplings._2658 import (
        ShaftHubConnection,
    )
    from mastapy._private.system_model.part_model.couplings._2659 import (
        SplineFitOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2660 import (
        SplineLeadRelief,
    )
    from mastapy._private.system_model.part_model.couplings._2661 import (
        SplinePitchErrorInputType,
    )
    from mastapy._private.system_model.part_model.couplings._2662 import (
        SplinePitchErrorOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2663 import SpringDamper
    from mastapy._private.system_model.part_model.couplings._2664 import (
        SpringDamperHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2665 import Synchroniser
    from mastapy._private.system_model.part_model.couplings._2666 import (
        SynchroniserCone,
    )
    from mastapy._private.system_model.part_model.couplings._2667 import (
        SynchroniserHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2668 import (
        SynchroniserPart,
    )
    from mastapy._private.system_model.part_model.couplings._2669 import (
        SynchroniserSleeve,
    )
    from mastapy._private.system_model.part_model.couplings._2670 import TorqueConverter
    from mastapy._private.system_model.part_model.couplings._2671 import (
        TorqueConverterPump,
    )
    from mastapy._private.system_model.part_model.couplings._2672 import (
        TorqueConverterSpeedRatio,
    )
    from mastapy._private.system_model.part_model.couplings._2673 import (
        TorqueConverterTurbine,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.couplings._2634": ["BeltDrive"],
        "_private.system_model.part_model.couplings._2635": ["BeltDriveType"],
        "_private.system_model.part_model.couplings._2636": ["Clutch"],
        "_private.system_model.part_model.couplings._2637": ["ClutchHalf"],
        "_private.system_model.part_model.couplings._2638": ["ClutchType"],
        "_private.system_model.part_model.couplings._2639": ["ConceptCoupling"],
        "_private.system_model.part_model.couplings._2640": ["ConceptCouplingHalf"],
        "_private.system_model.part_model.couplings._2641": [
            "ConceptCouplingHalfPositioning"
        ],
        "_private.system_model.part_model.couplings._2642": ["Coupling"],
        "_private.system_model.part_model.couplings._2643": ["CouplingHalf"],
        "_private.system_model.part_model.couplings._2644": ["CrowningSpecification"],
        "_private.system_model.part_model.couplings._2645": ["CVT"],
        "_private.system_model.part_model.couplings._2646": ["CVTPulley"],
        "_private.system_model.part_model.couplings._2647": ["PartToPartShearCoupling"],
        "_private.system_model.part_model.couplings._2648": [
            "PartToPartShearCouplingHalf"
        ],
        "_private.system_model.part_model.couplings._2649": ["PitchErrorFlankOptions"],
        "_private.system_model.part_model.couplings._2650": ["Pulley"],
        "_private.system_model.part_model.couplings._2651": [
            "RigidConnectorStiffnessType"
        ],
        "_private.system_model.part_model.couplings._2652": [
            "RigidConnectorTiltStiffnessTypes"
        ],
        "_private.system_model.part_model.couplings._2653": [
            "RigidConnectorToothLocation"
        ],
        "_private.system_model.part_model.couplings._2654": [
            "RigidConnectorToothSpacingType"
        ],
        "_private.system_model.part_model.couplings._2655": ["RigidConnectorTypes"],
        "_private.system_model.part_model.couplings._2656": ["RollingRing"],
        "_private.system_model.part_model.couplings._2657": ["RollingRingAssembly"],
        "_private.system_model.part_model.couplings._2658": ["ShaftHubConnection"],
        "_private.system_model.part_model.couplings._2659": ["SplineFitOptions"],
        "_private.system_model.part_model.couplings._2660": ["SplineLeadRelief"],
        "_private.system_model.part_model.couplings._2661": [
            "SplinePitchErrorInputType"
        ],
        "_private.system_model.part_model.couplings._2662": ["SplinePitchErrorOptions"],
        "_private.system_model.part_model.couplings._2663": ["SpringDamper"],
        "_private.system_model.part_model.couplings._2664": ["SpringDamperHalf"],
        "_private.system_model.part_model.couplings._2665": ["Synchroniser"],
        "_private.system_model.part_model.couplings._2666": ["SynchroniserCone"],
        "_private.system_model.part_model.couplings._2667": ["SynchroniserHalf"],
        "_private.system_model.part_model.couplings._2668": ["SynchroniserPart"],
        "_private.system_model.part_model.couplings._2669": ["SynchroniserSleeve"],
        "_private.system_model.part_model.couplings._2670": ["TorqueConverter"],
        "_private.system_model.part_model.couplings._2671": ["TorqueConverterPump"],
        "_private.system_model.part_model.couplings._2672": [
            "TorqueConverterSpeedRatio"
        ],
        "_private.system_model.part_model.couplings._2673": ["TorqueConverterTurbine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "ConceptCouplingHalfPositioning",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "PitchErrorFlankOptions",
    "Pulley",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineFitOptions",
    "SplineLeadRelief",
    "SplinePitchErrorInputType",
    "SplinePitchErrorOptions",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)
