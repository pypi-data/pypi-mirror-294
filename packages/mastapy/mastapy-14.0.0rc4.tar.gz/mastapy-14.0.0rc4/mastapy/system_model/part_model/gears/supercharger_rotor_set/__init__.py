"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2612 import (
        BoostPressureInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2613 import (
        InputPowerInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2614 import (
        PressureRatioInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2615 import (
        RotorSetDataInputFileOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2616 import (
        RotorSetMeasuredPoint,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2617 import (
        RotorSpeedInputOptions,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2618 import (
        SuperchargerMap,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2619 import (
        SuperchargerMaps,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2620 import (
        SuperchargerRotorSet,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2621 import (
        SuperchargerRotorSetDatabase,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set._2622 import (
        YVariableForImportedData,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.gears.supercharger_rotor_set._2612": [
            "BoostPressureInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2613": [
            "InputPowerInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2614": [
            "PressureRatioInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2615": [
            "RotorSetDataInputFileOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2616": [
            "RotorSetMeasuredPoint"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2617": [
            "RotorSpeedInputOptions"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2618": [
            "SuperchargerMap"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2619": [
            "SuperchargerMaps"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2620": [
            "SuperchargerRotorSet"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2621": [
            "SuperchargerRotorSetDatabase"
        ],
        "_private.system_model.part_model.gears.supercharger_rotor_set._2622": [
            "YVariableForImportedData"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BoostPressureInputOptions",
    "InputPowerInputOptions",
    "PressureRatioInputOptions",
    "RotorSetDataInputFileOptions",
    "RotorSetMeasuredPoint",
    "RotorSpeedInputOptions",
    "SuperchargerMap",
    "SuperchargerMaps",
    "SuperchargerRotorSet",
    "SuperchargerRotorSetDatabase",
    "YVariableForImportedData",
)
