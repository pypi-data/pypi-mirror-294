"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe._2409 import AlignConnectedComponentOptions
    from mastapy._private.system_model.fe._2410 import AlignmentMethod
    from mastapy._private.system_model.fe._2411 import AlignmentMethodForRaceBearing
    from mastapy._private.system_model.fe._2412 import AlignmentUsingAxialNodePositions
    from mastapy._private.system_model.fe._2413 import AngleSource
    from mastapy._private.system_model.fe._2414 import BaseFEWithSelection
    from mastapy._private.system_model.fe._2415 import BatchOperations
    from mastapy._private.system_model.fe._2416 import BearingNodeAlignmentOption
    from mastapy._private.system_model.fe._2417 import BearingNodeOption
    from mastapy._private.system_model.fe._2418 import BearingRaceNodeLink
    from mastapy._private.system_model.fe._2419 import BearingRacePosition
    from mastapy._private.system_model.fe._2420 import ComponentOrientationOption
    from mastapy._private.system_model.fe._2421 import ContactPairWithSelection
    from mastapy._private.system_model.fe._2422 import CoordinateSystemWithSelection
    from mastapy._private.system_model.fe._2423 import CreateConnectedComponentOptions
    from mastapy._private.system_model.fe._2424 import (
        CreateMicrophoneNormalToSurfaceOptions,
    )
    from mastapy._private.system_model.fe._2425 import DegreeOfFreedomBoundaryCondition
    from mastapy._private.system_model.fe._2426 import (
        DegreeOfFreedomBoundaryConditionAngular,
    )
    from mastapy._private.system_model.fe._2427 import (
        DegreeOfFreedomBoundaryConditionLinear,
    )
    from mastapy._private.system_model.fe._2428 import ElectricMachineDataSet
    from mastapy._private.system_model.fe._2429 import ElectricMachineDynamicLoadData
    from mastapy._private.system_model.fe._2430 import ElementFaceGroupWithSelection
    from mastapy._private.system_model.fe._2431 import ElementPropertiesWithSelection
    from mastapy._private.system_model.fe._2432 import FEEntityGroupWithSelection
    from mastapy._private.system_model.fe._2433 import FEExportSettings
    from mastapy._private.system_model.fe._2434 import FEPartDRIVASurfaceSelection
    from mastapy._private.system_model.fe._2435 import FEPartWithBatchOptions
    from mastapy._private.system_model.fe._2436 import FEStiffnessGeometry
    from mastapy._private.system_model.fe._2437 import FEStiffnessTester
    from mastapy._private.system_model.fe._2438 import FESubstructure
    from mastapy._private.system_model.fe._2439 import FESubstructureExportOptions
    from mastapy._private.system_model.fe._2440 import FESubstructureNode
    from mastapy._private.system_model.fe._2441 import FESubstructureNodeModeShape
    from mastapy._private.system_model.fe._2442 import FESubstructureNodeModeShapes
    from mastapy._private.system_model.fe._2443 import FESubstructureType
    from mastapy._private.system_model.fe._2444 import FESubstructureWithBatchOptions
    from mastapy._private.system_model.fe._2445 import FESubstructureWithSelection
    from mastapy._private.system_model.fe._2446 import (
        FESubstructureWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2447 import (
        FESubstructureWithSelectionForHarmonicAnalysis,
    )
    from mastapy._private.system_model.fe._2448 import (
        FESubstructureWithSelectionForModalAnalysis,
    )
    from mastapy._private.system_model.fe._2449 import (
        FESubstructureWithSelectionForStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2450 import GearMeshingOptions
    from mastapy._private.system_model.fe._2451 import (
        IndependentMASTACreatedCondensationNode,
    )
    from mastapy._private.system_model.fe._2452 import (
        LinkComponentAxialPositionErrorReporter,
    )
    from mastapy._private.system_model.fe._2453 import LinkNodeSource
    from mastapy._private.system_model.fe._2454 import MaterialPropertiesWithSelection
    from mastapy._private.system_model.fe._2455 import (
        NodeBoundaryConditionStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2456 import NodeGroupWithSelection
    from mastapy._private.system_model.fe._2457 import NodeSelectionDepthOption
    from mastapy._private.system_model.fe._2458 import (
        OptionsWhenExternalFEFileAlreadyExists,
    )
    from mastapy._private.system_model.fe._2459 import PerLinkExportOptions
    from mastapy._private.system_model.fe._2460 import PerNodeExportOptions
    from mastapy._private.system_model.fe._2461 import RaceBearingFE
    from mastapy._private.system_model.fe._2462 import RaceBearingFESystemDeflection
    from mastapy._private.system_model.fe._2463 import RaceBearingFEWithSelection
    from mastapy._private.system_model.fe._2464 import ReplacedShaftSelectionHelper
    from mastapy._private.system_model.fe._2465 import SystemDeflectionFEExportOptions
    from mastapy._private.system_model.fe._2466 import ThermalExpansionOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe._2409": ["AlignConnectedComponentOptions"],
        "_private.system_model.fe._2410": ["AlignmentMethod"],
        "_private.system_model.fe._2411": ["AlignmentMethodForRaceBearing"],
        "_private.system_model.fe._2412": ["AlignmentUsingAxialNodePositions"],
        "_private.system_model.fe._2413": ["AngleSource"],
        "_private.system_model.fe._2414": ["BaseFEWithSelection"],
        "_private.system_model.fe._2415": ["BatchOperations"],
        "_private.system_model.fe._2416": ["BearingNodeAlignmentOption"],
        "_private.system_model.fe._2417": ["BearingNodeOption"],
        "_private.system_model.fe._2418": ["BearingRaceNodeLink"],
        "_private.system_model.fe._2419": ["BearingRacePosition"],
        "_private.system_model.fe._2420": ["ComponentOrientationOption"],
        "_private.system_model.fe._2421": ["ContactPairWithSelection"],
        "_private.system_model.fe._2422": ["CoordinateSystemWithSelection"],
        "_private.system_model.fe._2423": ["CreateConnectedComponentOptions"],
        "_private.system_model.fe._2424": ["CreateMicrophoneNormalToSurfaceOptions"],
        "_private.system_model.fe._2425": ["DegreeOfFreedomBoundaryCondition"],
        "_private.system_model.fe._2426": ["DegreeOfFreedomBoundaryConditionAngular"],
        "_private.system_model.fe._2427": ["DegreeOfFreedomBoundaryConditionLinear"],
        "_private.system_model.fe._2428": ["ElectricMachineDataSet"],
        "_private.system_model.fe._2429": ["ElectricMachineDynamicLoadData"],
        "_private.system_model.fe._2430": ["ElementFaceGroupWithSelection"],
        "_private.system_model.fe._2431": ["ElementPropertiesWithSelection"],
        "_private.system_model.fe._2432": ["FEEntityGroupWithSelection"],
        "_private.system_model.fe._2433": ["FEExportSettings"],
        "_private.system_model.fe._2434": ["FEPartDRIVASurfaceSelection"],
        "_private.system_model.fe._2435": ["FEPartWithBatchOptions"],
        "_private.system_model.fe._2436": ["FEStiffnessGeometry"],
        "_private.system_model.fe._2437": ["FEStiffnessTester"],
        "_private.system_model.fe._2438": ["FESubstructure"],
        "_private.system_model.fe._2439": ["FESubstructureExportOptions"],
        "_private.system_model.fe._2440": ["FESubstructureNode"],
        "_private.system_model.fe._2441": ["FESubstructureNodeModeShape"],
        "_private.system_model.fe._2442": ["FESubstructureNodeModeShapes"],
        "_private.system_model.fe._2443": ["FESubstructureType"],
        "_private.system_model.fe._2444": ["FESubstructureWithBatchOptions"],
        "_private.system_model.fe._2445": ["FESubstructureWithSelection"],
        "_private.system_model.fe._2446": ["FESubstructureWithSelectionComponents"],
        "_private.system_model.fe._2447": [
            "FESubstructureWithSelectionForHarmonicAnalysis"
        ],
        "_private.system_model.fe._2448": [
            "FESubstructureWithSelectionForModalAnalysis"
        ],
        "_private.system_model.fe._2449": [
            "FESubstructureWithSelectionForStaticAnalysis"
        ],
        "_private.system_model.fe._2450": ["GearMeshingOptions"],
        "_private.system_model.fe._2451": ["IndependentMASTACreatedCondensationNode"],
        "_private.system_model.fe._2452": ["LinkComponentAxialPositionErrorReporter"],
        "_private.system_model.fe._2453": ["LinkNodeSource"],
        "_private.system_model.fe._2454": ["MaterialPropertiesWithSelection"],
        "_private.system_model.fe._2455": ["NodeBoundaryConditionStaticAnalysis"],
        "_private.system_model.fe._2456": ["NodeGroupWithSelection"],
        "_private.system_model.fe._2457": ["NodeSelectionDepthOption"],
        "_private.system_model.fe._2458": ["OptionsWhenExternalFEFileAlreadyExists"],
        "_private.system_model.fe._2459": ["PerLinkExportOptions"],
        "_private.system_model.fe._2460": ["PerNodeExportOptions"],
        "_private.system_model.fe._2461": ["RaceBearingFE"],
        "_private.system_model.fe._2462": ["RaceBearingFESystemDeflection"],
        "_private.system_model.fe._2463": ["RaceBearingFEWithSelection"],
        "_private.system_model.fe._2464": ["ReplacedShaftSelectionHelper"],
        "_private.system_model.fe._2465": ["SystemDeflectionFEExportOptions"],
        "_private.system_model.fe._2466": ["ThermalExpansionOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AlignConnectedComponentOptions",
    "AlignmentMethod",
    "AlignmentMethodForRaceBearing",
    "AlignmentUsingAxialNodePositions",
    "AngleSource",
    "BaseFEWithSelection",
    "BatchOperations",
    "BearingNodeAlignmentOption",
    "BearingNodeOption",
    "BearingRaceNodeLink",
    "BearingRacePosition",
    "ComponentOrientationOption",
    "ContactPairWithSelection",
    "CoordinateSystemWithSelection",
    "CreateConnectedComponentOptions",
    "CreateMicrophoneNormalToSurfaceOptions",
    "DegreeOfFreedomBoundaryCondition",
    "DegreeOfFreedomBoundaryConditionAngular",
    "DegreeOfFreedomBoundaryConditionLinear",
    "ElectricMachineDataSet",
    "ElectricMachineDynamicLoadData",
    "ElementFaceGroupWithSelection",
    "ElementPropertiesWithSelection",
    "FEEntityGroupWithSelection",
    "FEExportSettings",
    "FEPartDRIVASurfaceSelection",
    "FEPartWithBatchOptions",
    "FEStiffnessGeometry",
    "FEStiffnessTester",
    "FESubstructure",
    "FESubstructureExportOptions",
    "FESubstructureNode",
    "FESubstructureNodeModeShape",
    "FESubstructureNodeModeShapes",
    "FESubstructureType",
    "FESubstructureWithBatchOptions",
    "FESubstructureWithSelection",
    "FESubstructureWithSelectionComponents",
    "FESubstructureWithSelectionForHarmonicAnalysis",
    "FESubstructureWithSelectionForModalAnalysis",
    "FESubstructureWithSelectionForStaticAnalysis",
    "GearMeshingOptions",
    "IndependentMASTACreatedCondensationNode",
    "LinkComponentAxialPositionErrorReporter",
    "LinkNodeSource",
    "MaterialPropertiesWithSelection",
    "NodeBoundaryConditionStaticAnalysis",
    "NodeGroupWithSelection",
    "NodeSelectionDepthOption",
    "OptionsWhenExternalFEFileAlreadyExists",
    "PerLinkExportOptions",
    "PerNodeExportOptions",
    "RaceBearingFE",
    "RaceBearingFESystemDeflection",
    "RaceBearingFEWithSelection",
    "ReplacedShaftSelectionHelper",
    "SystemDeflectionFEExportOptions",
    "ThermalExpansionOption",
)
