"""CompoundAdvancedSystemDeflectionAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call_overload,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results import _2703

_CONCEPT_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "ConceptCouplingConnection",
)
_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "CouplingConnection"
)
_SPRING_DAMPER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "SpringDamperConnection"
)
_TORQUE_CONVERTER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "TorqueConverterConnection",
)
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "PartToPartShearCouplingConnection",
)
_CLUTCH_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "ClutchConnection"
)
_ABSTRACT_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
)
_MICROPHONE = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Microphone")
_MICROPHONE_ARRAY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
)
_ABSTRACT_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
)
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
)
_BEARING = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")
_BOLT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")
_BOLTED_JOINT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "BoltedJoint")
_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_CONNECTOR = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Connector")
_DATUM = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")
_EXTERNAL_CAD_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "ExternalCADModel"
)
_FE_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")
_FLEXIBLE_PIN_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
)
_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")
_GUIDE_DXF_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
)
_MASS_DISC = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")
_MEASUREMENT_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
)
_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)
_OIL_SEAL = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")
_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
_PLANET_CARRIER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
)
_POINT_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")
_POWER_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")
_ROOT_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "RootAssembly")
_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)
_UNBALANCED_MASS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMass"
)
_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)
_SHAFT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft")
_CONCEPT_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGear"
)
_CONCEPT_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGearSet"
)
_FACE_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear")
_FACE_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
)
_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)
_BEVEL_DIFFERENTIAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
)
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
)
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
)
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
)
_BEVEL_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear")
_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
)
_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
)
_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)
_CYLINDRICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
)
_CYLINDRICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
)
_CYLINDRICAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
)
_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")
_GEAR_SET = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet")
_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGear"
)
_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGear"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGear"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGear",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearSet",
)
_PLANETARY_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
)
_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGear"
)
_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
)
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
)
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGearSet"
)
_STRAIGHT_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGear"
)
_STRAIGHT_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGearSet"
)
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelPlanetGear"
)
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
)
_WORM_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGear")
_WORM_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
)
_ZEROL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
)
_ZEROL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
)
_CYCLOIDAL_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
)
_CYCLOIDAL_DISC = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
)
_RING_PINS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
)
_PART_TO_PART_SHEAR_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
)
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCouplingHalf"
)
_BELT_DRIVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
)
_CLUTCH = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch")
_CLUTCH_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
)
_CONCEPT_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
)
_CONCEPT_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
)
_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
)
_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)
_CVT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT")
_CVT_PULLEY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVTPulley"
)
_PULLEY = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley")
_SHAFT_HUB_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
)
_ROLLING_RING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRing"
)
_ROLLING_RING_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
)
_SPRING_DAMPER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
)
_SPRING_DAMPER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
)
_SYNCHRONISER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
)
_SYNCHRONISER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
)
_SYNCHRONISER_PART = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
)
_SYNCHRONISER_SLEEVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
)
_TORQUE_CONVERTER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
)
_TORQUE_CONVERTER_PUMP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterPump"
)
_TORQUE_CONVERTER_TURBINE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
)
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "ShaftToMountableComponentConnection",
)
_CVT_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CVTBeltConnection"
)
_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "BeltConnection"
)
_COAXIAL_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CoaxialConnection"
)
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "InterMountableComponentConnection",
)
_PLANETARY_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PlanetaryConnection"
)
_ROLLING_RING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "RollingRingConnection"
)
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "AbstractShaftToMountableComponentConnection",
)
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelDifferentialGearMesh"
)
_CONCEPT_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConceptGearMesh"
)
_FACE_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "FaceGearMesh"
)
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelDiffGearMesh"
)
_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelGearMesh"
)
_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConicalGearMesh"
)
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "AGMAGleasonConicalGearMesh"
)
_CYLINDRICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "CylindricalGearMesh"
)
_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "HypoidGearMesh"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidConicalGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidHypoidGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearMesh",
)
_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "SpiralBevelGearMesh"
)
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelGearMesh"
)
_WORM_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "WormGearMesh"
)
_ZEROL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ZerolBevelGearMesh"
)
_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearMesh"
)
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscCentralBearingConnection",
)
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscPlanetaryBearingConnection",
)
_RING_PINS_TO_DISC_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "RingPinsToDiscConnection",
)
_COMPOUND_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults",
    "CompoundAdvancedSystemDeflectionAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Iterable, Type, TypeVar

    from mastapy._private import _7722
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7561,
        _7562,
        _7563,
        _7564,
        _7565,
        _7566,
        _7567,
        _7568,
        _7569,
        _7570,
        _7571,
        _7572,
        _7573,
        _7574,
        _7575,
        _7576,
        _7577,
        _7578,
        _7579,
        _7580,
        _7581,
        _7582,
        _7583,
        _7584,
        _7585,
        _7586,
        _7587,
        _7588,
        _7589,
        _7590,
        _7591,
        _7592,
        _7593,
        _7594,
        _7595,
        _7596,
        _7597,
        _7598,
        _7599,
        _7600,
        _7601,
        _7602,
        _7603,
        _7604,
        _7605,
        _7606,
        _7607,
        _7608,
        _7609,
        _7610,
        _7611,
        _7612,
        _7613,
        _7614,
        _7615,
        _7616,
        _7617,
        _7618,
        _7619,
        _7620,
        _7621,
        _7622,
        _7623,
        _7624,
        _7625,
        _7626,
        _7627,
        _7628,
        _7629,
        _7630,
        _7631,
        _7632,
        _7633,
        _7634,
        _7635,
        _7636,
        _7637,
        _7638,
        _7639,
        _7640,
        _7641,
        _7642,
        _7643,
        _7644,
        _7645,
        _7646,
        _7647,
        _7648,
        _7649,
        _7650,
        _7651,
        _7652,
        _7653,
        _7654,
        _7655,
        _7656,
        _7657,
        _7658,
        _7659,
        _7660,
        _7661,
        _7662,
        _7663,
        _7664,
        _7665,
        _7666,
        _7667,
        _7668,
        _7669,
        _7670,
        _7671,
        _7672,
        _7673,
        _7674,
        _7675,
        _7676,
        _7677,
        _7678,
        _7679,
        _7680,
        _7681,
        _7682,
        _7683,
        _7684,
        _7685,
        _7686,
        _7687,
        _7688,
        _7689,
        _7690,
        _7691,
    )
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

    Self = TypeVar("Self", bound="CompoundAdvancedSystemDeflectionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CompoundAdvancedSystemDeflectionAnalysis._Cast_CompoundAdvancedSystemDeflectionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CompoundAdvancedSystemDeflectionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundAdvancedSystemDeflectionAnalysis:
    """Special nested class for casting CompoundAdvancedSystemDeflectionAnalysis to subclasses."""

    __parent__: "CompoundAdvancedSystemDeflectionAnalysis"

    @property
    def compound_analysis(self: "CastSelf") -> "_2703.CompoundAnalysis":
        return self.__parent__._cast(_2703.CompoundAnalysis)

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7722.MarshalByRefObjectPermanent":
        from mastapy._private import _7722

        return self.__parent__._cast(_7722.MarshalByRefObjectPermanent)

    @property
    def compound_advanced_system_deflection_analysis(
        self: "CastSelf",
    ) -> "CompoundAdvancedSystemDeflectionAnalysis":
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
class CompoundAdvancedSystemDeflectionAnalysis(_2703.CompoundAnalysis):
    """CompoundAdvancedSystemDeflectionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPOUND_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @enforce_parameter_types
    def results_for_concept_coupling_connection(
        self: "Self", design_entity: "_2398.ConceptCouplingConnection"
    ) -> "Iterable[_7588.ConceptCouplingConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptCouplingConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_COUPLING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_coupling_connection(
        self: "Self", design_entity: "_2400.CouplingConnection"
    ) -> "Iterable[_7599.CouplingConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CouplingConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COUPLING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spring_damper_connection(
        self: "Self", design_entity: "_2404.SpringDamperConnection"
    ) -> "Iterable[_7666.SpringDamperConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpringDamperConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPRING_DAMPER_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_torque_converter_connection(
        self: "Self", design_entity: "_2406.TorqueConverterConnection"
    ) -> "Iterable[_7681.TorqueConverterConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_TORQUE_CONVERTER_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_abstract_shaft(
        self: "Self", design_entity: "_2490.AbstractShaft"
    ) -> "Iterable[_7562.AbstractShaftCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractShaftCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ABSTRACT_SHAFT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_microphone(
        self: "Self", design_entity: "_2519.Microphone"
    ) -> "Iterable[_7639.MicrophoneCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MicrophoneCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.Microphone)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MICROPHONE],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_microphone_array(
        self: "Self", design_entity: "_2520.MicrophoneArray"
    ) -> "Iterable[_7638.MicrophoneArrayCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MicrophoneArrayCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.MicrophoneArray)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MICROPHONE_ARRAY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_abstract_assembly(
        self: "Self", design_entity: "_2489.AbstractAssembly"
    ) -> "Iterable[_7561.AbstractAssemblyCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractAssemblyCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ABSTRACT_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_abstract_shaft_or_housing(
        self: "Self", design_entity: "_2491.AbstractShaftOrHousing"
    ) -> "Iterable[_7563.AbstractShaftOrHousingCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractShaftOrHousingCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ABSTRACT_SHAFT_OR_HOUSING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bearing(
        self: "Self", design_entity: "_2494.Bearing"
    ) -> "Iterable[_7569.BearingCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BearingCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEARING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bolt(
        self: "Self", design_entity: "_2497.Bolt"
    ) -> "Iterable[_7580.BoltCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BoltCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BOLT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bolted_joint(
        self: "Self", design_entity: "_2498.BoltedJoint"
    ) -> "Iterable[_7581.BoltedJointCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BoltedJointCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BOLTED_JOINT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_component(
        self: "Self", design_entity: "_2499.Component"
    ) -> "Iterable[_7586.ComponentCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ComponentCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.Component)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COMPONENT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_connector(
        self: "Self", design_entity: "_2502.Connector"
    ) -> "Iterable[_7597.ConnectorCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConnectorCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.Connector)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONNECTOR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_datum(
        self: "Self", design_entity: "_2503.Datum"
    ) -> "Iterable[_7612.DatumCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.DatumCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.Datum)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_DATUM],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_external_cad_model(
        self: "Self", design_entity: "_2507.ExternalCADModel"
    ) -> "Iterable[_7613.ExternalCADModelCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ExternalCADModelCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_EXTERNAL_CAD_MODEL],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_fe_part(
        self: "Self", design_entity: "_2508.FEPart"
    ) -> "Iterable[_7617.FEPartCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FEPartCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FE_PART],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_flexible_pin_assembly(
        self: "Self", design_entity: "_2509.FlexiblePinAssembly"
    ) -> "Iterable[_7618.FlexiblePinAssemblyCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FlexiblePinAssemblyCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FLEXIBLE_PIN_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_assembly(
        self: "Self", design_entity: "_2488.Assembly"
    ) -> "Iterable[_7568.AssemblyCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AssemblyCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_guide_dxf_model(
        self: "Self", design_entity: "_2510.GuideDxfModel"
    ) -> "Iterable[_7622.GuideDxfModelCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GuideDxfModelCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_GUIDE_DXF_MODEL],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_mass_disc(
        self: "Self", design_entity: "_2517.MassDisc"
    ) -> "Iterable[_7636.MassDiscCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MassDiscCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MASS_DISC],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_measurement_component(
        self: "Self", design_entity: "_2518.MeasurementComponent"
    ) -> "Iterable[_7637.MeasurementComponentCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MeasurementComponentCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MEASUREMENT_COMPONENT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_mountable_component(
        self: "Self", design_entity: "_2521.MountableComponent"
    ) -> "Iterable[_7640.MountableComponentCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MountableComponentCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MOUNTABLE_COMPONENT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_oil_seal(
        self: "Self", design_entity: "_2523.OilSeal"
    ) -> "Iterable[_7641.OilSealCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.OilSealCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_OIL_SEAL],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_part(
        self: "Self", design_entity: "_2525.Part"
    ) -> "Iterable[_7642.PartCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.Part)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PART],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_planet_carrier(
        self: "Self", design_entity: "_2526.PlanetCarrier"
    ) -> "Iterable[_7648.PlanetCarrierCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PlanetCarrierCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PLANET_CARRIER],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_point_load(
        self: "Self", design_entity: "_2528.PointLoad"
    ) -> "Iterable[_7649.PointLoadCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PointLoadCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_POINT_LOAD],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_power_load(
        self: "Self", design_entity: "_2529.PowerLoad"
    ) -> "Iterable[_7650.PowerLoadCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PowerLoadCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_POWER_LOAD],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_root_assembly(
        self: "Self", design_entity: "_2531.RootAssembly"
    ) -> "Iterable[_7657.RootAssemblyCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RootAssemblyCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ROOT_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_specialised_assembly(
        self: "Self", design_entity: "_2533.SpecialisedAssembly"
    ) -> "Iterable[_7661.SpecialisedAssemblyCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpecialisedAssemblyCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPECIALISED_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_unbalanced_mass(
        self: "Self", design_entity: "_2534.UnbalancedMass"
    ) -> "Iterable[_7684.UnbalancedMassCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.UnbalancedMassCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_UNBALANCED_MASS],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_virtual_component(
        self: "Self", design_entity: "_2536.VirtualComponent"
    ) -> "Iterable[_7685.VirtualComponentCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.VirtualComponentCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_VIRTUAL_COMPONENT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_shaft(
        self: "Self", design_entity: "_2539.Shaft"
    ) -> "Iterable[_7658.ShaftCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ShaftCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SHAFT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_gear(
        self: "Self", design_entity: "_2578.ConceptGear"
    ) -> "Iterable[_7590.ConceptGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_gear_set(
        self: "Self", design_entity: "_2579.ConceptGearSet"
    ) -> "Iterable[_7592.ConceptGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_face_gear(
        self: "Self", design_entity: "_2585.FaceGear"
    ) -> "Iterable[_7614.FaceGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FaceGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FACE_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_face_gear_set(
        self: "Self", design_entity: "_2586.FaceGearSet"
    ) -> "Iterable[_7616.FaceGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FaceGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FACE_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear(
        self: "Self", design_entity: "_2570.AGMAGleasonConicalGear"
    ) -> "Iterable[_7565.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_AGMA_GLEASON_CONICAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_set(
        self: "Self", design_entity: "_2571.AGMAGleasonConicalGearSet"
    ) -> "Iterable[_7567.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_AGMA_GLEASON_CONICAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear(
        self: "Self", design_entity: "_2572.BevelDifferentialGear"
    ) -> "Iterable[_7572.BevelDifferentialGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear_set(
        self: "Self", design_entity: "_2573.BevelDifferentialGearSet"
    ) -> "Iterable[_7574.BevelDifferentialGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_planet_gear(
        self: "Self", design_entity: "_2574.BevelDifferentialPlanetGear"
    ) -> "Iterable[_7575.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_PLANET_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_sun_gear(
        self: "Self", design_entity: "_2575.BevelDifferentialSunGear"
    ) -> "Iterable[_7576.BevelDifferentialSunGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialSunGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_SUN_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_gear(
        self: "Self", design_entity: "_2576.BevelGear"
    ) -> "Iterable[_7577.BevelGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_gear_set(
        self: "Self", design_entity: "_2577.BevelGearSet"
    ) -> "Iterable[_7579.BevelGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_conical_gear(
        self: "Self", design_entity: "_2580.ConicalGear"
    ) -> "Iterable[_7593.ConicalGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONICAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_conical_gear_set(
        self: "Self", design_entity: "_2581.ConicalGearSet"
    ) -> "Iterable[_7595.ConicalGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONICAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear(
        self: "Self", design_entity: "_2582.CylindricalGear"
    ) -> "Iterable[_7608.CylindricalGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYLINDRICAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear_set(
        self: "Self", design_entity: "_2583.CylindricalGearSet"
    ) -> "Iterable[_7610.CylindricalGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYLINDRICAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cylindrical_planet_gear(
        self: "Self", design_entity: "_2584.CylindricalPlanetGear"
    ) -> "Iterable[_7611.CylindricalPlanetGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalPlanetGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYLINDRICAL_PLANET_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_gear(
        self: "Self", design_entity: "_2587.Gear"
    ) -> "Iterable[_7619.GearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_gear_set(
        self: "Self", design_entity: "_2589.GearSet"
    ) -> "Iterable[_7621.GearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_hypoid_gear(
        self: "Self", design_entity: "_2591.HypoidGear"
    ) -> "Iterable[_7623.HypoidGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.HypoidGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_HYPOID_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_hypoid_gear_set(
        self: "Self", design_entity: "_2592.HypoidGearSet"
    ) -> "Iterable[_7625.HypoidGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.HypoidGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_HYPOID_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear(
        self: "Self", design_entity: "_2593.KlingelnbergCycloPalloidConicalGear"
    ) -> "Iterable[_7627.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(
        self: "Self", design_entity: "_2594.KlingelnbergCycloPalloidConicalGearSet"
    ) -> "Iterable[_7629.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(
        self: "Self", design_entity: "_2595.KlingelnbergCycloPalloidHypoidGear"
    ) -> "Iterable[_7630.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self", design_entity: "_2596.KlingelnbergCycloPalloidHypoidGearSet"
    ) -> "Iterable[_7632.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "Self", design_entity: "_2597.KlingelnbergCycloPalloidSpiralBevelGear"
    ) -> "Iterable[_7633.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2598.KlingelnbergCycloPalloidSpiralBevelGearSet"
    ) -> "Iterable[_7635.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_planetary_gear_set(
        self: "Self", design_entity: "_2599.PlanetaryGearSet"
    ) -> "Iterable[_7647.PlanetaryGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PlanetaryGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PLANETARY_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear(
        self: "Self", design_entity: "_2600.SpiralBevelGear"
    ) -> "Iterable[_7662.SpiralBevelGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpiralBevelGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPIRAL_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2601.SpiralBevelGearSet"
    ) -> "Iterable[_7664.SpiralBevelGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpiralBevelGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPIRAL_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear(
        self: "Self", design_entity: "_2602.StraightBevelDiffGear"
    ) -> "Iterable[_7668.StraightBevelDiffGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelDiffGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_DIFF_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_set(
        self: "Self", design_entity: "_2603.StraightBevelDiffGearSet"
    ) -> "Iterable[_7670.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_DIFF_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear(
        self: "Self", design_entity: "_2604.StraightBevelGear"
    ) -> "Iterable[_7671.StraightBevelGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear_set(
        self: "Self", design_entity: "_2605.StraightBevelGearSet"
    ) -> "Iterable[_7673.StraightBevelGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_planet_gear(
        self: "Self", design_entity: "_2606.StraightBevelPlanetGear"
    ) -> "Iterable[_7674.StraightBevelPlanetGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelPlanetGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_PLANET_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_sun_gear(
        self: "Self", design_entity: "_2607.StraightBevelSunGear"
    ) -> "Iterable[_7675.StraightBevelSunGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelSunGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_SUN_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_worm_gear(
        self: "Self", design_entity: "_2608.WormGear"
    ) -> "Iterable[_7686.WormGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.WormGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_WORM_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_worm_gear_set(
        self: "Self", design_entity: "_2609.WormGearSet"
    ) -> "Iterable[_7688.WormGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.WormGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_WORM_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear(
        self: "Self", design_entity: "_2610.ZerolBevelGear"
    ) -> "Iterable[_7689.ZerolBevelGearCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ZEROL_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear_set(
        self: "Self", design_entity: "_2611.ZerolBevelGearSet"
    ) -> "Iterable[_7691.ZerolBevelGearSetCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearSetCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ZEROL_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cycloidal_assembly(
        self: "Self", design_entity: "_2625.CycloidalAssembly"
    ) -> "Iterable[_7604.CycloidalAssemblyCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CycloidalAssemblyCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYCLOIDAL_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc(
        self: "Self", design_entity: "_2626.CycloidalDisc"
    ) -> "Iterable[_7606.CycloidalDiscCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CycloidalDiscCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYCLOIDAL_DISC],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_ring_pins(
        self: "Self", design_entity: "_2627.RingPins"
    ) -> "Iterable[_7652.RingPinsCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RingPinsCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_RING_PINS],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling(
        self: "Self", design_entity: "_2647.PartToPartShearCoupling"
    ) -> "Iterable[_7643.PartToPartShearCouplingCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartToPartShearCouplingCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PART_TO_PART_SHEAR_COUPLING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_half(
        self: "Self", design_entity: "_2648.PartToPartShearCouplingHalf"
    ) -> "Iterable[_7645.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PART_TO_PART_SHEAR_COUPLING_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_belt_drive(
        self: "Self", design_entity: "_2634.BeltDrive"
    ) -> "Iterable[_7571.BeltDriveCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BeltDriveCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BELT_DRIVE],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_clutch(
        self: "Self", design_entity: "_2636.Clutch"
    ) -> "Iterable[_7582.ClutchCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ClutchCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CLUTCH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_clutch_half(
        self: "Self", design_entity: "_2637.ClutchHalf"
    ) -> "Iterable[_7584.ClutchHalfCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ClutchHalfCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CLUTCH_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_coupling(
        self: "Self", design_entity: "_2639.ConceptCoupling"
    ) -> "Iterable[_7587.ConceptCouplingCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptCouplingCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_COUPLING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_coupling_half(
        self: "Self", design_entity: "_2640.ConceptCouplingHalf"
    ) -> "Iterable[_7589.ConceptCouplingHalfCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptCouplingHalfCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_COUPLING_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_coupling(
        self: "Self", design_entity: "_2642.Coupling"
    ) -> "Iterable[_7598.CouplingCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CouplingCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COUPLING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_coupling_half(
        self: "Self", design_entity: "_2643.CouplingHalf"
    ) -> "Iterable[_7600.CouplingHalfCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CouplingHalfCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COUPLING_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cvt(
        self: "Self", design_entity: "_2645.CVT"
    ) -> "Iterable[_7602.CVTCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CVTCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CVT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cvt_pulley(
        self: "Self", design_entity: "_2646.CVTPulley"
    ) -> "Iterable[_7603.CVTPulleyCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CVTPulleyCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CVT_PULLEY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_pulley(
        self: "Self", design_entity: "_2650.Pulley"
    ) -> "Iterable[_7651.PulleyCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PulleyCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PULLEY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_shaft_hub_connection(
        self: "Self", design_entity: "_2658.ShaftHubConnection"
    ) -> "Iterable[_7659.ShaftHubConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ShaftHubConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SHAFT_HUB_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_rolling_ring(
        self: "Self", design_entity: "_2656.RollingRing"
    ) -> "Iterable[_7655.RollingRingCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RollingRingCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ROLLING_RING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_rolling_ring_assembly(
        self: "Self", design_entity: "_2657.RollingRingAssembly"
    ) -> "Iterable[_7654.RollingRingAssemblyCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RollingRingAssemblyCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ROLLING_RING_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spring_damper(
        self: "Self", design_entity: "_2663.SpringDamper"
    ) -> "Iterable[_7665.SpringDamperCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpringDamperCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPRING_DAMPER],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spring_damper_half(
        self: "Self", design_entity: "_2664.SpringDamperHalf"
    ) -> "Iterable[_7667.SpringDamperHalfCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpringDamperHalfCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPRING_DAMPER_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_synchroniser(
        self: "Self", design_entity: "_2665.Synchroniser"
    ) -> "Iterable[_7676.SynchroniserCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SYNCHRONISER],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_synchroniser_half(
        self: "Self", design_entity: "_2667.SynchroniserHalf"
    ) -> "Iterable[_7677.SynchroniserHalfCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserHalfCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SYNCHRONISER_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_synchroniser_part(
        self: "Self", design_entity: "_2668.SynchroniserPart"
    ) -> "Iterable[_7678.SynchroniserPartCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserPartCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SYNCHRONISER_PART],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_synchroniser_sleeve(
        self: "Self", design_entity: "_2669.SynchroniserSleeve"
    ) -> "Iterable[_7679.SynchroniserSleeveCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserSleeveCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SYNCHRONISER_SLEEVE],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_torque_converter(
        self: "Self", design_entity: "_2670.TorqueConverter"
    ) -> "Iterable[_7680.TorqueConverterCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_TORQUE_CONVERTER],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_torque_converter_pump(
        self: "Self", design_entity: "_2671.TorqueConverterPump"
    ) -> "Iterable[_7682.TorqueConverterPumpCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterPumpCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_TORQUE_CONVERTER_PUMP],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_torque_converter_turbine(
        self: "Self", design_entity: "_2673.TorqueConverterTurbine"
    ) -> "Iterable[_7683.TorqueConverterTurbineCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterTurbineCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_TORQUE_CONVERTER_TURBINE],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2349.ShaftToMountableComponentConnection"
    ) -> "Iterable[_7660.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cvt_belt_connection(
        self: "Self", design_entity: "_2327.CVTBeltConnection"
    ) -> "Iterable[_7601.CVTBeltConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CVTBeltConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CVT_BELT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_belt_connection(
        self: "Self", design_entity: "_2322.BeltConnection"
    ) -> "Iterable[_7570.BeltConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BeltConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BELT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_coaxial_connection(
        self: "Self", design_entity: "_2323.CoaxialConnection"
    ) -> "Iterable[_7585.CoaxialConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CoaxialConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COAXIAL_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_connection(
        self: "Self", design_entity: "_2326.Connection"
    ) -> "Iterable[_7596.ConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_inter_mountable_component_connection(
        self: "Self", design_entity: "_2335.InterMountableComponentConnection"
    ) -> "Iterable[_7626.InterMountableComponentConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.InterMountableComponentConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_INTER_MOUNTABLE_COMPONENT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_planetary_connection(
        self: "Self", design_entity: "_2341.PlanetaryConnection"
    ) -> "Iterable[_7646.PlanetaryConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PlanetaryConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PLANETARY_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_rolling_ring_connection(
        self: "Self", design_entity: "_2346.RollingRingConnection"
    ) -> "Iterable[_7656.RollingRingConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RollingRingConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ROLLING_RING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_abstract_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2319.AbstractShaftToMountableComponentConnection"
    ) -> "Iterable[_7564.AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear_mesh(
        self: "Self", design_entity: "_2355.BevelDifferentialGearMesh"
    ) -> "Iterable[_7573.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_gear_mesh(
        self: "Self", design_entity: "_2359.ConceptGearMesh"
    ) -> "Iterable[_7591.ConceptGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_face_gear_mesh(
        self: "Self", design_entity: "_2365.FaceGearMesh"
    ) -> "Iterable[_7615.FaceGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FaceGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FACE_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_mesh(
        self: "Self", design_entity: "_2379.StraightBevelDiffGearMesh"
    ) -> "Iterable[_7669.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_DIFF_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_gear_mesh(
        self: "Self", design_entity: "_2357.BevelGearMesh"
    ) -> "Iterable[_7578.BevelGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_conical_gear_mesh(
        self: "Self", design_entity: "_2361.ConicalGearMesh"
    ) -> "Iterable[_7594.ConicalGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONICAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_mesh(
        self: "Self", design_entity: "_2353.AGMAGleasonConicalGearMesh"
    ) -> "Iterable[_7566.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_AGMA_GLEASON_CONICAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear_mesh(
        self: "Self", design_entity: "_2363.CylindricalGearMesh"
    ) -> "Iterable[_7609.CylindricalGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYLINDRICAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_hypoid_gear_mesh(
        self: "Self", design_entity: "_2369.HypoidGearMesh"
    ) -> "Iterable[_7624.HypoidGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.HypoidGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_HYPOID_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "Self", design_entity: "_2372.KlingelnbergCycloPalloidConicalGearMesh"
    ) -> "Iterable[_7628.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "Self", design_entity: "_2373.KlingelnbergCycloPalloidHypoidGearMesh"
    ) -> "Iterable[_7631.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2374.KlingelnbergCycloPalloidSpiralBevelGearMesh"
    ) -> "Iterable[_7634.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2377.SpiralBevelGearMesh"
    ) -> "Iterable[_7663.SpiralBevelGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpiralBevelGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPIRAL_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear_mesh(
        self: "Self", design_entity: "_2381.StraightBevelGearMesh"
    ) -> "Iterable[_7672.StraightBevelGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_worm_gear_mesh(
        self: "Self", design_entity: "_2383.WormGearMesh"
    ) -> "Iterable[_7687.WormGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.WormGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_WORM_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear_mesh(
        self: "Self", design_entity: "_2385.ZerolBevelGearMesh"
    ) -> "Iterable[_7690.ZerolBevelGearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ZEROL_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_gear_mesh(
        self: "Self", design_entity: "_2367.GearMesh"
    ) -> "Iterable[_7620.GearMeshCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GearMeshCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc_central_bearing_connection(
        self: "Self", design_entity: "_2389.CycloidalDiscCentralBearingConnection"
    ) -> "Iterable[_7605.CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc_planetary_bearing_connection(
        self: "Self", design_entity: "_2392.CycloidalDiscPlanetaryBearingConnection"
    ) -> "Iterable[_7607.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_ring_pins_to_disc_connection(
        self: "Self", design_entity: "_2395.RingPinsToDiscConnection"
    ) -> "Iterable[_7653.RingPinsToDiscConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RingPinsToDiscConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_RING_PINS_TO_DISC_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_connection(
        self: "Self", design_entity: "_2402.PartToPartShearCouplingConnection"
    ) -> "Iterable[_7644.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PART_TO_PART_SHEAR_COUPLING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_clutch_connection(
        self: "Self", design_entity: "_2396.ClutchConnection"
    ) -> "Iterable[_7583.ClutchConnectionCompoundAdvancedSystemDeflection]":
        """Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ClutchConnectionCompoundAdvancedSystemDeflection]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CLUTCH_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CompoundAdvancedSystemDeflectionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CompoundAdvancedSystemDeflectionAnalysis
        """
        return _Cast_CompoundAdvancedSystemDeflectionAnalysis(self)
