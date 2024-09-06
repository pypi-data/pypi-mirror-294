"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model._2488 import Assembly
    from mastapy._private.system_model.part_model._2489 import AbstractAssembly
    from mastapy._private.system_model.part_model._2490 import AbstractShaft
    from mastapy._private.system_model.part_model._2491 import AbstractShaftOrHousing
    from mastapy._private.system_model.part_model._2492 import (
        AGMALoadSharingTableApplicationLevel,
    )
    from mastapy._private.system_model.part_model._2493 import (
        AxialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2494 import Bearing
    from mastapy._private.system_model.part_model._2495 import BearingF0InputMethod
    from mastapy._private.system_model.part_model._2496 import (
        BearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2497 import Bolt
    from mastapy._private.system_model.part_model._2498 import BoltedJoint
    from mastapy._private.system_model.part_model._2499 import Component
    from mastapy._private.system_model.part_model._2500 import ComponentsConnectedResult
    from mastapy._private.system_model.part_model._2501 import ConnectedSockets
    from mastapy._private.system_model.part_model._2502 import Connector
    from mastapy._private.system_model.part_model._2503 import Datum
    from mastapy._private.system_model.part_model._2504 import (
        ElectricMachineSearchRegionSpecificationMethod,
    )
    from mastapy._private.system_model.part_model._2505 import EnginePartLoad
    from mastapy._private.system_model.part_model._2506 import EngineSpeed
    from mastapy._private.system_model.part_model._2507 import ExternalCADModel
    from mastapy._private.system_model.part_model._2508 import FEPart
    from mastapy._private.system_model.part_model._2509 import FlexiblePinAssembly
    from mastapy._private.system_model.part_model._2510 import GuideDxfModel
    from mastapy._private.system_model.part_model._2511 import GuideImage
    from mastapy._private.system_model.part_model._2512 import GuideModelUsage
    from mastapy._private.system_model.part_model._2513 import (
        InnerBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2514 import (
        InternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2515 import LoadSharingModes
    from mastapy._private.system_model.part_model._2516 import LoadSharingSettings
    from mastapy._private.system_model.part_model._2517 import MassDisc
    from mastapy._private.system_model.part_model._2518 import MeasurementComponent
    from mastapy._private.system_model.part_model._2519 import Microphone
    from mastapy._private.system_model.part_model._2520 import MicrophoneArray
    from mastapy._private.system_model.part_model._2521 import MountableComponent
    from mastapy._private.system_model.part_model._2522 import OilLevelSpecification
    from mastapy._private.system_model.part_model._2523 import OilSeal
    from mastapy._private.system_model.part_model._2524 import (
        OuterBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2525 import Part
    from mastapy._private.system_model.part_model._2526 import PlanetCarrier
    from mastapy._private.system_model.part_model._2527 import PlanetCarrierSettings
    from mastapy._private.system_model.part_model._2528 import PointLoad
    from mastapy._private.system_model.part_model._2529 import PowerLoad
    from mastapy._private.system_model.part_model._2530 import (
        RadialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2531 import RootAssembly
    from mastapy._private.system_model.part_model._2532 import (
        ShaftDiameterModificationDueToRollingBearingRing,
    )
    from mastapy._private.system_model.part_model._2533 import SpecialisedAssembly
    from mastapy._private.system_model.part_model._2534 import UnbalancedMass
    from mastapy._private.system_model.part_model._2535 import (
        UnbalancedMassInclusionOption,
    )
    from mastapy._private.system_model.part_model._2536 import VirtualComponent
    from mastapy._private.system_model.part_model._2537 import (
        WindTurbineBladeModeDetails,
    )
    from mastapy._private.system_model.part_model._2538 import (
        WindTurbineSingleBladeDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model._2488": ["Assembly"],
        "_private.system_model.part_model._2489": ["AbstractAssembly"],
        "_private.system_model.part_model._2490": ["AbstractShaft"],
        "_private.system_model.part_model._2491": ["AbstractShaftOrHousing"],
        "_private.system_model.part_model._2492": [
            "AGMALoadSharingTableApplicationLevel"
        ],
        "_private.system_model.part_model._2493": ["AxialInternalClearanceTolerance"],
        "_private.system_model.part_model._2494": ["Bearing"],
        "_private.system_model.part_model._2495": ["BearingF0InputMethod"],
        "_private.system_model.part_model._2496": ["BearingRaceMountingOptions"],
        "_private.system_model.part_model._2497": ["Bolt"],
        "_private.system_model.part_model._2498": ["BoltedJoint"],
        "_private.system_model.part_model._2499": ["Component"],
        "_private.system_model.part_model._2500": ["ComponentsConnectedResult"],
        "_private.system_model.part_model._2501": ["ConnectedSockets"],
        "_private.system_model.part_model._2502": ["Connector"],
        "_private.system_model.part_model._2503": ["Datum"],
        "_private.system_model.part_model._2504": [
            "ElectricMachineSearchRegionSpecificationMethod"
        ],
        "_private.system_model.part_model._2505": ["EnginePartLoad"],
        "_private.system_model.part_model._2506": ["EngineSpeed"],
        "_private.system_model.part_model._2507": ["ExternalCADModel"],
        "_private.system_model.part_model._2508": ["FEPart"],
        "_private.system_model.part_model._2509": ["FlexiblePinAssembly"],
        "_private.system_model.part_model._2510": ["GuideDxfModel"],
        "_private.system_model.part_model._2511": ["GuideImage"],
        "_private.system_model.part_model._2512": ["GuideModelUsage"],
        "_private.system_model.part_model._2513": ["InnerBearingRaceMountingOptions"],
        "_private.system_model.part_model._2514": ["InternalClearanceTolerance"],
        "_private.system_model.part_model._2515": ["LoadSharingModes"],
        "_private.system_model.part_model._2516": ["LoadSharingSettings"],
        "_private.system_model.part_model._2517": ["MassDisc"],
        "_private.system_model.part_model._2518": ["MeasurementComponent"],
        "_private.system_model.part_model._2519": ["Microphone"],
        "_private.system_model.part_model._2520": ["MicrophoneArray"],
        "_private.system_model.part_model._2521": ["MountableComponent"],
        "_private.system_model.part_model._2522": ["OilLevelSpecification"],
        "_private.system_model.part_model._2523": ["OilSeal"],
        "_private.system_model.part_model._2524": ["OuterBearingRaceMountingOptions"],
        "_private.system_model.part_model._2525": ["Part"],
        "_private.system_model.part_model._2526": ["PlanetCarrier"],
        "_private.system_model.part_model._2527": ["PlanetCarrierSettings"],
        "_private.system_model.part_model._2528": ["PointLoad"],
        "_private.system_model.part_model._2529": ["PowerLoad"],
        "_private.system_model.part_model._2530": ["RadialInternalClearanceTolerance"],
        "_private.system_model.part_model._2531": ["RootAssembly"],
        "_private.system_model.part_model._2532": [
            "ShaftDiameterModificationDueToRollingBearingRing"
        ],
        "_private.system_model.part_model._2533": ["SpecialisedAssembly"],
        "_private.system_model.part_model._2534": ["UnbalancedMass"],
        "_private.system_model.part_model._2535": ["UnbalancedMassInclusionOption"],
        "_private.system_model.part_model._2536": ["VirtualComponent"],
        "_private.system_model.part_model._2537": ["WindTurbineBladeModeDetails"],
        "_private.system_model.part_model._2538": ["WindTurbineSingleBladeDetails"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Assembly",
    "AbstractAssembly",
    "AbstractShaft",
    "AbstractShaftOrHousing",
    "AGMALoadSharingTableApplicationLevel",
    "AxialInternalClearanceTolerance",
    "Bearing",
    "BearingF0InputMethod",
    "BearingRaceMountingOptions",
    "Bolt",
    "BoltedJoint",
    "Component",
    "ComponentsConnectedResult",
    "ConnectedSockets",
    "Connector",
    "Datum",
    "ElectricMachineSearchRegionSpecificationMethod",
    "EnginePartLoad",
    "EngineSpeed",
    "ExternalCADModel",
    "FEPart",
    "FlexiblePinAssembly",
    "GuideDxfModel",
    "GuideImage",
    "GuideModelUsage",
    "InnerBearingRaceMountingOptions",
    "InternalClearanceTolerance",
    "LoadSharingModes",
    "LoadSharingSettings",
    "MassDisc",
    "MeasurementComponent",
    "Microphone",
    "MicrophoneArray",
    "MountableComponent",
    "OilLevelSpecification",
    "OilSeal",
    "OuterBearingRaceMountingOptions",
    "Part",
    "PlanetCarrier",
    "PlanetCarrierSettings",
    "PointLoad",
    "PowerLoad",
    "RadialInternalClearanceTolerance",
    "RootAssembly",
    "ShaftDiameterModificationDueToRollingBearingRing",
    "SpecialisedAssembly",
    "UnbalancedMass",
    "UnbalancedMassInclusionOption",
    "VirtualComponent",
    "WindTurbineBladeModeDetails",
    "WindTurbineSingleBladeDetails",
)
