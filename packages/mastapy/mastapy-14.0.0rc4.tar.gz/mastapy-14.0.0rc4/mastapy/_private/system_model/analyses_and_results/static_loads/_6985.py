"""ComponentLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7078

_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ComponentLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6955,
        _6956,
        _6961,
        _6967,
        _6970,
        _6973,
        _6974,
        _6975,
        _6979,
        _6981,
        _6987,
        _6989,
        _6992,
        _6998,
        _7000,
        _7004,
        _7007,
        _7009,
        _7014,
        _7017,
        _7031,
        _7032,
        _7035,
        _7038,
        _7044,
        _7053,
        _7060,
        _7063,
        _7066,
        _7069,
        _7070,
        _7073,
        _7074,
        _7076,
        _7080,
        _7085,
        _7088,
        _7089,
        _7090,
        _7093,
        _7097,
        _7099,
        _7100,
        _7103,
        _7107,
        _7109,
        _7112,
        _7115,
        _7116,
        _7117,
        _7119,
        _7120,
        _7124,
        _7125,
        _7130,
        _7131,
        _7132,
        _7135,
    )
    from mastapy._private.system_model.part_model import _2499

    Self = TypeVar("Self", bound="ComponentLoadCase")
    CastSelf = TypeVar("CastSelf", bound="ComponentLoadCase._Cast_ComponentLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("ComponentLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentLoadCase:
    """Special nested class for casting ComponentLoadCase to subclasses."""

    __parent__: "ComponentLoadCase"

    @property
    def part_load_case(self: "CastSelf") -> "_7078.PartLoadCase":
        return self.__parent__._cast(_7078.PartLoadCase)

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
    def abstract_shaft_load_case(self: "CastSelf") -> "_6955.AbstractShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6955,
        )

        return self.__parent__._cast(_6955.AbstractShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_6956.AbstractShaftOrHousingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6956,
        )

        return self.__parent__._cast(_6956.AbstractShaftOrHousingLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_6961.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6961,
        )

        return self.__parent__._cast(_6961.AGMAGleasonConicalGearLoadCase)

    @property
    def bearing_load_case(self: "CastSelf") -> "_6967.BearingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6967,
        )

        return self.__parent__._cast(_6967.BearingLoadCase)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_6970.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6970,
        )

        return self.__parent__._cast(_6970.BevelDifferentialGearLoadCase)

    @property
    def bevel_differential_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_6973.BevelDifferentialPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6973,
        )

        return self.__parent__._cast(_6973.BevelDifferentialPlanetGearLoadCase)

    @property
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_6974.BevelDifferentialSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6974,
        )

        return self.__parent__._cast(_6974.BevelDifferentialSunGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_6975.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6975,
        )

        return self.__parent__._cast(_6975.BevelGearLoadCase)

    @property
    def bolt_load_case(self: "CastSelf") -> "_6979.BoltLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6979,
        )

        return self.__parent__._cast(_6979.BoltLoadCase)

    @property
    def clutch_half_load_case(self: "CastSelf") -> "_6981.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6981,
        )

        return self.__parent__._cast(_6981.ClutchHalfLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_6987.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6987,
        )

        return self.__parent__._cast(_6987.ConceptCouplingHalfLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_6989.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6989,
        )

        return self.__parent__._cast(_6989.ConceptGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_6992.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6992,
        )

        return self.__parent__._cast(_6992.ConicalGearLoadCase)

    @property
    def connector_load_case(self: "CastSelf") -> "_6998.ConnectorLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6998,
        )

        return self.__parent__._cast(_6998.ConnectorLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7000.CouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7000,
        )

        return self.__parent__._cast(_7000.CouplingHalfLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7004.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7004,
        )

        return self.__parent__._cast(_7004.CVTPulleyLoadCase)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7007.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7007,
        )

        return self.__parent__._cast(_7007.CycloidalDiscLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_7009.CylindricalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7009,
        )

        return self.__parent__._cast(_7009.CylindricalGearLoadCase)

    @property
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7014.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7014,
        )

        return self.__parent__._cast(_7014.CylindricalPlanetGearLoadCase)

    @property
    def datum_load_case(self: "CastSelf") -> "_7017.DatumLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7017,
        )

        return self.__parent__._cast(_7017.DatumLoadCase)

    @property
    def external_cad_model_load_case(
        self: "CastSelf",
    ) -> "_7031.ExternalCADModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7031,
        )

        return self.__parent__._cast(_7031.ExternalCADModelLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_7032.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7032,
        )

        return self.__parent__._cast(_7032.FaceGearLoadCase)

    @property
    def fe_part_load_case(self: "CastSelf") -> "_7035.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7035,
        )

        return self.__parent__._cast(_7035.FEPartLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7038.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7038,
        )

        return self.__parent__._cast(_7038.GearLoadCase)

    @property
    def guide_dxf_model_load_case(self: "CastSelf") -> "_7044.GuideDxfModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7044,
        )

        return self.__parent__._cast(_7044.GuideDxfModelLoadCase)

    @property
    def hypoid_gear_load_case(self: "CastSelf") -> "_7053.HypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7053,
        )

        return self.__parent__._cast(_7053.HypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7060.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7060,
        )

        return self.__parent__._cast(_7060.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7063.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7063,
        )

        return self.__parent__._cast(_7063.KlingelnbergCycloPalloidHypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7066.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7066,
        )

        return self.__parent__._cast(
            _7066.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        )

    @property
    def mass_disc_load_case(self: "CastSelf") -> "_7069.MassDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7069,
        )

        return self.__parent__._cast(_7069.MassDiscLoadCase)

    @property
    def measurement_component_load_case(
        self: "CastSelf",
    ) -> "_7070.MeasurementComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7070,
        )

        return self.__parent__._cast(_7070.MeasurementComponentLoadCase)

    @property
    def microphone_load_case(self: "CastSelf") -> "_7073.MicrophoneLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7073,
        )

        return self.__parent__._cast(_7073.MicrophoneLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7074.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7074,
        )

        return self.__parent__._cast(_7074.MountableComponentLoadCase)

    @property
    def oil_seal_load_case(self: "CastSelf") -> "_7076.OilSealLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7076,
        )

        return self.__parent__._cast(_7076.OilSealLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7080.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7080,
        )

        return self.__parent__._cast(_7080.PartToPartShearCouplingHalfLoadCase)

    @property
    def planet_carrier_load_case(self: "CastSelf") -> "_7085.PlanetCarrierLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7085,
        )

        return self.__parent__._cast(_7085.PlanetCarrierLoadCase)

    @property
    def point_load_load_case(self: "CastSelf") -> "_7088.PointLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7088,
        )

        return self.__parent__._cast(_7088.PointLoadLoadCase)

    @property
    def power_load_load_case(self: "CastSelf") -> "_7089.PowerLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7089,
        )

        return self.__parent__._cast(_7089.PowerLoadLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7090.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7090,
        )

        return self.__parent__._cast(_7090.PulleyLoadCase)

    @property
    def ring_pins_load_case(self: "CastSelf") -> "_7093.RingPinsLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7093,
        )

        return self.__parent__._cast(_7093.RingPinsLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7097.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7097,
        )

        return self.__parent__._cast(_7097.RollingRingLoadCase)

    @property
    def shaft_hub_connection_load_case(
        self: "CastSelf",
    ) -> "_7099.ShaftHubConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7099,
        )

        return self.__parent__._cast(_7099.ShaftHubConnectionLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7100.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7100,
        )

        return self.__parent__._cast(_7100.ShaftLoadCase)

    @property
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7103.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7103,
        )

        return self.__parent__._cast(_7103.SpiralBevelGearLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7107.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7107,
        )

        return self.__parent__._cast(_7107.SpringDamperHalfLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7109.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7109,
        )

        return self.__parent__._cast(_7109.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7112.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7112,
        )

        return self.__parent__._cast(_7112.StraightBevelGearLoadCase)

    @property
    def straight_bevel_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7115.StraightBevelPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7115,
        )

        return self.__parent__._cast(_7115.StraightBevelPlanetGearLoadCase)

    @property
    def straight_bevel_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7116.StraightBevelSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7116,
        )

        return self.__parent__._cast(_7116.StraightBevelSunGearLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7117.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7117,
        )

        return self.__parent__._cast(_7117.SynchroniserHalfLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7119.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7119,
        )

        return self.__parent__._cast(_7119.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7120.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7120,
        )

        return self.__parent__._cast(_7120.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7124.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7124,
        )

        return self.__parent__._cast(_7124.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7125.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7125,
        )

        return self.__parent__._cast(_7125.TorqueConverterTurbineLoadCase)

    @property
    def unbalanced_mass_load_case(self: "CastSelf") -> "_7130.UnbalancedMassLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7130,
        )

        return self.__parent__._cast(_7130.UnbalancedMassLoadCase)

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7131.VirtualComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7131,
        )

        return self.__parent__._cast(_7131.VirtualComponentLoadCase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_7132.WormGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7132,
        )

        return self.__parent__._cast(_7132.WormGearLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7135.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7135,
        )

        return self.__parent__._cast(_7135.ZerolBevelGearLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "ComponentLoadCase":
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
class ComponentLoadCase(_7078.PartLoadCase):
    """ComponentLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def additional_modal_damping_ratio(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalModalDampingRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @additional_modal_damping_ratio.setter
    @enforce_parameter_types
    def additional_modal_damping_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AdditionalModalDampingRatio", value)

    @property
    def is_connected_to_ground(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsConnectedToGround")

        if temp is None:
            return False

        return temp

    @property
    def is_torsionally_free(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsTorsionallyFree")

        if temp is None:
            return False

        return temp

    @property
    def magnitude_of_rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MagnitudeOfRotation")

        if temp is None:
            return 0.0

        return temp

    @magnitude_of_rotation.setter
    @enforce_parameter_types
    def magnitude_of_rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MagnitudeOfRotation",
            float(value) if value is not None else 0.0,
        )

    @property
    def rayleigh_damping_beta(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingBeta")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rayleigh_damping_beta.setter
    @enforce_parameter_types
    def rayleigh_damping_beta(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RayleighDampingBeta", value)

    @property
    def rotation_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAngle")

        if temp is None:
            return 0.0

        return temp

    @rotation_angle.setter
    @enforce_parameter_types
    def rotation_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RotationAngle", float(value) if value is not None else 0.0
        )

    @property
    def component_design(self: "Self") -> "_2499.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ComponentLoadCase
        """
        return _Cast_ComponentLoadCase(self)
