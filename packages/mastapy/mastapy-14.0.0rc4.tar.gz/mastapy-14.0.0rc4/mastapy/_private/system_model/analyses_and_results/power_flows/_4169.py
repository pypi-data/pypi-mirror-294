"""ConicalGearPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4198

_CONICAL_GEAR_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "ConicalGearPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4141,
        _4148,
        _4150,
        _4151,
        _4153,
        _4161,
        _4202,
        _4206,
        _4209,
        _4212,
        _4218,
        _4220,
        _4243,
        _4249,
        _4252,
        _4254,
        _4255,
        _4271,
    )
    from mastapy._private.system_model.part_model.gears import _2580

    Self = TypeVar("Self", bound="ConicalGearPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalGearPowerFlow._Cast_ConicalGearPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearPowerFlow:
    """Special nested class for casting ConicalGearPowerFlow to subclasses."""

    __parent__: "ConicalGearPowerFlow"

    @property
    def gear_power_flow(self: "CastSelf") -> "_4198.GearPowerFlow":
        return self.__parent__._cast(_4198.GearPowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4218.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4218

        return self.__parent__._cast(_4218.MountableComponentPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4161.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4161

        return self.__parent__._cast(_4161.ComponentPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "_4220.PartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4220

        return self.__parent__._cast(_4220.PartPowerFlow)

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
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4141.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4141

        return self.__parent__._cast(_4141.AGMAGleasonConicalGearPowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4148.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4148

        return self.__parent__._cast(_4148.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4150.BevelDifferentialPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4150

        return self.__parent__._cast(_4150.BevelDifferentialPlanetGearPowerFlow)

    @property
    def bevel_differential_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4151.BevelDifferentialSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4151

        return self.__parent__._cast(_4151.BevelDifferentialSunGearPowerFlow)

    @property
    def bevel_gear_power_flow(self: "CastSelf") -> "_4153.BevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4153

        return self.__parent__._cast(_4153.BevelGearPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4202.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4202

        return self.__parent__._cast(_4202.HypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4206.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4206

        return self.__parent__._cast(_4206.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4209

        return self.__parent__._cast(_4209.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4212.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4212

        return self.__parent__._cast(
            _4212.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4243.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4243

        return self.__parent__._cast(_4243.SpiralBevelGearPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4249.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4249

        return self.__parent__._cast(_4249.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4252.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4252

        return self.__parent__._cast(_4252.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4254.StraightBevelPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4254

        return self.__parent__._cast(_4254.StraightBevelPlanetGearPowerFlow)

    @property
    def straight_bevel_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4255.StraightBevelSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4255

        return self.__parent__._cast(_4255.StraightBevelSunGearPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4271.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4271

        return self.__parent__._cast(_4271.ZerolBevelGearPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "ConicalGearPowerFlow":
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
class ConicalGearPowerFlow(_4198.GearPowerFlow):
    """ConicalGearPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2580.ConicalGear":
        """mastapy.system_model.part_model.gears.ConicalGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearPowerFlow
        """
        return _Cast_ConicalGearPowerFlow(self)
