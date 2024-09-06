"""GearMeshLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7059

_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearMeshLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6962,
        _6971,
        _6976,
        _6990,
        _6994,
        _6997,
        _7011,
        _7033,
        _7042,
        _7054,
        _7061,
        _7064,
        _7067,
        _7104,
        _7110,
        _7113,
        _7133,
        _7136,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2367

    Self = TypeVar("Self", bound="GearMeshLoadCase")
    CastSelf = TypeVar("CastSelf", bound="GearMeshLoadCase._Cast_GearMeshLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshLoadCase:
    """Special nested class for casting GearMeshLoadCase to subclasses."""

    __parent__: "GearMeshLoadCase"

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7059.InterMountableComponentConnectionLoadCase":
        return self.__parent__._cast(_7059.InterMountableComponentConnectionLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "_6997.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6997,
        )

        return self.__parent__._cast(_6997.ConnectionLoadCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2733.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2733

        return self.__parent__._cast(_2733.ConnectionAnalysis)

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
    def agma_gleason_conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6962.AGMAGleasonConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6962,
        )

        return self.__parent__._cast(_6962.AGMAGleasonConicalGearMeshLoadCase)

    @property
    def bevel_differential_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6971.BevelDifferentialGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6971,
        )

        return self.__parent__._cast(_6971.BevelDifferentialGearMeshLoadCase)

    @property
    def bevel_gear_mesh_load_case(self: "CastSelf") -> "_6976.BevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6976,
        )

        return self.__parent__._cast(_6976.BevelGearMeshLoadCase)

    @property
    def concept_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6990.ConceptGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6990,
        )

        return self.__parent__._cast(_6990.ConceptGearMeshLoadCase)

    @property
    def conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_6994.ConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6994,
        )

        return self.__parent__._cast(_6994.ConicalGearMeshLoadCase)

    @property
    def cylindrical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7011.CylindricalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7011,
        )

        return self.__parent__._cast(_7011.CylindricalGearMeshLoadCase)

    @property
    def face_gear_mesh_load_case(self: "CastSelf") -> "_7033.FaceGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7033,
        )

        return self.__parent__._cast(_7033.FaceGearMeshLoadCase)

    @property
    def hypoid_gear_mesh_load_case(self: "CastSelf") -> "_7054.HypoidGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7054,
        )

        return self.__parent__._cast(_7054.HypoidGearMeshLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7061.KlingelnbergCycloPalloidConicalGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7061,
        )

        return self.__parent__._cast(
            _7061.KlingelnbergCycloPalloidConicalGearMeshLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7064.KlingelnbergCycloPalloidHypoidGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7064,
        )

        return self.__parent__._cast(
            _7064.KlingelnbergCycloPalloidHypoidGearMeshLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7067.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7067,
        )

        return self.__parent__._cast(
            _7067.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase
        )

    @property
    def spiral_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7104.SpiralBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7104,
        )

        return self.__parent__._cast(_7104.SpiralBevelGearMeshLoadCase)

    @property
    def straight_bevel_diff_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7110.StraightBevelDiffGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7110,
        )

        return self.__parent__._cast(_7110.StraightBevelDiffGearMeshLoadCase)

    @property
    def straight_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7113.StraightBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7113,
        )

        return self.__parent__._cast(_7113.StraightBevelGearMeshLoadCase)

    @property
    def worm_gear_mesh_load_case(self: "CastSelf") -> "_7133.WormGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7133,
        )

        return self.__parent__._cast(_7133.WormGearMeshLoadCase)

    @property
    def zerol_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7136.ZerolBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7136,
        )

        return self.__parent__._cast(_7136.ZerolBevelGearMeshLoadCase)

    @property
    def gear_mesh_load_case(self: "CastSelf") -> "GearMeshLoadCase":
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
class GearMeshLoadCase(_7059.InterMountableComponentConnectionLoadCase):
    """GearMeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def minimum_power_for_gear_mesh_to_be_loaded(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumPowerForGearMeshToBeLoaded")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_power_for_gear_mesh_to_be_loaded.setter
    @enforce_parameter_types
    def minimum_power_for_gear_mesh_to_be_loaded(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumPowerForGearMeshToBeLoaded", value)

    @property
    def minimum_torque_for_gear_mesh_to_be_loaded(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumTorqueForGearMeshToBeLoaded"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_torque_for_gear_mesh_to_be_loaded.setter
    @enforce_parameter_types
    def minimum_torque_for_gear_mesh_to_be_loaded(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumTorqueForGearMeshToBeLoaded", value
        )

    @property
    def number_of_steps_for_one_tooth_pass(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfStepsForOneToothPass")

        if temp is None:
            return 0

        return temp

    @property
    def number_of_teeth_passed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethPassed")

        if temp is None:
            return 0.0

        return temp

    @number_of_teeth_passed.setter
    @enforce_parameter_types
    def number_of_teeth_passed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTeethPassed",
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
    def connection_design(self: "Self") -> "_2367.GearMesh":
        """mastapy.system_model.connections_and_sockets.gears.GearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def get_harmonic_load_data_for_import(
        self: "Self",
    ) -> "_7042.GearSetHarmonicLoadData":
        """mastapy.system_model.analyses_and_results.static_loads.GearSetHarmonicLoadData"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_GearMeshLoadCase
        """
        return _Cast_GearMeshLoadCase(self)
