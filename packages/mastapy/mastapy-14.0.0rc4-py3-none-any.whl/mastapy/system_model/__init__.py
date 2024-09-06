"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model._2254 import Design
    from mastapy._private.system_model._2255 import ComponentDampingOption
    from mastapy._private.system_model._2256 import (
        ConceptCouplingSpeedRatioSpecificationMethod,
    )
    from mastapy._private.system_model._2257 import DesignEntity
    from mastapy._private.system_model._2258 import DesignEntityId
    from mastapy._private.system_model._2259 import DesignSettings
    from mastapy._private.system_model._2260 import DutyCycleImporter
    from mastapy._private.system_model._2261 import DutyCycleImporterDesignEntityMatch
    from mastapy._private.system_model._2262 import ExternalFullFELoader
    from mastapy._private.system_model._2263 import HypoidWindUpRemovalMethod
    from mastapy._private.system_model._2264 import IncludeDutyCycleOption
    from mastapy._private.system_model._2265 import MAAElectricMachineGroup
    from mastapy._private.system_model._2266 import MASTASettings
    from mastapy._private.system_model._2267 import MemorySummary
    from mastapy._private.system_model._2268 import MeshStiffnessModel
    from mastapy._private.system_model._2269 import (
        PlanetPinManufacturingErrorsCoordinateSystem,
    )
    from mastapy._private.system_model._2270 import (
        PowerLoadDragTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2271 import (
        PowerLoadInputTorqueSpecificationMethod,
    )
    from mastapy._private.system_model._2272 import PowerLoadPIDControlSpeedInputType
    from mastapy._private.system_model._2273 import PowerLoadType
    from mastapy._private.system_model._2274 import RelativeComponentAlignment
    from mastapy._private.system_model._2275 import RelativeOffsetOption
    from mastapy._private.system_model._2276 import SystemReporting
    from mastapy._private.system_model._2277 import (
        ThermalExpansionOptionForGroundedNodes,
    )
    from mastapy._private.system_model._2278 import TransmissionTemperatureSet
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model._2254": ["Design"],
        "_private.system_model._2255": ["ComponentDampingOption"],
        "_private.system_model._2256": ["ConceptCouplingSpeedRatioSpecificationMethod"],
        "_private.system_model._2257": ["DesignEntity"],
        "_private.system_model._2258": ["DesignEntityId"],
        "_private.system_model._2259": ["DesignSettings"],
        "_private.system_model._2260": ["DutyCycleImporter"],
        "_private.system_model._2261": ["DutyCycleImporterDesignEntityMatch"],
        "_private.system_model._2262": ["ExternalFullFELoader"],
        "_private.system_model._2263": ["HypoidWindUpRemovalMethod"],
        "_private.system_model._2264": ["IncludeDutyCycleOption"],
        "_private.system_model._2265": ["MAAElectricMachineGroup"],
        "_private.system_model._2266": ["MASTASettings"],
        "_private.system_model._2267": ["MemorySummary"],
        "_private.system_model._2268": ["MeshStiffnessModel"],
        "_private.system_model._2269": ["PlanetPinManufacturingErrorsCoordinateSystem"],
        "_private.system_model._2270": ["PowerLoadDragTorqueSpecificationMethod"],
        "_private.system_model._2271": ["PowerLoadInputTorqueSpecificationMethod"],
        "_private.system_model._2272": ["PowerLoadPIDControlSpeedInputType"],
        "_private.system_model._2273": ["PowerLoadType"],
        "_private.system_model._2274": ["RelativeComponentAlignment"],
        "_private.system_model._2275": ["RelativeOffsetOption"],
        "_private.system_model._2276": ["SystemReporting"],
        "_private.system_model._2277": ["ThermalExpansionOptionForGroundedNodes"],
        "_private.system_model._2278": ["TransmissionTemperatureSet"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Design",
    "ComponentDampingOption",
    "ConceptCouplingSpeedRatioSpecificationMethod",
    "DesignEntity",
    "DesignEntityId",
    "DesignSettings",
    "DutyCycleImporter",
    "DutyCycleImporterDesignEntityMatch",
    "ExternalFullFELoader",
    "HypoidWindUpRemovalMethod",
    "IncludeDutyCycleOption",
    "MAAElectricMachineGroup",
    "MASTASettings",
    "MemorySummary",
    "MeshStiffnessModel",
    "PlanetPinManufacturingErrorsCoordinateSystem",
    "PowerLoadDragTorqueSpecificationMethod",
    "PowerLoadInputTorqueSpecificationMethod",
    "PowerLoadPIDControlSpeedInputType",
    "PowerLoadType",
    "RelativeComponentAlignment",
    "RelativeOffsetOption",
    "SystemReporting",
    "ThermalExpansionOptionForGroundedNodes",
    "TransmissionTemperatureSet",
)
