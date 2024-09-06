"""ConicalGearMeshCompoundPowerFlow"""

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
    _4332,
)

_CONICAL_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "ConicalGearMeshCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4168
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4278,
        _4285,
        _4290,
        _4308,
        _4336,
        _4338,
        _4340,
        _4343,
        _4346,
        _4375,
        _4381,
        _4384,
        _4402,
    )

    Self = TypeVar("Self", bound="ConicalGearMeshCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshCompoundPowerFlow._Cast_ConicalGearMeshCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshCompoundPowerFlow:
    """Special nested class for casting ConicalGearMeshCompoundPowerFlow to subclasses."""

    __parent__: "ConicalGearMeshCompoundPowerFlow"

    @property
    def gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4332.GearMeshCompoundPowerFlow":
        return self.__parent__._cast(_4332.GearMeshCompoundPowerFlow)

    @property
    def inter_mountable_component_connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4338.InterMountableComponentConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4338,
        )

        return self.__parent__._cast(
            _4338.InterMountableComponentConnectionCompoundPowerFlow
        )

    @property
    def connection_compound_power_flow(
        self: "CastSelf",
    ) -> "_4308.ConnectionCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4308,
        )

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
    def spiral_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4375.SpiralBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4375,
        )

        return self.__parent__._cast(_4375.SpiralBevelGearMeshCompoundPowerFlow)

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
    def zerol_bevel_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "_4402.ZerolBevelGearMeshCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4402,
        )

        return self.__parent__._cast(_4402.ZerolBevelGearMeshCompoundPowerFlow)

    @property
    def conical_gear_mesh_compound_power_flow(
        self: "CastSelf",
    ) -> "ConicalGearMeshCompoundPowerFlow":
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
class ConicalGearMeshCompoundPowerFlow(_4332.GearMeshCompoundPowerFlow):
    """ConicalGearMeshCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4168.ConicalGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow]

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
    ) -> "List[_4168.ConicalGearMeshPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshCompoundPowerFlow
        """
        return _Cast_ConicalGearMeshCompoundPowerFlow(self)
