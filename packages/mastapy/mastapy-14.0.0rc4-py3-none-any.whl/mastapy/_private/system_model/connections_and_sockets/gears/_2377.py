"""SpiralBevelGearMesh"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.connections_and_sockets.gears import _2357

_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "SpiralBevelGearMesh"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.spiral_bevel import _996
    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.connections_and_sockets import _2326, _2335
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2353,
        _2361,
        _2367,
    )

    Self = TypeVar("Self", bound="SpiralBevelGearMesh")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelGearMesh._Cast_SpiralBevelGearMesh"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearMesh",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearMesh:
    """Special nested class for casting SpiralBevelGearMesh to subclasses."""

    __parent__: "SpiralBevelGearMesh"

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2357.BevelGearMesh":
        return self.__parent__._cast(_2357.BevelGearMesh)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2353.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2353

        return self.__parent__._cast(_2353.AGMAGleasonConicalGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2361.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2361

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
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "SpiralBevelGearMesh":
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
class SpiralBevelGearMesh(_2357.BevelGearMesh):
    """SpiralBevelGearMesh

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_MESH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def bevel_gear_mesh_design(self: "Self") -> "_996.SpiralBevelGearMeshDesign":
        """mastapy.gears.gear_designs.spiral_bevel.SpiralBevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def spiral_bevel_gear_mesh_design(self: "Self") -> "_996.SpiralBevelGearMeshDesign":
        """mastapy.gears.gear_designs.spiral_bevel.SpiralBevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearMesh":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearMesh
        """
        return _Cast_SpiralBevelGearMesh(self)
