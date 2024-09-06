"""InterMountableComponentConnection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.connections_and_sockets import _2326

_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "InterMountableComponentConnection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.connections_and_sockets import (
        _2322,
        _2327,
        _2346,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2396,
        _2398,
        _2400,
        _2402,
        _2404,
        _2406,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2395
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2353,
        _2355,
        _2357,
        _2359,
        _2361,
        _2363,
        _2365,
        _2367,
        _2369,
        _2372,
        _2373,
        _2374,
        _2377,
        _2379,
        _2381,
        _2383,
        _2385,
    )

    Self = TypeVar("Self", bound="InterMountableComponentConnection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnection._Cast_InterMountableComponentConnection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnection:
    """Special nested class for casting InterMountableComponentConnection to subclasses."""

    __parent__: "InterMountableComponentConnection"

    @property
    def connection(self: "CastSelf") -> "_2326.Connection":
        return self.__parent__._cast(_2326.Connection)

    @property
    def design_entity(self: "CastSelf") -> "_2257.DesignEntity":
        from mastapy._private.system_model import _2257

        return self.__parent__._cast(_2257.DesignEntity)

    @property
    def belt_connection(self: "CastSelf") -> "_2322.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2322

        return self.__parent__._cast(_2322.BeltConnection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2327.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2327

        return self.__parent__._cast(_2327.CVTBeltConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2346.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2346

        return self.__parent__._cast(_2346.RollingRingConnection)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2353.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2353

        return self.__parent__._cast(_2353.AGMAGleasonConicalGearMesh)

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
    def concept_gear_mesh(self: "CastSelf") -> "_2359.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2359

        return self.__parent__._cast(_2359.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2361.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2361

        return self.__parent__._cast(_2361.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2363.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2363

        return self.__parent__._cast(_2363.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2365.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2365

        return self.__parent__._cast(_2365.FaceGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2367.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2367

        return self.__parent__._cast(_2367.GearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2369.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2369

        return self.__parent__._cast(_2369.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2372.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2372

        return self.__parent__._cast(_2372.KlingelnbergCycloPalloidConicalGearMesh)

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
    def worm_gear_mesh(self: "CastSelf") -> "_2383.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2383

        return self.__parent__._cast(_2383.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2385.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2385

        return self.__parent__._cast(_2385.ZerolBevelGearMesh)

    @property
    def ring_pins_to_disc_connection(
        self: "CastSelf",
    ) -> "_2395.RingPinsToDiscConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2395,
        )

        return self.__parent__._cast(_2395.RingPinsToDiscConnection)

    @property
    def clutch_connection(self: "CastSelf") -> "_2396.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2396,
        )

        return self.__parent__._cast(_2396.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2398.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2398,
        )

        return self.__parent__._cast(_2398.ConceptCouplingConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "_2400.CouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2400,
        )

        return self.__parent__._cast(_2400.CouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2402.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2402,
        )

        return self.__parent__._cast(_2402.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2404.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2404,
        )

        return self.__parent__._cast(_2404.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2406.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2406,
        )

        return self.__parent__._cast(_2406.TorqueConverterConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "InterMountableComponentConnection":
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
class InterMountableComponentConnection(_2326.Connection):
    """InterMountableComponentConnection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def additional_modal_damping_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalModalDampingRatio")

        if temp is None:
            return 0.0

        return temp

    @additional_modal_damping_ratio.setter
    @enforce_parameter_types
    def additional_modal_damping_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AdditionalModalDampingRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_InterMountableComponentConnection":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnection
        """
        return _Cast_InterMountableComponentConnection(self)
