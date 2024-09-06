"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.harmonic_load_data._1426 import (
        ElectricMachineHarmonicLoadDataBase,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1427 import (
        ForceDisplayOption,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1428 import (
        HarmonicLoadDataBase,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1429 import (
        HarmonicLoadDataControlExcitationOptionBase,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1430 import (
        HarmonicLoadDataType,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1431 import (
        SpeedDependentHarmonicLoadData,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1432 import (
        StatorToothInterpolator,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1433 import (
        StatorToothLoadInterpolator,
    )
    from mastapy._private.electric_machines.harmonic_load_data._1434 import (
        StatorToothMomentInterpolator,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.harmonic_load_data._1426": [
            "ElectricMachineHarmonicLoadDataBase"
        ],
        "_private.electric_machines.harmonic_load_data._1427": ["ForceDisplayOption"],
        "_private.electric_machines.harmonic_load_data._1428": ["HarmonicLoadDataBase"],
        "_private.electric_machines.harmonic_load_data._1429": [
            "HarmonicLoadDataControlExcitationOptionBase"
        ],
        "_private.electric_machines.harmonic_load_data._1430": ["HarmonicLoadDataType"],
        "_private.electric_machines.harmonic_load_data._1431": [
            "SpeedDependentHarmonicLoadData"
        ],
        "_private.electric_machines.harmonic_load_data._1432": [
            "StatorToothInterpolator"
        ],
        "_private.electric_machines.harmonic_load_data._1433": [
            "StatorToothLoadInterpolator"
        ],
        "_private.electric_machines.harmonic_load_data._1434": [
            "StatorToothMomentInterpolator"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ElectricMachineHarmonicLoadDataBase",
    "ForceDisplayOption",
    "HarmonicLoadDataBase",
    "HarmonicLoadDataControlExcitationOptionBase",
    "HarmonicLoadDataType",
    "SpeedDependentHarmonicLoadData",
    "StatorToothInterpolator",
    "StatorToothLoadInterpolator",
    "StatorToothMomentInterpolator",
)
