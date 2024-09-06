"""CylindricalSocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2350

_CYLINDRICAL_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CylindricalSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2320,
        _2321,
        _2328,
        _2333,
        _2334,
        _2336,
        _2337,
        _2338,
        _2339,
        _2340,
        _2342,
        _2343,
        _2344,
        _2347,
        _2348,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2397,
        _2399,
        _2401,
        _2403,
        _2405,
        _2407,
        _2408,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2387,
        _2388,
        _2390,
        _2391,
        _2393,
        _2394,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2364

    Self = TypeVar("Self", bound="CylindricalSocket")
    CastSelf = TypeVar("CastSelf", bound="CylindricalSocket._Cast_CylindricalSocket")


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalSocket:
    """Special nested class for casting CylindricalSocket to subclasses."""

    __parent__: "CylindricalSocket"

    @property
    def socket(self: "CastSelf") -> "_2350.Socket":
        return self.__parent__._cast(_2350.Socket)

    @property
    def bearing_inner_socket(self: "CastSelf") -> "_2320.BearingInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2320

        return self.__parent__._cast(_2320.BearingInnerSocket)

    @property
    def bearing_outer_socket(self: "CastSelf") -> "_2321.BearingOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2321

        return self.__parent__._cast(_2321.BearingOuterSocket)

    @property
    def cvt_pulley_socket(self: "CastSelf") -> "_2328.CVTPulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2328

        return self.__parent__._cast(_2328.CVTPulleySocket)

    @property
    def inner_shaft_socket(self: "CastSelf") -> "_2333.InnerShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2333

        return self.__parent__._cast(_2333.InnerShaftSocket)

    @property
    def inner_shaft_socket_base(self: "CastSelf") -> "_2334.InnerShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2334

        return self.__parent__._cast(_2334.InnerShaftSocketBase)

    @property
    def mountable_component_inner_socket(
        self: "CastSelf",
    ) -> "_2336.MountableComponentInnerSocket":
        from mastapy._private.system_model.connections_and_sockets import _2336

        return self.__parent__._cast(_2336.MountableComponentInnerSocket)

    @property
    def mountable_component_outer_socket(
        self: "CastSelf",
    ) -> "_2337.MountableComponentOuterSocket":
        from mastapy._private.system_model.connections_and_sockets import _2337

        return self.__parent__._cast(_2337.MountableComponentOuterSocket)

    @property
    def mountable_component_socket(
        self: "CastSelf",
    ) -> "_2338.MountableComponentSocket":
        from mastapy._private.system_model.connections_and_sockets import _2338

        return self.__parent__._cast(_2338.MountableComponentSocket)

    @property
    def outer_shaft_socket(self: "CastSelf") -> "_2339.OuterShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2339

        return self.__parent__._cast(_2339.OuterShaftSocket)

    @property
    def outer_shaft_socket_base(self: "CastSelf") -> "_2340.OuterShaftSocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2340

        return self.__parent__._cast(_2340.OuterShaftSocketBase)

    @property
    def planetary_socket(self: "CastSelf") -> "_2342.PlanetarySocket":
        from mastapy._private.system_model.connections_and_sockets import _2342

        return self.__parent__._cast(_2342.PlanetarySocket)

    @property
    def planetary_socket_base(self: "CastSelf") -> "_2343.PlanetarySocketBase":
        from mastapy._private.system_model.connections_and_sockets import _2343

        return self.__parent__._cast(_2343.PlanetarySocketBase)

    @property
    def pulley_socket(self: "CastSelf") -> "_2344.PulleySocket":
        from mastapy._private.system_model.connections_and_sockets import _2344

        return self.__parent__._cast(_2344.PulleySocket)

    @property
    def rolling_ring_socket(self: "CastSelf") -> "_2347.RollingRingSocket":
        from mastapy._private.system_model.connections_and_sockets import _2347

        return self.__parent__._cast(_2347.RollingRingSocket)

    @property
    def shaft_socket(self: "CastSelf") -> "_2348.ShaftSocket":
        from mastapy._private.system_model.connections_and_sockets import _2348

        return self.__parent__._cast(_2348.ShaftSocket)

    @property
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2364.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2364

        return self.__parent__._cast(_2364.CylindricalGearTeethSocket)

    @property
    def cycloidal_disc_axial_left_socket(
        self: "CastSelf",
    ) -> "_2387.CycloidalDiscAxialLeftSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2387,
        )

        return self.__parent__._cast(_2387.CycloidalDiscAxialLeftSocket)

    @property
    def cycloidal_disc_axial_right_socket(
        self: "CastSelf",
    ) -> "_2388.CycloidalDiscAxialRightSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2388,
        )

        return self.__parent__._cast(_2388.CycloidalDiscAxialRightSocket)

    @property
    def cycloidal_disc_inner_socket(
        self: "CastSelf",
    ) -> "_2390.CycloidalDiscInnerSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2390,
        )

        return self.__parent__._cast(_2390.CycloidalDiscInnerSocket)

    @property
    def cycloidal_disc_outer_socket(
        self: "CastSelf",
    ) -> "_2391.CycloidalDiscOuterSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2391,
        )

        return self.__parent__._cast(_2391.CycloidalDiscOuterSocket)

    @property
    def cycloidal_disc_planetary_bearing_socket(
        self: "CastSelf",
    ) -> "_2393.CycloidalDiscPlanetaryBearingSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2393,
        )

        return self.__parent__._cast(_2393.CycloidalDiscPlanetaryBearingSocket)

    @property
    def ring_pins_socket(self: "CastSelf") -> "_2394.RingPinsSocket":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2394,
        )

        return self.__parent__._cast(_2394.RingPinsSocket)

    @property
    def clutch_socket(self: "CastSelf") -> "_2397.ClutchSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2397,
        )

        return self.__parent__._cast(_2397.ClutchSocket)

    @property
    def concept_coupling_socket(self: "CastSelf") -> "_2399.ConceptCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2399,
        )

        return self.__parent__._cast(_2399.ConceptCouplingSocket)

    @property
    def coupling_socket(self: "CastSelf") -> "_2401.CouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2401,
        )

        return self.__parent__._cast(_2401.CouplingSocket)

    @property
    def part_to_part_shear_coupling_socket(
        self: "CastSelf",
    ) -> "_2403.PartToPartShearCouplingSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2403,
        )

        return self.__parent__._cast(_2403.PartToPartShearCouplingSocket)

    @property
    def spring_damper_socket(self: "CastSelf") -> "_2405.SpringDamperSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2405,
        )

        return self.__parent__._cast(_2405.SpringDamperSocket)

    @property
    def torque_converter_pump_socket(
        self: "CastSelf",
    ) -> "_2407.TorqueConverterPumpSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2407,
        )

        return self.__parent__._cast(_2407.TorqueConverterPumpSocket)

    @property
    def torque_converter_turbine_socket(
        self: "CastSelf",
    ) -> "_2408.TorqueConverterTurbineSocket":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2408,
        )

        return self.__parent__._cast(_2408.TorqueConverterTurbineSocket)

    @property
    def cylindrical_socket(self: "CastSelf") -> "CylindricalSocket":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class CylindricalSocket(_2350.Socket):
    """CylindricalSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalSocket":
        """Cast to another type.

        Returns:
            _Cast_CylindricalSocket
        """
        return _Cast_CylindricalSocket(self)
