"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4130 import (
        RotorDynamicsDrawStyle,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4131 import (
        ShaftComplexShape,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4132 import (
        ShaftForcedComplexShape,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4133 import (
        ShaftModalComplexShape,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4134 import (
        ShaftModalComplexShapeAtSpeeds,
    )
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics._4135 import (
        ShaftModalComplexShapeAtStiffness,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.rotor_dynamics._4130": [
            "RotorDynamicsDrawStyle"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4131": [
            "ShaftComplexShape"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4132": [
            "ShaftForcedComplexShape"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4133": [
            "ShaftModalComplexShape"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4134": [
            "ShaftModalComplexShapeAtSpeeds"
        ],
        "_private.system_model.analyses_and_results.rotor_dynamics._4135": [
            "ShaftModalComplexShapeAtStiffness"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "RotorDynamicsDrawStyle",
    "ShaftComplexShape",
    "ShaftForcedComplexShape",
    "ShaftModalComplexShape",
    "ShaftModalComplexShapeAtSpeeds",
    "ShaftModalComplexShapeAtStiffness",
)
