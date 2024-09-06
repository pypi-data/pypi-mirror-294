"""InterMountableComponentConnectionLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _6997

_INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "InterMountableComponentConnectionLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6962,
        _6968,
        _6971,
        _6976,
        _6980,
        _6986,
        _6990,
        _6994,
        _6999,
        _7002,
        _7011,
        _7033,
        _7040,
        _7054,
        _7061,
        _7064,
        _7067,
        _7079,
        _7094,
        _7096,
        _7104,
        _7106,
        _7110,
        _7113,
        _7122,
        _7133,
        _7136,
    )
    from mastapy._private.system_model.connections_and_sockets import _2335

    Self = TypeVar("Self", bound="InterMountableComponentConnectionLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionLoadCase._Cast_InterMountableComponentConnectionLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionLoadCase:
    """Special nested class for casting InterMountableComponentConnectionLoadCase to subclasses."""

    __parent__: "InterMountableComponentConnectionLoadCase"

    @property
    def connection_load_case(self: "CastSelf") -> "_6997.ConnectionLoadCase":
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
    def belt_connection_load_case(self: "CastSelf") -> "_6968.BeltConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6968,
        )

        return self.__parent__._cast(_6968.BeltConnectionLoadCase)

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
    def clutch_connection_load_case(
        self: "CastSelf",
    ) -> "_6980.ClutchConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6980,
        )

        return self.__parent__._cast(_6980.ClutchConnectionLoadCase)

    @property
    def concept_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_6986.ConceptCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6986,
        )

        return self.__parent__._cast(_6986.ConceptCouplingConnectionLoadCase)

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
    def coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_6999.CouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6999,
        )

        return self.__parent__._cast(_6999.CouplingConnectionLoadCase)

    @property
    def cvt_belt_connection_load_case(
        self: "CastSelf",
    ) -> "_7002.CVTBeltConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7002,
        )

        return self.__parent__._cast(_7002.CVTBeltConnectionLoadCase)

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
    def gear_mesh_load_case(self: "CastSelf") -> "_7040.GearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7040,
        )

        return self.__parent__._cast(_7040.GearMeshLoadCase)

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
    def part_to_part_shear_coupling_connection_load_case(
        self: "CastSelf",
    ) -> "_7079.PartToPartShearCouplingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7079,
        )

        return self.__parent__._cast(_7079.PartToPartShearCouplingConnectionLoadCase)

    @property
    def ring_pins_to_disc_connection_load_case(
        self: "CastSelf",
    ) -> "_7094.RingPinsToDiscConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7094,
        )

        return self.__parent__._cast(_7094.RingPinsToDiscConnectionLoadCase)

    @property
    def rolling_ring_connection_load_case(
        self: "CastSelf",
    ) -> "_7096.RollingRingConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7096,
        )

        return self.__parent__._cast(_7096.RollingRingConnectionLoadCase)

    @property
    def spiral_bevel_gear_mesh_load_case(
        self: "CastSelf",
    ) -> "_7104.SpiralBevelGearMeshLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7104,
        )

        return self.__parent__._cast(_7104.SpiralBevelGearMeshLoadCase)

    @property
    def spring_damper_connection_load_case(
        self: "CastSelf",
    ) -> "_7106.SpringDamperConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7106,
        )

        return self.__parent__._cast(_7106.SpringDamperConnectionLoadCase)

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
    def torque_converter_connection_load_case(
        self: "CastSelf",
    ) -> "_7122.TorqueConverterConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7122,
        )

        return self.__parent__._cast(_7122.TorqueConverterConnectionLoadCase)

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
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionLoadCase":
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
class InterMountableComponentConnectionLoadCase(_6997.ConnectionLoadCase):
    """InterMountableComponentConnectionLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION_LOAD_CASE

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
    def connection_design(self: "Self") -> "_2335.InterMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.InterMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_InterMountableComponentConnectionLoadCase":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionLoadCase
        """
        return _Cast_InterMountableComponentConnectionLoadCase(self)
