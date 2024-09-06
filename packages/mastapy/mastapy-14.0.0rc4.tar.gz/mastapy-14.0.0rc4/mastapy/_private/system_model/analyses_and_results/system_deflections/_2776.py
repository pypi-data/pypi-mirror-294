"""AssemblySystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2769

_ASSEMBLY_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "AssemblySystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1267
    from mastapy._private.nodal_analysis import _50
    from mastapy._private.shafts import _40
    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7716,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4143
    from mastapy._private.system_model.analyses_and_results.static_loads import _6966
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2770,
        _2782,
        _2784,
        _2786,
        _2793,
        _2794,
        _2797,
        _2799,
        _2803,
        _2805,
        _2811,
        _2818,
        _2819,
        _2822,
        _2826,
        _2839,
        _2841,
        _2842,
        _2843,
        _2848,
        _2856,
        _2859,
        _2863,
        _2864,
        _2867,
        _2868,
        _2870,
        _2871,
        _2874,
        _2876,
        _2877,
        _2878,
        _2880,
        _2883,
        _2886,
        _2887,
        _2890,
        _2894,
        _2898,
        _2900,
        _2903,
        _2910,
        _2916,
        _2920,
        _2923,
        _2926,
    )
    from mastapy._private.system_model.part_model import _2488

    Self = TypeVar("Self", bound="AssemblySystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="AssemblySystemDeflection._Cast_AssemblySystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AssemblySystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AssemblySystemDeflection:
    """Special nested class for casting AssemblySystemDeflection to subclasses."""

    __parent__: "AssemblySystemDeflection"

    @property
    def abstract_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2769.AbstractAssemblySystemDeflection":
        return self.__parent__._cast(_2769.AbstractAssemblySystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2871.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2871,
        )

        return self.__parent__._cast(_2871.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7716.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7716,
        )

        return self.__parent__._cast(_7716.PartFEAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7714.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2741.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2741

        return self.__parent__._cast(_2741.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2737.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2737

        return self.__parent__._cast(_2737.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2735.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.DesignEntityAnalysis)

    @property
    def root_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2886.RootAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2886,
        )

        return self.__parent__._cast(_2886.RootAssemblySystemDeflection)

    @property
    def assembly_system_deflection(self: "CastSelf") -> "AssemblySystemDeflection":
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
class AssemblySystemDeflection(_2769.AbstractAssemblySystemDeflection):
    """AssemblySystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ASSEMBLY_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def overall_bearing_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallBearingReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def overall_gear_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallGearReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def overall_oil_seal_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallOilSealReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def overall_shaft_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallShaftReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def overall_system_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverallSystemReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def analysis_settings(self: "Self") -> "_50.AnalysisSettingsItem":
        """mastapy.nodal_analysis.AnalysisSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2488.Assembly":
        """mastapy.system_model.part_model.Assembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_6966.AssemblyLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(self: "Self") -> "_4143.AssemblyPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.AssemblyPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rating_for_all_gear_sets(self: "Self") -> "_1267.GearSetGroupDutyCycle":
        """mastapy.gears.analysis.GearSetGroupDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingForAllGearSets")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def shaft_settings(self: "Self") -> "_40.ShaftSettingsItem":
        """mastapy.shafts.ShaftSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bearings(self: "Self") -> "List[_2782.BearingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bearings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def belt_drives(self: "Self") -> "List[_2784.BeltDriveSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BeltDriveSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltDrives")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_differential_gear_sets(
        self: "Self",
    ) -> "List[_2786.BevelDifferentialGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BevelDifferentialGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelDifferentialGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bolted_joints(self: "Self") -> "List[_2793.BoltedJointSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BoltedJointSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltedJoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bolts(self: "Self") -> "List[_2794.BoltSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BoltSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bolts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cv_ts(self: "Self") -> "List[_2818.CVTSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CVTSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CVTs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def clutches(self: "Self") -> "List[_2797.ClutchSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ClutchSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Clutches")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_details(self: "Self") -> "List[_2799.ComponentSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ComponentSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_couplings(
        self: "Self",
    ) -> "List[_2803.ConceptCouplingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConceptCouplingSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptCouplings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_gear_sets(self: "Self") -> "List[_2805.ConceptGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConceptGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_details(self: "Self") -> "List[_2811.ConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cycloidal_assemblies(
        self: "Self",
    ) -> "List[_2819.CycloidalAssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CycloidalAssemblySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cycloidal_discs(self: "Self") -> "List[_2822.CycloidalDiscSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CycloidalDiscSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalDiscs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_gear_sets(
        self: "Self",
    ) -> "List[_2826.CylindricalGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def fe_parts(self: "Self") -> "List[_2841.FEPartSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.FEPartSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEParts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def face_gear_sets(self: "Self") -> "List[_2839.FaceGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.FaceGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def flexible_pin_assemblies(
        self: "Self",
    ) -> "List[_2842.FlexiblePinAssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.FlexiblePinAssemblySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlexiblePinAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def hypoid_gear_sets(self: "Self") -> "List[_2848.HypoidGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.HypoidGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(
        self: "Self",
    ) -> "List[_2856.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearSets"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(
        self: "Self",
    ) -> "List[_2859.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidSpiralBevelGearSets"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def mass_discs(self: "Self") -> "List[_2863.MassDiscSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.MassDiscSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassDiscs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def measurement_components(
        self: "Self",
    ) -> "List[_2864.MeasurementComponentSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.MeasurementComponentSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeasurementComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def microphones(self: "Self") -> "List[_2867.MicrophoneSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.MicrophoneSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Microphones")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def mountable_component_details(
        self: "Self",
    ) -> "List[_2868.MountableComponentSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.MountableComponentSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MountableComponentDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def oil_seals(self: "Self") -> "List[_2870.OilSealSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.OilSealSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilSeals")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def part_to_part_shear_couplings(
        self: "Self",
    ) -> "List[_2874.PartToPartShearCouplingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.PartToPartShearCouplingSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartToPartShearCouplings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planet_carriers(self: "Self") -> "List[_2876.PlanetCarrierSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.PlanetCarrierSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetCarriers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def point_loads(self: "Self") -> "List[_2877.PointLoadSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.PointLoadSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def power_loads(self: "Self") -> "List[_2878.PowerLoadSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.PowerLoadSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def ring_pins(self: "Self") -> "List[_2880.RingPinsSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.RingPinsSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPins")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def rolling_bearings(self: "Self") -> "List[_2782.BearingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingBearings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def rolling_ring_assemblies(
        self: "Self",
    ) -> "List[_2883.RollingRingAssemblySystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.RollingRingAssemblySystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingRingAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shaft_hub_connections(
        self: "Self",
    ) -> "List[_2887.ShaftHubConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftHubConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftHubConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shafts(self: "Self") -> "List[_2890.ShaftSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ShaftSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shafts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shafts_and_housings(
        self: "Self",
    ) -> "List[_2770.AbstractShaftOrHousingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AbstractShaftOrHousingSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftsAndHousings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def sorted_converged_component_details(
        self: "Self",
    ) -> "List[_2799.ComponentSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ComponentSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SortedConvergedComponentDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def sorted_converged_connection_details(
        self: "Self",
    ) -> "List[_2811.ConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SortedConvergedConnectionDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def sorted_unconverged_component_details(
        self: "Self",
    ) -> "List[_2799.ComponentSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ComponentSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SortedUnconvergedComponentDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def sorted_unconverged_connection_details(
        self: "Self",
    ) -> "List[_2811.ConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SortedUnconvergedConnectionDetails"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def spiral_bevel_gear_sets(
        self: "Self",
    ) -> "List[_2894.SpiralBevelGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.SpiralBevelGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def spring_dampers(self: "Self") -> "List[_2898.SpringDamperSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.SpringDamperSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpringDampers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_gear_sets(
        self: "Self",
    ) -> "List[_2900.StraightBevelDiffGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelDiffGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_gear_sets(
        self: "Self",
    ) -> "List[_2903.StraightBevelGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def supercharger_rotor_sets(
        self: "Self",
    ) -> "List[_2826.CylindricalGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SuperchargerRotorSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def synchronisers(self: "Self") -> "List[_2910.SynchroniserSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.SynchroniserSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Synchronisers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def torque_converters(
        self: "Self",
    ) -> "List[_2916.TorqueConverterSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.TorqueConverterSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueConverters")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def unbalanced_masses(self: "Self") -> "List[_2920.UnbalancedMassSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.UnbalancedMassSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UnbalancedMasses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def unconverged_bearings_sorted_by_load(
        self: "Self",
    ) -> "List[_2782.BearingSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BearingSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UnconvergedBearingsSortedByLoad")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def unconverged_gear_meshes_sorted_by_power(
        self: "Self",
    ) -> "List[_2843.GearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.GearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UnconvergedGearMeshesSortedByPower"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def worm_gear_sets(self: "Self") -> "List[_2923.WormGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.WormGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_gear_sets(
        self: "Self",
    ) -> "List[_2926.ZerolBevelGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ZerolBevelGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AssemblySystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AssemblySystemDeflection
        """
        return _Cast_AssemblySystemDeflection(self)
