"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.scripting._7731 import ApiEnumForAttribute
    from mastapy._private.scripting._7732 import ApiVersion
    from mastapy._private.scripting._7733 import SMTBitmap
    from mastapy._private.scripting._7735 import MastaPropertyAttribute
    from mastapy._private.scripting._7736 import PythonCommand
    from mastapy._private.scripting._7737 import ScriptingCommand
    from mastapy._private.scripting._7738 import ScriptingExecutionCommand
    from mastapy._private.scripting._7739 import ScriptingObjectCommand
    from mastapy._private.scripting._7740 import ApiVersioning
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.scripting._7731": ["ApiEnumForAttribute"],
        "_private.scripting._7732": ["ApiVersion"],
        "_private.scripting._7733": ["SMTBitmap"],
        "_private.scripting._7735": ["MastaPropertyAttribute"],
        "_private.scripting._7736": ["PythonCommand"],
        "_private.scripting._7737": ["ScriptingCommand"],
        "_private.scripting._7738": ["ScriptingExecutionCommand"],
        "_private.scripting._7739": ["ScriptingObjectCommand"],
        "_private.scripting._7740": ["ApiVersioning"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ApiEnumForAttribute",
    "ApiVersion",
    "SMTBitmap",
    "MastaPropertyAttribute",
    "PythonCommand",
    "ScriptingCommand",
    "ScriptingExecutionCommand",
    "ScriptingObjectCommand",
    "ApiVersioning",
)
