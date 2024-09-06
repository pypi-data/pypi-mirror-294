"""InterMountableComponentConnectionCompoundPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4308,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "InterMountableComponentConnectionCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4204
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4278,
        _4282,
        _4285,
        _4290,
        _4295,
        _4300,
        _4303,
        _4306,
        _4311,
        _4313,
        _4321,
        _4327,
        _4332,
        _4336,
        _4340,
        _4343,
        _4346,
        _4356,
        _4365,
        _4368,
        _4375,
        _4378,
        _4381,
        _4384,
        _4393,
        _4399,
        _4402,
    )

    Self = TypeVar("Self", bound="InterMountableComponentConnectionCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundPowerFlow._Cast_InterMountableComponentConnectionCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundPowerFlow:
    """Special nested class for casting InterMountableComponentConnectionCompoundPowerFlow to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundPowerFlow"

    @property
    def connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4308.ConnectionCompoundPowerFlow":
        return self.__parent__._cast(_4308.ConnectionCompoundPowerFlow)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7708.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7708,
        )

        return self.__parent__._cast(_7708.ConnectionCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7712.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2735.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2735

        return self.__parent__._cast(_2735.DesignEntityAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4278.AGMAGleasonConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4278,
        )

        return self.__parent__._cast(_4278.AGMAGleasonConicalGearMeshCompoundPowerFlow)

    @property
    def belt_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4282.BeltConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4282,
        )

        return self.__parent__._cast(_4282.BeltConnectionCompoundPowerFlow)

    @property
    def bevel_differential_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4285.BevelDifferentialGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4285,
        )

        return self.__parent__._cast(_4285.BevelDifferentialGearMeshCompoundPowerFlow)

    @property
    def bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4290.BevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4290,
        )

        return self.__parent__._cast(_4290.BevelGearMeshCompoundPowerFlow)

    @property
    def clutch_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4295.ClutchConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4295,
        )

        return self.__parent__._cast(_4295.ClutchConnectionCompoundPowerFlow)

    @property
    def concept_coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4300.ConceptCouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4300,
        )

        return self.__parent__._cast(_4300.ConceptCouplingConnectionCompoundPowerFlow)

    @property
    def concept_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4303.ConceptGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4303,
        )

        return self.__parent__._cast(_4303.ConceptGearMeshCompoundPowerFlow)

    @property
    def conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4306.ConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4306,
        )

        return self.__parent__._cast(_4306.ConicalGearMeshCompoundPowerFlow)

    @property
    def coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4311.CouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4311,
        )

        return self.__parent__._cast(_4311.CouplingConnectionCompoundPowerFlow)

    @property
    def cvt_belt_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4313.CVTBeltConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4313,
        )

        return self.__parent__._cast(_4313.CVTBeltConnectionCompoundPowerFlow)

    @property
    def cylindrical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4321.CylindricalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4321,
        )

        return self.__parent__._cast(_4321.CylindricalGearMeshCompoundPowerFlow)

    @property
    def face_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4327.FaceGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4327,
        )

        return self.__parent__._cast(_4327.FaceGearMeshCompoundPowerFlow)

    @property
    def gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4332.GearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4332,
        )

        return self.__parent__._cast(_4332.GearMeshCompoundPowerFlow)

    @property
    def hypoid_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4336.HypoidGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4336,
        )

        return self.__parent__._cast(_4336.HypoidGearMeshCompoundPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4340.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4340,
        )

        return self.__parent__._cast(
            _4340.KlingelnbergCycloPalloidConicalGearMeshCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4343.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4343,
        )

        return self.__parent__._cast(
            _4343.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4346.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4346,
        )

        return self.__parent__._cast(
            _4346.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundPowerFlow
        )

    @property
    def part_to_part_shear_coupling_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4356.PartToPartShearCouplingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4356,
        )

        return self.__parent__._cast(
            _4356.PartToPartShearCouplingConnectionCompoundPowerFlow
        )

    @property
    def ring_pins_to_disc_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4365.RingPinsToDiscConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4365,
        )

        return self.__parent__._cast(_4365.RingPinsToDiscConnectionCompoundPowerFlow)

    @property
    def rolling_ring_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4368.RollingRingConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4368,
        )

        return self.__parent__._cast(_4368.RollingRingConnectionCompoundPowerFlow)

    @property
    def spiral_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4375.SpiralBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4375,
        )

        return self.__parent__._cast(_4375.SpiralBevelGearMeshCompoundPowerFlow)

    @property
    def spring_damper_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4378.SpringDamperConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4378,
        )

        return self.__parent__._cast(_4378.SpringDamperConnectionCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4381.StraightBevelDiffGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4381,
        )

        return self.__parent__._cast(_4381.StraightBevelDiffGearMeshCompoundPowerFlow)

    @property
    def straight_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4384.StraightBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4384,
        )

        return self.__parent__._cast(_4384.StraightBevelGearMeshCompoundPowerFlow)

    @property
    def torque_converter_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4393.TorqueConverterConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4393,
        )

        return self.__parent__._cast(_4393.TorqueConverterConnectionCompoundPowerFlow)

    @property
    def worm_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4399.WormGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4399,
        )

        return self.__parent__._cast(_4399.WormGearMeshCompoundPowerFlow)

    @property
    def zerol_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4402.ZerolBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4402,
        )

        return self.__parent__._cast(_4402.ZerolBevelGearMeshCompoundPowerFlow)

    @property
    def inter_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundPowerFlow":
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
class InterMountableComponentConnectionCompoundPowerFlow(
    _4308.ConnectionCompoundPowerFlow
):
    """InterMountableComponentConnectionCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4204.InterMountableComponentConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4204.InterMountableComponentConnectionPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundPowerFlow
        """
        return _Cast_InterMountableComponentConnectionCompoundPowerFlow(self)
