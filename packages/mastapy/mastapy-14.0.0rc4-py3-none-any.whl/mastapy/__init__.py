"""Root of the mastapy package."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private._0 import APIBase
    from mastapy._private._1 import Initialiser
    from mastapy._private._2 import LegacyV2RuntimeActivationPolicyAttributeSetter
    from mastapy._private._3 import PythonUtility
    from mastapy._private._4 import UtilityMethods
    from mastapy._private._5 import Versioning
    from mastapy._private._7721 import ConsoleProgress
    from mastapy._private._7722 import MarshalByRefObjectPermanent
    from mastapy._private._7723 import MarshalByRefObjects
    from mastapy._private._7724 import EnvironmentVariableUtility
    from mastapy._private._7725 import Remoting
    from mastapy._private._7726 import ScriptedPropertyNameAttribute
    from mastapy._private._7727 import SimpleTaskProgress
    from mastapy._private._7728 import TaskProgress
    from mastapy._private._internal import (
        __api_version__,
        __version__,
        AssemblyLoadError,
        CastException,
        DebugEnvironment,
        Examples,
        init,
        masta_after,
        masta_before,
        masta_licences,
        masta_property,
        MastaInitException,
        MastaPropertyException,
        MastaPropertyTypeException,
        MastapyImportException,
        MeasurementType,
        overridable,
        start_debugging,
        TupleWithName,
        TypeCheckException,
        UnavailableMethodError,
    )
    from mastapy._private._math import (
        approximately_equal,
        clamp,
        Color,
        fract,
        Long,
        Matrix2x2,
        Matrix3x3,
        Matrix4x4,
        MatrixException,
        sign,
        smoothstep,
        step,
        Vector2D,
        Vector3D,
        Vector4D,
        VectorException,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private._internal": [
            "DebugEnvironment",
            "MastaInitException",
            "MastaPropertyException",
            "MastaPropertyTypeException",
            "masta_property",
            "masta_before",
            "masta_after",
            "init",
            "start_debugging",
            "__version__",
            "__api_version__",
            "TupleWithName",
            "CastException",
            "MastapyImportException",
            "overridable",
            "MeasurementType",
            "TypeCheckException",
            "masta_licences",
            "AssemblyLoadError",
            "UnavailableMethodError",
            "Examples",
        ],
        "_private._math": [
            "clamp",
            "sign",
            "fract",
            "step",
            "smoothstep",
            "approximately_equal",
            "Long",
            "Vector2D",
            "Vector3D",
            "Vector4D",
            "Color",
            "VectorException",
            "Matrix2x2",
            "Matrix3x3",
            "Matrix4x4",
            "MatrixException",
        ],
        "_private._0": ["APIBase"],
        "_private._1": ["Initialiser"],
        "_private._2": ["LegacyV2RuntimeActivationPolicyAttributeSetter"],
        "_private._3": ["PythonUtility"],
        "_private._4": ["UtilityMethods"],
        "_private._5": ["Versioning"],
        "_private._7721": ["ConsoleProgress"],
        "_private._7722": ["MarshalByRefObjectPermanent"],
        "_private._7723": ["MarshalByRefObjects"],
        "_private._7724": ["EnvironmentVariableUtility"],
        "_private._7725": ["Remoting"],
        "_private._7726": ["ScriptedPropertyNameAttribute"],
        "_private._7727": ["SimpleTaskProgress"],
        "_private._7728": ["TaskProgress"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

    from mastapy._private._internal import mastafile_hook as __mh

    __mh()


__all__ = (
    "DebugEnvironment",
    "MastaInitException",
    "MastaPropertyException",
    "MastaPropertyTypeException",
    "masta_property",
    "masta_before",
    "masta_after",
    "init",
    "start_debugging",
    "__version__",
    "__api_version__",
    "TupleWithName",
    "CastException",
    "MastapyImportException",
    "overridable",
    "MeasurementType",
    "TypeCheckException",
    "masta_licences",
    "AssemblyLoadError",
    "UnavailableMethodError",
    "Examples",
    "clamp",
    "sign",
    "fract",
    "step",
    "smoothstep",
    "approximately_equal",
    "Long",
    "Vector2D",
    "Vector3D",
    "Vector4D",
    "Color",
    "VectorException",
    "Matrix2x2",
    "Matrix3x3",
    "Matrix4x4",
    "MatrixException",
    "APIBase",
    "Initialiser",
    "LegacyV2RuntimeActivationPolicyAttributeSetter",
    "PythonUtility",
    "UtilityMethods",
    "Versioning",
    "ConsoleProgress",
    "MarshalByRefObjectPermanent",
    "MarshalByRefObjects",
    "EnvironmentVariableUtility",
    "Remoting",
    "ScriptedPropertyNameAttribute",
    "SimpleTaskProgress",
    "TaskProgress",
)
