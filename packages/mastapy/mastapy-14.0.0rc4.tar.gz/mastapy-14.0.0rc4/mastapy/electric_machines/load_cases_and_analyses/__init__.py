"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.load_cases_and_analyses._1394 import (
        BasicDynamicForceLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1395 import (
        DynamicForceAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1396 import (
        DynamicForceLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1397 import (
        DynamicForcesOperatingPoint,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1398 import (
        EfficiencyMapAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1399 import (
        EfficiencyMapLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1400 import (
        ElectricMachineAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1401 import (
        ElectricMachineBasicMechanicalLossSettings,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1402 import (
        ElectricMachineControlStrategy,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1403 import (
        ElectricMachineEfficiencyMapSettings,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1404 import (
        ElectricMachineFEAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1405 import (
        ElectricMachineFEMechanicalAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1406 import (
        ElectricMachineLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1407 import (
        ElectricMachineLoadCaseBase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1408 import (
        ElectricMachineLoadCaseGroup,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1409 import (
        ElectricMachineMechanicalLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1410 import (
        EndWindingInductanceMethod,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1411 import (
        LeadingOrLagging,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1412 import (
        LoadCaseType,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1413 import (
        LoadCaseTypeSelector,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1414 import (
        MotoringOrGenerating,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1415 import (
        NonLinearDQModelMultipleOperatingPointsLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1416 import (
        NumberOfStepsPerOperatingPointSpecificationMethod,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1417 import (
        OperatingPointsSpecificationMethod,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1418 import (
        SingleOperatingPointAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1419 import (
        SlotDetailForAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1420 import (
        SpecifyTorqueOrCurrent,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1421 import (
        SpeedPointsDistribution,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1422 import (
        SpeedTorqueCurveAnalysis,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1423 import (
        SpeedTorqueCurveLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1424 import (
        SpeedTorqueLoadCase,
    )
    from mastapy._private.electric_machines.load_cases_and_analyses._1425 import (
        Temperatures,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.load_cases_and_analyses._1394": [
            "BasicDynamicForceLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1395": [
            "DynamicForceAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1396": [
            "DynamicForceLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1397": [
            "DynamicForcesOperatingPoint"
        ],
        "_private.electric_machines.load_cases_and_analyses._1398": [
            "EfficiencyMapAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1399": [
            "EfficiencyMapLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1400": [
            "ElectricMachineAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1401": [
            "ElectricMachineBasicMechanicalLossSettings"
        ],
        "_private.electric_machines.load_cases_and_analyses._1402": [
            "ElectricMachineControlStrategy"
        ],
        "_private.electric_machines.load_cases_and_analyses._1403": [
            "ElectricMachineEfficiencyMapSettings"
        ],
        "_private.electric_machines.load_cases_and_analyses._1404": [
            "ElectricMachineFEAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1405": [
            "ElectricMachineFEMechanicalAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1406": [
            "ElectricMachineLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1407": [
            "ElectricMachineLoadCaseBase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1408": [
            "ElectricMachineLoadCaseGroup"
        ],
        "_private.electric_machines.load_cases_and_analyses._1409": [
            "ElectricMachineMechanicalLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1410": [
            "EndWindingInductanceMethod"
        ],
        "_private.electric_machines.load_cases_and_analyses._1411": [
            "LeadingOrLagging"
        ],
        "_private.electric_machines.load_cases_and_analyses._1412": ["LoadCaseType"],
        "_private.electric_machines.load_cases_and_analyses._1413": [
            "LoadCaseTypeSelector"
        ],
        "_private.electric_machines.load_cases_and_analyses._1414": [
            "MotoringOrGenerating"
        ],
        "_private.electric_machines.load_cases_and_analyses._1415": [
            "NonLinearDQModelMultipleOperatingPointsLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1416": [
            "NumberOfStepsPerOperatingPointSpecificationMethod"
        ],
        "_private.electric_machines.load_cases_and_analyses._1417": [
            "OperatingPointsSpecificationMethod"
        ],
        "_private.electric_machines.load_cases_and_analyses._1418": [
            "SingleOperatingPointAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1419": [
            "SlotDetailForAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1420": [
            "SpecifyTorqueOrCurrent"
        ],
        "_private.electric_machines.load_cases_and_analyses._1421": [
            "SpeedPointsDistribution"
        ],
        "_private.electric_machines.load_cases_and_analyses._1422": [
            "SpeedTorqueCurveAnalysis"
        ],
        "_private.electric_machines.load_cases_and_analyses._1423": [
            "SpeedTorqueCurveLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1424": [
            "SpeedTorqueLoadCase"
        ],
        "_private.electric_machines.load_cases_and_analyses._1425": ["Temperatures"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BasicDynamicForceLoadCase",
    "DynamicForceAnalysis",
    "DynamicForceLoadCase",
    "DynamicForcesOperatingPoint",
    "EfficiencyMapAnalysis",
    "EfficiencyMapLoadCase",
    "ElectricMachineAnalysis",
    "ElectricMachineBasicMechanicalLossSettings",
    "ElectricMachineControlStrategy",
    "ElectricMachineEfficiencyMapSettings",
    "ElectricMachineFEAnalysis",
    "ElectricMachineFEMechanicalAnalysis",
    "ElectricMachineLoadCase",
    "ElectricMachineLoadCaseBase",
    "ElectricMachineLoadCaseGroup",
    "ElectricMachineMechanicalLoadCase",
    "EndWindingInductanceMethod",
    "LeadingOrLagging",
    "LoadCaseType",
    "LoadCaseTypeSelector",
    "MotoringOrGenerating",
    "NonLinearDQModelMultipleOperatingPointsLoadCase",
    "NumberOfStepsPerOperatingPointSpecificationMethod",
    "OperatingPointsSpecificationMethod",
    "SingleOperatingPointAnalysis",
    "SlotDetailForAnalysis",
    "SpecifyTorqueOrCurrent",
    "SpeedPointsDistribution",
    "SpeedTorqueCurveAnalysis",
    "SpeedTorqueCurveLoadCase",
    "SpeedTorqueLoadCase",
    "Temperatures",
)
