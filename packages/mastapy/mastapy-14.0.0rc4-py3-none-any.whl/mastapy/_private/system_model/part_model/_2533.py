"""SpecialisedAssembly"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2489

_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2257
    from mastapy._private.system_model.part_model import _2498, _2509, _2520, _2525
    from mastapy._private.system_model.part_model.couplings import (
        _2634,
        _2636,
        _2639,
        _2642,
        _2645,
        _2647,
        _2657,
        _2663,
        _2665,
        _2670,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2625
    from mastapy._private.system_model.part_model.gears import (
        _2571,
        _2573,
        _2577,
        _2579,
        _2581,
        _2583,
        _2586,
        _2589,
        _2592,
        _2594,
        _2596,
        _2598,
        _2599,
        _2601,
        _2603,
        _2605,
        _2609,
        _2611,
    )

    Self = TypeVar("Self", bound="SpecialisedAssembly")
    CastSelf = TypeVar(
        "CastSelf", bound="SpecialisedAssembly._Cast_SpecialisedAssembly"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssembly:
    """Special nested class for casting SpecialisedAssembly to subclasses."""

    __parent__: "SpecialisedAssembly"

    @property
    def abstract_assembly(self: "CastSelf") -> "_2489.AbstractAssembly":
        return self.__parent__._cast(_2489.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2525.Part":
        from mastapy._private.system_model.part_model import _2525

        return self.__parent__._cast(_2525.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2257.DesignEntity":
        from mastapy._private.system_model import _2257

        return self.__parent__._cast(_2257.DesignEntity)

    @property
    def bolted_joint(self: "CastSelf") -> "_2498.BoltedJoint":
        from mastapy._private.system_model.part_model import _2498

        return self.__parent__._cast(_2498.BoltedJoint)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2509.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2509

        return self.__parent__._cast(_2509.FlexiblePinAssembly)

    @property
    def microphone_array(self: "CastSelf") -> "_2520.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2520

        return self.__parent__._cast(_2520.MicrophoneArray)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2571.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2571

        return self.__parent__._cast(_2571.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2573.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2573

        return self.__parent__._cast(_2573.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2577.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2577

        return self.__parent__._cast(_2577.BevelGearSet)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2579.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2579

        return self.__parent__._cast(_2579.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2581.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2581

        return self.__parent__._cast(_2581.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2583.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2583

        return self.__parent__._cast(_2583.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2586.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2586

        return self.__parent__._cast(_2586.FaceGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2589.GearSet":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.GearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2592.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2592

        return self.__parent__._cast(_2592.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2594.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2594

        return self.__parent__._cast(_2594.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2596.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2598.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2599.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.PlanetaryGearSet)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2601.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2603.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2605.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.StraightBevelGearSet)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2609.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2611.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2625.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2625

        return self.__parent__._cast(_2625.CycloidalAssembly)

    @property
    def belt_drive(self: "CastSelf") -> "_2634.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2634

        return self.__parent__._cast(_2634.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2636.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2636

        return self.__parent__._cast(_2636.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2639.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2639

        return self.__parent__._cast(_2639.ConceptCoupling)

    @property
    def coupling(self: "CastSelf") -> "_2642.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2642

        return self.__parent__._cast(_2642.Coupling)

    @property
    def cvt(self: "CastSelf") -> "_2645.CVT":
        from mastapy._private.system_model.part_model.couplings import _2645

        return self.__parent__._cast(_2645.CVT)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2647.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2647

        return self.__parent__._cast(_2647.PartToPartShearCoupling)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2657.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2657

        return self.__parent__._cast(_2657.RollingRingAssembly)

    @property
    def spring_damper(self: "CastSelf") -> "_2663.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2663

        return self.__parent__._cast(_2663.SpringDamper)

    @property
    def synchroniser(self: "CastSelf") -> "_2665.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2665

        return self.__parent__._cast(_2665.Synchroniser)

    @property
    def torque_converter(self: "CastSelf") -> "_2670.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2670

        return self.__parent__._cast(_2670.TorqueConverter)

    @property
    def specialised_assembly(self: "CastSelf") -> "SpecialisedAssembly":
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
class SpecialisedAssembly(_2489.AbstractAssembly):
    """SpecialisedAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssembly":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssembly
        """
        return _Cast_SpecialisedAssembly(self)
