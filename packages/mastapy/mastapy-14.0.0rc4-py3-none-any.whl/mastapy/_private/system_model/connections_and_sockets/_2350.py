"""Socket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_SOCKET = python_net_import("SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Socket")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets import (
        _2320,
        _2321,
        _2326,
        _2328,
        _2330,
        _2332,
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
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2354,
        _2356,
        _2358,
        _2360,
        _2362,
        _2364,
        _2366,
        _2368,
        _2370,
        _2371,
        _2375,
        _2376,
        _2378,
        _2380,
        _2382,
        _2384,
        _2386,
    )
    from mastapy._private.system_model.part_model import _2499, _2500

    Self = TypeVar("Self", bound="Socket")
    CastSelf = TypeVar("CastSelf", bound="Socket._Cast_Socket")


__docformat__ = "restructuredtext en"
__all__ = ("Socket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Socket:
    """Special nested class for casting Socket to subclasses."""

    __parent__: "Socket"

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
    def cylindrical_socket(self: "CastSelf") -> "_2330.CylindricalSocket":
        from mastapy._private.system_model.connections_and_sockets import _2330

        return self.__parent__._cast(_2330.CylindricalSocket)

    @property
    def electric_machine_stator_socket(
        self: "CastSelf",
    ) -> "_2332.ElectricMachineStatorSocket":
        from mastapy._private.system_model.connections_and_sockets import _2332

        return self.__parent__._cast(_2332.ElectricMachineStatorSocket)

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
    def agma_gleason_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2354.AGMAGleasonConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2354

        return self.__parent__._cast(_2354.AGMAGleasonConicalGearTeethSocket)

    @property
    def bevel_differential_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2356.BevelDifferentialGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2356

        return self.__parent__._cast(_2356.BevelDifferentialGearTeethSocket)

    @property
    def bevel_gear_teeth_socket(self: "CastSelf") -> "_2358.BevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2358

        return self.__parent__._cast(_2358.BevelGearTeethSocket)

    @property
    def concept_gear_teeth_socket(self: "CastSelf") -> "_2360.ConceptGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2360

        return self.__parent__._cast(_2360.ConceptGearTeethSocket)

    @property
    def conical_gear_teeth_socket(self: "CastSelf") -> "_2362.ConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2362

        return self.__parent__._cast(_2362.ConicalGearTeethSocket)

    @property
    def cylindrical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2364.CylindricalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2364

        return self.__parent__._cast(_2364.CylindricalGearTeethSocket)

    @property
    def face_gear_teeth_socket(self: "CastSelf") -> "_2366.FaceGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2366

        return self.__parent__._cast(_2366.FaceGearTeethSocket)

    @property
    def gear_teeth_socket(self: "CastSelf") -> "_2368.GearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2368

        return self.__parent__._cast(_2368.GearTeethSocket)

    @property
    def hypoid_gear_teeth_socket(self: "CastSelf") -> "_2370.HypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2370

        return self.__parent__._cast(_2370.HypoidGearTeethSocket)

    @property
    def klingelnberg_conical_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2371.KlingelnbergConicalGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2371

        return self.__parent__._cast(_2371.KlingelnbergConicalGearTeethSocket)

    @property
    def klingelnberg_hypoid_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2375.KlingelnbergHypoidGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2375

        return self.__parent__._cast(_2375.KlingelnbergHypoidGearTeethSocket)

    @property
    def klingelnberg_spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2376.KlingelnbergSpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2376

        return self.__parent__._cast(_2376.KlingelnbergSpiralBevelGearTeethSocket)

    @property
    def spiral_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2378.SpiralBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2378

        return self.__parent__._cast(_2378.SpiralBevelGearTeethSocket)

    @property
    def straight_bevel_diff_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2380.StraightBevelDiffGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2380

        return self.__parent__._cast(_2380.StraightBevelDiffGearTeethSocket)

    @property
    def straight_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2382.StraightBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2382

        return self.__parent__._cast(_2382.StraightBevelGearTeethSocket)

    @property
    def worm_gear_teeth_socket(self: "CastSelf") -> "_2384.WormGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2384

        return self.__parent__._cast(_2384.WormGearTeethSocket)

    @property
    def zerol_bevel_gear_teeth_socket(
        self: "CastSelf",
    ) -> "_2386.ZerolBevelGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2386

        return self.__parent__._cast(_2386.ZerolBevelGearTeethSocket)

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
    def socket(self: "CastSelf") -> "Socket":
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
class Socket(_0.APIBase):
    """Socket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def connected_components(self: "Self") -> "List[_2499.Component]":
        """List[mastapy.system_model.part_model.Component]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connections(self: "Self") -> "List[_2326.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def owner(self: "Self") -> "_2499.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Owner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def connect_to(
        self: "Self", component: "_2499.Component"
    ) -> "_2500.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            component (mastapy.system_model.part_model.Component)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ConnectTo",
            [_COMPONENT],
            component.wrapped if component else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def connect_to_socket(
        self: "Self", socket: "Socket"
    ) -> "_2500.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call_overload(
            self.wrapped, "ConnectTo", [_SOCKET], socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def connection_to(self: "Self", socket: "Socket") -> "_2326.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Args:
            socket (mastapy.system_model.connections_and_sockets.Socket)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "ConnectionTo", socket.wrapped if socket else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def get_possible_sockets_to_connect_to(
        self: "Self", component_to_connect_to: "_2499.Component"
    ) -> "List[Socket]":
        """List[mastapy.system_model.connections_and_sockets.Socket]

        Args:
            component_to_connect_to (mastapy.system_model.part_model.Component)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped,
                "GetPossibleSocketsToConnectTo",
                component_to_connect_to.wrapped if component_to_connect_to else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Socket":
        """Cast to another type.

        Returns:
            _Cast_Socket
        """
        return _Cast_Socket(self)
