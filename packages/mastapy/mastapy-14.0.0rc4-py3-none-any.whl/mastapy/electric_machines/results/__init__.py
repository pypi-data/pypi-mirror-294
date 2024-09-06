"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.results._1369 import DynamicForceResults
    from mastapy._private.electric_machines.results._1370 import EfficiencyResults
    from mastapy._private.electric_machines.results._1371 import ElectricMachineDQModel
    from mastapy._private.electric_machines.results._1372 import (
        ElectricMachineMechanicalResults,
    )
    from mastapy._private.electric_machines.results._1373 import (
        ElectricMachineMechanicalResultsViewable,
    )
    from mastapy._private.electric_machines.results._1374 import ElectricMachineResults
    from mastapy._private.electric_machines.results._1375 import (
        ElectricMachineResultsForConductorTurn,
    )
    from mastapy._private.electric_machines.results._1376 import (
        ElectricMachineResultsForConductorTurnAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1377 import (
        ElectricMachineResultsForLineToLine,
    )
    from mastapy._private.electric_machines.results._1378 import (
        ElectricMachineResultsForOpenCircuitAndOnLoad,
    )
    from mastapy._private.electric_machines.results._1379 import (
        ElectricMachineResultsForPhase,
    )
    from mastapy._private.electric_machines.results._1380 import (
        ElectricMachineResultsForPhaseAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1381 import (
        ElectricMachineResultsForStatorToothAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1382 import (
        ElectricMachineResultsLineToLineAtTimeStep,
    )
    from mastapy._private.electric_machines.results._1383 import (
        ElectricMachineResultsTimeStep,
    )
    from mastapy._private.electric_machines.results._1384 import (
        ElectricMachineResultsTimeStepAtLocation,
    )
    from mastapy._private.electric_machines.results._1385 import (
        ElectricMachineResultsViewable,
    )
    from mastapy._private.electric_machines.results._1386 import (
        ElectricMachineForceViewOptions,
    )
    from mastapy._private.electric_machines.results._1388 import LinearDQModel
    from mastapy._private.electric_machines.results._1389 import (
        MaximumTorqueResultsPoints,
    )
    from mastapy._private.electric_machines.results._1390 import NonLinearDQModel
    from mastapy._private.electric_machines.results._1391 import (
        NonLinearDQModelGeneratorSettings,
    )
    from mastapy._private.electric_machines.results._1392 import (
        OnLoadElectricMachineResults,
    )
    from mastapy._private.electric_machines.results._1393 import (
        OpenCircuitElectricMachineResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.results._1369": ["DynamicForceResults"],
        "_private.electric_machines.results._1370": ["EfficiencyResults"],
        "_private.electric_machines.results._1371": ["ElectricMachineDQModel"],
        "_private.electric_machines.results._1372": [
            "ElectricMachineMechanicalResults"
        ],
        "_private.electric_machines.results._1373": [
            "ElectricMachineMechanicalResultsViewable"
        ],
        "_private.electric_machines.results._1374": ["ElectricMachineResults"],
        "_private.electric_machines.results._1375": [
            "ElectricMachineResultsForConductorTurn"
        ],
        "_private.electric_machines.results._1376": [
            "ElectricMachineResultsForConductorTurnAtTimeStep"
        ],
        "_private.electric_machines.results._1377": [
            "ElectricMachineResultsForLineToLine"
        ],
        "_private.electric_machines.results._1378": [
            "ElectricMachineResultsForOpenCircuitAndOnLoad"
        ],
        "_private.electric_machines.results._1379": ["ElectricMachineResultsForPhase"],
        "_private.electric_machines.results._1380": [
            "ElectricMachineResultsForPhaseAtTimeStep"
        ],
        "_private.electric_machines.results._1381": [
            "ElectricMachineResultsForStatorToothAtTimeStep"
        ],
        "_private.electric_machines.results._1382": [
            "ElectricMachineResultsLineToLineAtTimeStep"
        ],
        "_private.electric_machines.results._1383": ["ElectricMachineResultsTimeStep"],
        "_private.electric_machines.results._1384": [
            "ElectricMachineResultsTimeStepAtLocation"
        ],
        "_private.electric_machines.results._1385": ["ElectricMachineResultsViewable"],
        "_private.electric_machines.results._1386": ["ElectricMachineForceViewOptions"],
        "_private.electric_machines.results._1388": ["LinearDQModel"],
        "_private.electric_machines.results._1389": ["MaximumTorqueResultsPoints"],
        "_private.electric_machines.results._1390": ["NonLinearDQModel"],
        "_private.electric_machines.results._1391": [
            "NonLinearDQModelGeneratorSettings"
        ],
        "_private.electric_machines.results._1392": ["OnLoadElectricMachineResults"],
        "_private.electric_machines.results._1393": [
            "OpenCircuitElectricMachineResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DynamicForceResults",
    "EfficiencyResults",
    "ElectricMachineDQModel",
    "ElectricMachineMechanicalResults",
    "ElectricMachineMechanicalResultsViewable",
    "ElectricMachineResults",
    "ElectricMachineResultsForConductorTurn",
    "ElectricMachineResultsForConductorTurnAtTimeStep",
    "ElectricMachineResultsForLineToLine",
    "ElectricMachineResultsForOpenCircuitAndOnLoad",
    "ElectricMachineResultsForPhase",
    "ElectricMachineResultsForPhaseAtTimeStep",
    "ElectricMachineResultsForStatorToothAtTimeStep",
    "ElectricMachineResultsLineToLineAtTimeStep",
    "ElectricMachineResultsTimeStep",
    "ElectricMachineResultsTimeStepAtLocation",
    "ElectricMachineResultsViewable",
    "ElectricMachineForceViewOptions",
    "LinearDQModel",
    "MaximumTorqueResultsPoints",
    "NonLinearDQModel",
    "NonLinearDQModelGeneratorSettings",
    "OnLoadElectricMachineResults",
    "OpenCircuitElectricMachineResults",
)
