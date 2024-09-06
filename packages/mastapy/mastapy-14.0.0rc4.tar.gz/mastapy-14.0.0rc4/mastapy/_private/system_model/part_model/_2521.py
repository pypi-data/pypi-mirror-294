"""MountableComponent"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2499

_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.connections_and_sockets import (
        _2323,
        _2326,
        _2330,
    )
    from mastapy._private.system_model.part_model import (
        _2490,
        _2494,
        _2500,
        _2502,
        _2517,
        _2518,
        _2523,
        _2525,
        _2526,
        _2528,
        _2529,
        _2534,
        _2536,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2637,
        _2640,
        _2643,
        _2646,
        _2648,
        _2650,
        _2656,
        _2658,
        _2664,
        _2667,
        _2668,
        _2669,
        _2671,
        _2673,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2627
    from mastapy._private.system_model.part_model.gears import (
        _2570,
        _2572,
        _2574,
        _2575,
        _2576,
        _2578,
        _2580,
        _2582,
        _2584,
        _2585,
        _2587,
        _2591,
        _2593,
        _2595,
        _2597,
        _2600,
        _2602,
        _2604,
        _2606,
        _2607,
        _2608,
        _2610,
    )

    Self = TypeVar("Self", bound="MountableComponent")
    CastSelf = TypeVar("CastSelf", bound="MountableComponent._Cast_MountableComponent")


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponent:
    """Special nested class for casting MountableComponent to subclasses."""

    __parent__: "MountableComponent"

    @property
    def component(self: "CastSelf") -> "_2499.Component":
        return self.__parent__._cast(_2499.Component)

    @property
    def part(self: "CastSelf") -> "_2525.Part":
        from mastapy._private.system_model.part_model import _2525

        return self.__parent__._cast(_2525.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2257.DesignEntity":
        from mastapy._private.system_model import _2257

        return self.__parent__._cast(_2257.DesignEntity)

    @property
    def bearing(self: "CastSelf") -> "_2494.Bearing":
        from mastapy._private.system_model.part_model import _2494

        return self.__parent__._cast(_2494.Bearing)

    @property
    def connector(self: "CastSelf") -> "_2502.Connector":
        from mastapy._private.system_model.part_model import _2502

        return self.__parent__._cast(_2502.Connector)

    @property
    def mass_disc(self: "CastSelf") -> "_2517.MassDisc":
        from mastapy._private.system_model.part_model import _2517

        return self.__parent__._cast(_2517.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2518.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2518

        return self.__parent__._cast(_2518.MeasurementComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2523.OilSeal":
        from mastapy._private.system_model.part_model import _2523

        return self.__parent__._cast(_2523.OilSeal)

    @property
    def planet_carrier(self: "CastSelf") -> "_2526.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2528.PointLoad":
        from mastapy._private.system_model.part_model import _2528

        return self.__parent__._cast(_2528.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2529.PowerLoad":
        from mastapy._private.system_model.part_model import _2529

        return self.__parent__._cast(_2529.PowerLoad)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2534.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2534

        return self.__parent__._cast(_2534.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2536.VirtualComponent":
        from mastapy._private.system_model.part_model import _2536

        return self.__parent__._cast(_2536.VirtualComponent)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2570.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2570

        return self.__parent__._cast(_2570.AGMAGleasonConicalGear)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2572.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2572

        return self.__parent__._cast(_2572.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2574.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2574

        return self.__parent__._cast(_2574.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2575.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2575

        return self.__parent__._cast(_2575.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2576.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2576

        return self.__parent__._cast(_2576.BevelGear)

    @property
    def concept_gear(self: "CastSelf") -> "_2578.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2578

        return self.__parent__._cast(_2578.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2580.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2580

        return self.__parent__._cast(_2580.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2582.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2584.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2584

        return self.__parent__._cast(_2584.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2585.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.FaceGear)

    @property
    def gear(self: "CastSelf") -> "_2587.Gear":
        from mastapy._private.system_model.part_model.gears import _2587

        return self.__parent__._cast(_2587.Gear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2591.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2593.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2593

        return self.__parent__._cast(_2593.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2595.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2597.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2600.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2600

        return self.__parent__._cast(_2600.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2602.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2602

        return self.__parent__._cast(_2602.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2604.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2606.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2607.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.StraightBevelSunGear)

    @property
    def worm_gear(self: "CastSelf") -> "_2608.WormGear":
        from mastapy._private.system_model.part_model.gears import _2608

        return self.__parent__._cast(_2608.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2610.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.ZerolBevelGear)

    @property
    def ring_pins(self: "CastSelf") -> "_2627.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2627

        return self.__parent__._cast(_2627.RingPins)

    @property
    def clutch_half(self: "CastSelf") -> "_2637.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2637

        return self.__parent__._cast(_2637.ClutchHalf)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2640.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2640

        return self.__parent__._cast(_2640.ConceptCouplingHalf)

    @property
    def coupling_half(self: "CastSelf") -> "_2643.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2643

        return self.__parent__._cast(_2643.CouplingHalf)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2646.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2646

        return self.__parent__._cast(_2646.CVTPulley)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2648.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2648

        return self.__parent__._cast(_2648.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2650.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2650

        return self.__parent__._cast(_2650.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2656.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2656

        return self.__parent__._cast(_2656.RollingRing)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2658.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2658

        return self.__parent__._cast(_2658.ShaftHubConnection)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2664.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2664

        return self.__parent__._cast(_2664.SpringDamperHalf)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2667.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2667

        return self.__parent__._cast(_2667.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2668.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2668

        return self.__parent__._cast(_2668.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2669.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2669

        return self.__parent__._cast(_2669.SynchroniserSleeve)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2671.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2671

        return self.__parent__._cast(_2671.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2673.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2673

        return self.__parent__._cast(_2673.TorqueConverterTurbine)

    @property
    def mountable_component(self: "CastSelf") -> "MountableComponent":
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
class MountableComponent(_2499.Component):
    """MountableComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTABLE_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def rotation_about_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAboutAxis")

        if temp is None:
            return 0.0

        return temp

    @rotation_about_axis.setter
    @enforce_parameter_types
    def rotation_about_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotationAboutAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_component(self: "Self") -> "_2490.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerComponent")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_connection(self: "Self") -> "_2326.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerConnection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_socket(self: "Self") -> "_2330.CylindricalSocket":
        """mastapy.system_model.connections_and_sockets.CylindricalSocket

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSocket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def is_mounted(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsMounted")

        if temp is None:
            return False

        return temp

    @enforce_parameter_types
    def mount_on(
        self: "Self", shaft: "_2490.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2323.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def try_mount_on(
        self: "Self", shaft: "_2490.AbstractShaft", offset: "float" = float("nan")
    ) -> "_2500.ComponentsConnectedResult":
        """mastapy.system_model.part_model.ComponentsConnectedResult

        Args:
            shaft (mastapy.system_model.part_model.AbstractShaft)
            offset (float, optional)
        """
        offset = float(offset)
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryMountOn",
            shaft.wrapped if shaft else None,
            offset if offset else 0.0,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_MountableComponent":
        """Cast to another type.

        Returns:
            _Cast_MountableComponent
        """
        return _Cast_MountableComponent(self)
