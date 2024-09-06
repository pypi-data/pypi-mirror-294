"""KlingelnbergCycloPalloidConicalGearMesh"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2361

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidConicalGearMesh",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.connections_and_sockets import _2326, _2335
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2367,
        _2373,
        _2374,
    )

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearMesh")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMesh._Cast_KlingelnbergCycloPalloidConicalGearMesh",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMesh:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMesh to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMesh"

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2361.ConicalGearMesh":
        return self.__parent__._cast(_2361.ConicalGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2367.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2367

        return self.__parent__._cast(_2367.GearMesh)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2335.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2335

        return self.__parent__._cast(_2335.InterMountableComponentConnection)

    @property
    def connection(self: "CastSelf") -> "_2326.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2326

        return self.__parent__._cast(_2326.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2257.DesignEntity":
        from mastapy._private.system_model import _2257

        return self.__parent__._cast(_2257.DesignEntity)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2373.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2373

        return self.__parent__._cast(_2373.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2374.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2374

        return self.__parent__._cast(_2374.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMesh":
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
class KlingelnbergCycloPalloidConicalGearMesh(_2361.ConicalGearMesh):
    """KlingelnbergCycloPalloidConicalGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidConicalGearMesh":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMesh
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMesh(self)
