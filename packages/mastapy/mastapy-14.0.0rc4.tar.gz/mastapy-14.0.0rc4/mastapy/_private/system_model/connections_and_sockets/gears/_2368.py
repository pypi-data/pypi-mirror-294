"""GearTeethSocket"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets import _2350

_GEAR_TEETH_SOCKET = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearTeethSocket"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2354,
        _2356,
        _2358,
        _2360,
        _2362,
        _2366,
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

    Self = TypeVar("Self", bound="GearTeethSocket")
    CastSelf = TypeVar("CastSelf", bound="GearTeethSocket._Cast_GearTeethSocket")


__docformat__ = "restructuredtext en"
__all__ = ("GearTeethSocket",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearTeethSocket:
    """Special nested class for casting GearTeethSocket to subclasses."""

    __parent__: "GearTeethSocket"

    @property
    def socket(self: "CastSelf") -> "_2350.Socket":
        return self.__parent__._cast(_2350.Socket)

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
    def face_gear_teeth_socket(self: "CastSelf") -> "_2366.FaceGearTeethSocket":
        from mastapy._private.system_model.connections_and_sockets.gears import _2366

        return self.__parent__._cast(_2366.FaceGearTeethSocket)

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
    def gear_teeth_socket(self: "CastSelf") -> "GearTeethSocket":
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
class GearTeethSocket(_2350.Socket):
    """GearTeethSocket

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_TEETH_SOCKET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearTeethSocket":
        """Cast to another type.

        Returns:
            _Cast_GearTeethSocket
        """
        return _Cast_GearTeethSocket(self)
