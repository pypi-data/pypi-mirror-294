"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.connections_and_sockets._2319 import (
        AbstractShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2320 import (
        BearingInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2321 import (
        BearingOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2322 import (
        BeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2323 import (
        CoaxialConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2324 import (
        ComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2325 import (
        ComponentMeasurer,
    )
    from mastapy._private.system_model.connections_and_sockets._2326 import Connection
    from mastapy._private.system_model.connections_and_sockets._2327 import (
        CVTBeltConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2328 import (
        CVTPulleySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2329 import (
        CylindricalComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2330 import (
        CylindricalSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2331 import (
        DatumMeasurement,
    )
    from mastapy._private.system_model.connections_and_sockets._2332 import (
        ElectricMachineStatorSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2333 import (
        InnerShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2334 import (
        InnerShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2335 import (
        InterMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2336 import (
        MountableComponentInnerSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2337 import (
        MountableComponentOuterSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2338 import (
        MountableComponentSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2339 import (
        OuterShaftSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2340 import (
        OuterShaftSocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2341 import (
        PlanetaryConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2342 import (
        PlanetarySocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2343 import (
        PlanetarySocketBase,
    )
    from mastapy._private.system_model.connections_and_sockets._2344 import PulleySocket
    from mastapy._private.system_model.connections_and_sockets._2345 import (
        RealignmentResult,
    )
    from mastapy._private.system_model.connections_and_sockets._2346 import (
        RollingRingConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2347 import (
        RollingRingSocket,
    )
    from mastapy._private.system_model.connections_and_sockets._2348 import ShaftSocket
    from mastapy._private.system_model.connections_and_sockets._2349 import (
        ShaftToMountableComponentConnection,
    )
    from mastapy._private.system_model.connections_and_sockets._2350 import Socket
    from mastapy._private.system_model.connections_and_sockets._2351 import (
        SocketConnectionOptions,
    )
    from mastapy._private.system_model.connections_and_sockets._2352 import (
        SocketConnectionSelection,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.connections_and_sockets._2319": [
            "AbstractShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2320": ["BearingInnerSocket"],
        "_private.system_model.connections_and_sockets._2321": ["BearingOuterSocket"],
        "_private.system_model.connections_and_sockets._2322": ["BeltConnection"],
        "_private.system_model.connections_and_sockets._2323": ["CoaxialConnection"],
        "_private.system_model.connections_and_sockets._2324": ["ComponentConnection"],
        "_private.system_model.connections_and_sockets._2325": ["ComponentMeasurer"],
        "_private.system_model.connections_and_sockets._2326": ["Connection"],
        "_private.system_model.connections_and_sockets._2327": ["CVTBeltConnection"],
        "_private.system_model.connections_and_sockets._2328": ["CVTPulleySocket"],
        "_private.system_model.connections_and_sockets._2329": [
            "CylindricalComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2330": ["CylindricalSocket"],
        "_private.system_model.connections_and_sockets._2331": ["DatumMeasurement"],
        "_private.system_model.connections_and_sockets._2332": [
            "ElectricMachineStatorSocket"
        ],
        "_private.system_model.connections_and_sockets._2333": ["InnerShaftSocket"],
        "_private.system_model.connections_and_sockets._2334": ["InnerShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2335": [
            "InterMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2336": [
            "MountableComponentInnerSocket"
        ],
        "_private.system_model.connections_and_sockets._2337": [
            "MountableComponentOuterSocket"
        ],
        "_private.system_model.connections_and_sockets._2338": [
            "MountableComponentSocket"
        ],
        "_private.system_model.connections_and_sockets._2339": ["OuterShaftSocket"],
        "_private.system_model.connections_and_sockets._2340": ["OuterShaftSocketBase"],
        "_private.system_model.connections_and_sockets._2341": ["PlanetaryConnection"],
        "_private.system_model.connections_and_sockets._2342": ["PlanetarySocket"],
        "_private.system_model.connections_and_sockets._2343": ["PlanetarySocketBase"],
        "_private.system_model.connections_and_sockets._2344": ["PulleySocket"],
        "_private.system_model.connections_and_sockets._2345": ["RealignmentResult"],
        "_private.system_model.connections_and_sockets._2346": [
            "RollingRingConnection"
        ],
        "_private.system_model.connections_and_sockets._2347": ["RollingRingSocket"],
        "_private.system_model.connections_and_sockets._2348": ["ShaftSocket"],
        "_private.system_model.connections_and_sockets._2349": [
            "ShaftToMountableComponentConnection"
        ],
        "_private.system_model.connections_and_sockets._2350": ["Socket"],
        "_private.system_model.connections_and_sockets._2351": [
            "SocketConnectionOptions"
        ],
        "_private.system_model.connections_and_sockets._2352": [
            "SocketConnectionSelection"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractShaftToMountableComponentConnection",
    "BearingInnerSocket",
    "BearingOuterSocket",
    "BeltConnection",
    "CoaxialConnection",
    "ComponentConnection",
    "ComponentMeasurer",
    "Connection",
    "CVTBeltConnection",
    "CVTPulleySocket",
    "CylindricalComponentConnection",
    "CylindricalSocket",
    "DatumMeasurement",
    "ElectricMachineStatorSocket",
    "InnerShaftSocket",
    "InnerShaftSocketBase",
    "InterMountableComponentConnection",
    "MountableComponentInnerSocket",
    "MountableComponentOuterSocket",
    "MountableComponentSocket",
    "OuterShaftSocket",
    "OuterShaftSocketBase",
    "PlanetaryConnection",
    "PlanetarySocket",
    "PlanetarySocketBase",
    "PulleySocket",
    "RealignmentResult",
    "RollingRingConnection",
    "RollingRingSocket",
    "ShaftSocket",
    "ShaftToMountableComponentConnection",
    "Socket",
    "SocketConnectionOptions",
    "SocketConnectionSelection",
)
