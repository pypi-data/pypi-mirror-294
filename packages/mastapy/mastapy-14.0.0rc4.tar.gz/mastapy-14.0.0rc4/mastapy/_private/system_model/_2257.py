"""DesignEntity"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DESIGN_ENTITY = python_net_import("SMT.MastaAPI.SystemModel", "DesignEntity")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2254
    from mastapy._private.system_model.connections_and_sockets import (
        _2319,
        _2322,
        _2323,
        _2326,
        _2327,
        _2335,
        _2341,
        _2346,
        _2349,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2396,
        _2398,
        _2400,
        _2402,
        _2404,
        _2406,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2389,
        _2392,
        _2395,
    )
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
    from mastapy._private.system_model.part_model import (
        _2488,
        _2489,
        _2490,
        _2491,
        _2494,
        _2497,
        _2498,
        _2499,
        _2502,
        _2503,
        _2507,
        _2508,
        _2509,
        _2510,
        _2517,
        _2518,
        _2519,
        _2520,
        _2521,
        _2523,
        _2525,
        _2526,
        _2528,
        _2529,
        _2531,
        _2533,
        _2534,
        _2536,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2634,
        _2636,
        _2637,
        _2639,
        _2640,
        _2642,
        _2643,
        _2645,
        _2646,
        _2647,
        _2648,
        _2650,
        _2656,
        _2657,
        _2658,
        _2663,
        _2664,
        _2665,
        _2667,
        _2668,
        _2669,
        _2670,
        _2671,
        _2673,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2625, _2626, _2627
    from mastapy._private.system_model.part_model.gears import (
        _2570,
        _2571,
        _2572,
        _2573,
        _2574,
        _2575,
        _2576,
        _2577,
        _2578,
        _2579,
        _2580,
        _2581,
        _2582,
        _2583,
        _2584,
        _2585,
        _2586,
        _2587,
        _2589,
        _2591,
        _2592,
        _2593,
        _2594,
        _2595,
        _2596,
        _2597,
        _2598,
        _2599,
        _2600,
        _2601,
        _2602,
        _2603,
        _2604,
        _2605,
        _2606,
        _2607,
        _2608,
        _2609,
        _2610,
        _2611,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2539
    from mastapy._private.utility.model_validation import _1844, _1845
    from mastapy._private.utility.scripting import _1792

    Self = TypeVar("Self", bound="DesignEntity")
    CastSelf = TypeVar("CastSelf", bound="DesignEntity._Cast_DesignEntity")


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntity:
    """Special nested class for casting DesignEntity to subclasses."""

    __parent__: "DesignEntity"

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2319.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2319

        return self.__parent__._cast(_2319.AbstractShaftToMountableComponentConnection)

    @property
    def belt_connection(self: "CastSelf") -> "_2322.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2322

        return self.__parent__._cast(_2322.BeltConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2323.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2323

        return self.__parent__._cast(_2323.CoaxialConnection)

    @property
    def connection(self: "CastSelf") -> "_2326.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2326

        return self.__parent__._cast(_2326.Connection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2327.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2327

        return self.__parent__._cast(_2327.CVTBeltConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2335.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2335

        return self.__parent__._cast(_2335.InterMountableComponentConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2341.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2341

        return self.__parent__._cast(_2341.PlanetaryConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2346.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2346

        return self.__parent__._cast(_2346.RollingRingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2349.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2349

        return self.__parent__._cast(_2349.ShaftToMountableComponentConnection)

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
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2389.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2389,
        )

        return self.__parent__._cast(_2389.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2392.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2392,
        )

        return self.__parent__._cast(_2392.CycloidalDiscPlanetaryBearingConnection)

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
    def assembly(self: "CastSelf") -> "_2488.Assembly":
        from mastapy._private.system_model.part_model import _2488

        return self.__parent__._cast(_2488.Assembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2489.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2489

        return self.__parent__._cast(_2489.AbstractAssembly)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2490.AbstractShaft":
        from mastapy._private.system_model.part_model import _2490

        return self.__parent__._cast(_2490.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2491.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2491

        return self.__parent__._cast(_2491.AbstractShaftOrHousing)

    @property
    def bearing(self: "CastSelf") -> "_2494.Bearing":
        from mastapy._private.system_model.part_model import _2494

        return self.__parent__._cast(_2494.Bearing)

    @property
    def bolt(self: "CastSelf") -> "_2497.Bolt":
        from mastapy._private.system_model.part_model import _2497

        return self.__parent__._cast(_2497.Bolt)

    @property
    def bolted_joint(self: "CastSelf") -> "_2498.BoltedJoint":
        from mastapy._private.system_model.part_model import _2498

        return self.__parent__._cast(_2498.BoltedJoint)

    @property
    def component(self: "CastSelf") -> "_2499.Component":
        from mastapy._private.system_model.part_model import _2499

        return self.__parent__._cast(_2499.Component)

    @property
    def connector(self: "CastSelf") -> "_2502.Connector":
        from mastapy._private.system_model.part_model import _2502

        return self.__parent__._cast(_2502.Connector)

    @property
    def datum(self: "CastSelf") -> "_2503.Datum":
        from mastapy._private.system_model.part_model import _2503

        return self.__parent__._cast(_2503.Datum)

    @property
    def external_cad_model(self: "CastSelf") -> "_2507.ExternalCADModel":
        from mastapy._private.system_model.part_model import _2507

        return self.__parent__._cast(_2507.ExternalCADModel)

    @property
    def fe_part(self: "CastSelf") -> "_2508.FEPart":
        from mastapy._private.system_model.part_model import _2508

        return self.__parent__._cast(_2508.FEPart)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2509.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2509

        return self.__parent__._cast(_2509.FlexiblePinAssembly)

    @property
    def guide_dxf_model(self: "CastSelf") -> "_2510.GuideDxfModel":
        from mastapy._private.system_model.part_model import _2510

        return self.__parent__._cast(_2510.GuideDxfModel)

    @property
    def mass_disc(self: "CastSelf") -> "_2517.MassDisc":
        from mastapy._private.system_model.part_model import _2517

        return self.__parent__._cast(_2517.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2518.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2518

        return self.__parent__._cast(_2518.MeasurementComponent)

    @property
    def microphone(self: "CastSelf") -> "_2519.Microphone":
        from mastapy._private.system_model.part_model import _2519

        return self.__parent__._cast(_2519.Microphone)

    @property
    def microphone_array(self: "CastSelf") -> "_2520.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2520

        return self.__parent__._cast(_2520.MicrophoneArray)

    @property
    def mountable_component(self: "CastSelf") -> "_2521.MountableComponent":
        from mastapy._private.system_model.part_model import _2521

        return self.__parent__._cast(_2521.MountableComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2523.OilSeal":
        from mastapy._private.system_model.part_model import _2523

        return self.__parent__._cast(_2523.OilSeal)

    @property
    def part(self: "CastSelf") -> "_2525.Part":
        from mastapy._private.system_model.part_model import _2525

        return self.__parent__._cast(_2525.Part)

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
    def root_assembly(self: "CastSelf") -> "_2531.RootAssembly":
        from mastapy._private.system_model.part_model import _2531

        return self.__parent__._cast(_2531.RootAssembly)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2533.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2533

        return self.__parent__._cast(_2533.SpecialisedAssembly)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2534.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2534

        return self.__parent__._cast(_2534.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2536.VirtualComponent":
        from mastapy._private.system_model.part_model import _2536

        return self.__parent__._cast(_2536.VirtualComponent)

    @property
    def shaft(self: "CastSelf") -> "_2539.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2539

        return self.__parent__._cast(_2539.Shaft)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2570.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2570

        return self.__parent__._cast(_2570.AGMAGleasonConicalGear)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2571.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2571

        return self.__parent__._cast(_2571.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2572.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2572

        return self.__parent__._cast(_2572.BevelDifferentialGear)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2573.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2573

        return self.__parent__._cast(_2573.BevelDifferentialGearSet)

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
    def bevel_gear_set(self: "CastSelf") -> "_2577.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2577

        return self.__parent__._cast(_2577.BevelGearSet)

    @property
    def concept_gear(self: "CastSelf") -> "_2578.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2578

        return self.__parent__._cast(_2578.ConceptGear)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2579.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2579

        return self.__parent__._cast(_2579.ConceptGearSet)

    @property
    def conical_gear(self: "CastSelf") -> "_2580.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2580

        return self.__parent__._cast(_2580.ConicalGear)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2581.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2581

        return self.__parent__._cast(_2581.ConicalGearSet)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2582.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.CylindricalGear)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2583.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2583

        return self.__parent__._cast(_2583.CylindricalGearSet)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2584.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2584

        return self.__parent__._cast(_2584.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2585.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.FaceGear)

    @property
    def face_gear_set(self: "CastSelf") -> "_2586.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2586

        return self.__parent__._cast(_2586.FaceGearSet)

    @property
    def gear(self: "CastSelf") -> "_2587.Gear":
        from mastapy._private.system_model.part_model.gears import _2587

        return self.__parent__._cast(_2587.Gear)

    @property
    def gear_set(self: "CastSelf") -> "_2589.GearSet":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.GearSet)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2591.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.HypoidGear)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2592.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2592

        return self.__parent__._cast(_2592.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2593.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2593

        return self.__parent__._cast(_2593.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2594.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2594

        return self.__parent__._cast(_2594.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2595.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2596.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2597.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.KlingelnbergCycloPalloidSpiralBevelGear)

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
    def spiral_bevel_gear(self: "CastSelf") -> "_2600.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2600

        return self.__parent__._cast(_2600.SpiralBevelGear)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2601.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2602.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2602

        return self.__parent__._cast(_2602.StraightBevelDiffGear)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2603.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2604.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.StraightBevelGear)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2605.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.StraightBevelGearSet)

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
    def worm_gear_set(self: "CastSelf") -> "_2609.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.WormGearSet)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2610.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.ZerolBevelGear)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2611.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2625.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2625

        return self.__parent__._cast(_2625.CycloidalAssembly)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2626.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2626

        return self.__parent__._cast(_2626.CycloidalDisc)

    @property
    def ring_pins(self: "CastSelf") -> "_2627.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2627

        return self.__parent__._cast(_2627.RingPins)

    @property
    def belt_drive(self: "CastSelf") -> "_2634.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2634

        return self.__parent__._cast(_2634.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2636.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2636

        return self.__parent__._cast(_2636.Clutch)

    @property
    def clutch_half(self: "CastSelf") -> "_2637.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2637

        return self.__parent__._cast(_2637.ClutchHalf)

    @property
    def concept_coupling(self: "CastSelf") -> "_2639.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2639

        return self.__parent__._cast(_2639.ConceptCoupling)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2640.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2640

        return self.__parent__._cast(_2640.ConceptCouplingHalf)

    @property
    def coupling(self: "CastSelf") -> "_2642.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2642

        return self.__parent__._cast(_2642.Coupling)

    @property
    def coupling_half(self: "CastSelf") -> "_2643.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2643

        return self.__parent__._cast(_2643.CouplingHalf)

    @property
    def cvt(self: "CastSelf") -> "_2645.CVT":
        from mastapy._private.system_model.part_model.couplings import _2645

        return self.__parent__._cast(_2645.CVT)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2646.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2646

        return self.__parent__._cast(_2646.CVTPulley)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2647.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2647

        return self.__parent__._cast(_2647.PartToPartShearCoupling)

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
    def rolling_ring_assembly(self: "CastSelf") -> "_2657.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2657

        return self.__parent__._cast(_2657.RollingRingAssembly)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2658.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2658

        return self.__parent__._cast(_2658.ShaftHubConnection)

    @property
    def spring_damper(self: "CastSelf") -> "_2663.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2663

        return self.__parent__._cast(_2663.SpringDamper)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2664.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2664

        return self.__parent__._cast(_2664.SpringDamperHalf)

    @property
    def synchroniser(self: "CastSelf") -> "_2665.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2665

        return self.__parent__._cast(_2665.Synchroniser)

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
    def torque_converter(self: "CastSelf") -> "_2670.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2670

        return self.__parent__._cast(_2670.TorqueConverter)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2671.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2671

        return self.__parent__._cast(_2671.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2673.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2673

        return self.__parent__._cast(_2673.TorqueConverterTurbine)

    @property
    def design_entity(self: "CastSelf") -> "DesignEntity":
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
class DesignEntity(_0.APIBase):
    """DesignEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

    @property
    def full_name_without_root_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullNameWithoutRootName")

        if temp is None:
            return ""

        return temp

    @property
    def id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return ""

        return temp

    @property
    def icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Icon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def small_icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallIcon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    def design_properties(self: "Self") -> "_2254.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def all_design_entities(self: "Self") -> "List[DesignEntity]":
        """List[mastapy.system_model.DesignEntity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllDesignEntities")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_status_errors(self: "Self") -> "List[_1845.StatusItem]":
        """List[mastapy.utility.model_validation.StatusItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllStatusErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def status(self: "Self") -> "_1844.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def user_specified_data(self: "Self") -> "_1792.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DesignEntity":
        """Cast to another type.

        Returns:
            _Cast_DesignEntity
        """
        return _Cast_DesignEntity(self)
