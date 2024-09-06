"""AGMAGleasonConicalGearMesh"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.connections_and_sockets.gears import _2361

_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "AGMAGleasonConicalGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.connections_and_sockets import _2326, _2335
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2355,
        _2357,
        _2367,
        _2369,
        _2377,
        _2379,
        _2381,
        _2385,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGearMesh._Cast_AGMAGleasonConicalGearMesh"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMesh:
    """Special nested class for casting AGMAGleasonConicalGearMesh to subclasses."""

    __parent__: "AGMAGleasonConicalGearMesh"

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
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2355.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2355

        return self.__parent__._cast(_2355.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2357.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2357

        return self.__parent__._cast(_2357.BevelGearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2369.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2369

        return self.__parent__._cast(_2369.HypoidGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2377.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2377

        return self.__parent__._cast(_2377.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2379.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2379

        return self.__parent__._cast(_2379.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2381.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2381

        return self.__parent__._cast(_2381.StraightBevelGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2385.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2385

        return self.__parent__._cast(_2385.ZerolBevelGearMesh)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMesh":
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
class AGMAGleasonConicalGearMesh(_2361.ConicalGearMesh):
    """AGMAGleasonConicalGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearMesh":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMesh
        """
        return _Cast_AGMAGleasonConicalGearMesh(self)
