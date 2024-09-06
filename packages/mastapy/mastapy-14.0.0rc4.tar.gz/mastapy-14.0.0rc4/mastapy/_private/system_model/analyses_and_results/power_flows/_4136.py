"""AbstractAssemblyPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows import _4220

_ABSTRACT_ASSEMBLY_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows",
    "AbstractAssemblyPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4142,
        _4143,
        _4146,
        _4149,
        _4154,
        _4155,
        _4159,
        _4164,
        _4167,
        _4170,
        _4175,
        _4177,
        _4179,
        _4186,
        _4192,
        _4196,
        _4199,
        _4203,
        _4207,
        _4210,
        _4213,
        _4216,
        _4223,
        _4225,
        _4234,
        _4237,
        _4241,
        _4244,
        _4247,
        _4250,
        _4253,
        _4258,
        _4262,
        _4269,
        _4272,
    )
    from mastapy._private.system_model.part_model import _2489

    Self = TypeVar("Self", bound="AbstractAssemblyPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractAssemblyPowerFlow._Cast_AbstractAssemblyPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyPowerFlow:
    """Special nested class for casting AbstractAssemblyPowerFlow to subclasses."""

    __parent__: "AbstractAssemblyPowerFlow"

    @property
    def part_power_flow(self: "CastSelf") -> "_4220.PartPowerFlow":
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
    def agma_gleason_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4142.AGMAGleasonConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4142

        return self.__parent__._cast(_4142.AGMAGleasonConicalGearSetPowerFlow)

    @property
    def assembly_power_flow(self: "CastSelf") -> "_4143.AssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4143

        return self.__parent__._cast(_4143.AssemblyPowerFlow)

    @property
    def belt_drive_power_flow(self: "CastSelf") -> "_4146.BeltDrivePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4146

        return self.__parent__._cast(_4146.BeltDrivePowerFlow)

    @property
    def bevel_differential_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4149.BevelDifferentialGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4149

        return self.__parent__._cast(_4149.BevelDifferentialGearSetPowerFlow)

    @property
    def bevel_gear_set_power_flow(self: "CastSelf") -> "_4154.BevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4154

        return self.__parent__._cast(_4154.BevelGearSetPowerFlow)

    @property
    def bolted_joint_power_flow(self: "CastSelf") -> "_4155.BoltedJointPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4155

        return self.__parent__._cast(_4155.BoltedJointPowerFlow)

    @property
    def clutch_power_flow(self: "CastSelf") -> "_4159.ClutchPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4159

        return self.__parent__._cast(_4159.ClutchPowerFlow)

    @property
    def concept_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4164.ConceptCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4164

        return self.__parent__._cast(_4164.ConceptCouplingPowerFlow)

    @property
    def concept_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4167.ConceptGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4167

        return self.__parent__._cast(_4167.ConceptGearSetPowerFlow)

    @property
    def conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4170.ConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4170

        return self.__parent__._cast(_4170.ConicalGearSetPowerFlow)

    @property
    def coupling_power_flow(self: "CastSelf") -> "_4175.CouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4175

        return self.__parent__._cast(_4175.CouplingPowerFlow)

    @property
    def cvt_power_flow(self: "CastSelf") -> "_4177.CVTPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4177

        return self.__parent__._cast(_4177.CVTPowerFlow)

    @property
    def cycloidal_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4179.CycloidalAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4179

        return self.__parent__._cast(_4179.CycloidalAssemblyPowerFlow)

    @property
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4186.CylindricalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4186

        return self.__parent__._cast(_4186.CylindricalGearSetPowerFlow)

    @property
    def face_gear_set_power_flow(self: "CastSelf") -> "_4192.FaceGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4192

        return self.__parent__._cast(_4192.FaceGearSetPowerFlow)

    @property
    def flexible_pin_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4196.FlexiblePinAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4196

        return self.__parent__._cast(_4196.FlexiblePinAssemblyPowerFlow)

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4199.GearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4199

        return self.__parent__._cast(_4199.GearSetPowerFlow)

    @property
    def hypoid_gear_set_power_flow(self: "CastSelf") -> "_4203.HypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4203

        return self.__parent__._cast(_4203.HypoidGearSetPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4207.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4207

        return self.__parent__._cast(
            _4207.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4210.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4210

        return self.__parent__._cast(
            _4210.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4213.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4213

        return self.__parent__._cast(
            _4213.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        )

    @property
    def microphone_array_power_flow(
        self: "CastSelf",
    ) -> "_4216.MicrophoneArrayPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4216

        return self.__parent__._cast(_4216.MicrophoneArrayPowerFlow)

    @property
    def part_to_part_shear_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4223.PartToPartShearCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4223

        return self.__parent__._cast(_4223.PartToPartShearCouplingPowerFlow)

    @property
    def planetary_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4225.PlanetaryGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4225

        return self.__parent__._cast(_4225.PlanetaryGearSetPowerFlow)

    @property
    def rolling_ring_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4234.RollingRingAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4234

        return self.__parent__._cast(_4234.RollingRingAssemblyPowerFlow)

    @property
    def root_assembly_power_flow(self: "CastSelf") -> "_4237.RootAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4237

        return self.__parent__._cast(_4237.RootAssemblyPowerFlow)

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4241.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4241

        return self.__parent__._cast(_4241.SpecialisedAssemblyPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4244.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4244

        return self.__parent__._cast(_4244.SpiralBevelGearSetPowerFlow)

    @property
    def spring_damper_power_flow(self: "CastSelf") -> "_4247.SpringDamperPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4247

        return self.__parent__._cast(_4247.SpringDamperPowerFlow)

    @property
    def straight_bevel_diff_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4250.StraightBevelDiffGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4250

        return self.__parent__._cast(_4250.StraightBevelDiffGearSetPowerFlow)

    @property
    def straight_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4253.StraightBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4253

        return self.__parent__._cast(_4253.StraightBevelGearSetPowerFlow)

    @property
    def synchroniser_power_flow(self: "CastSelf") -> "_4258.SynchroniserPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4258

        return self.__parent__._cast(_4258.SynchroniserPowerFlow)

    @property
    def torque_converter_power_flow(
        self: "CastSelf",
    ) -> "_4262.TorqueConverterPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4262

        return self.__parent__._cast(_4262.TorqueConverterPowerFlow)

    @property
    def worm_gear_set_power_flow(self: "CastSelf") -> "_4269.WormGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4269

        return self.__parent__._cast(_4269.WormGearSetPowerFlow)

    @property
    def zerol_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4272.ZerolBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4272

        return self.__parent__._cast(_4272.ZerolBevelGearSetPowerFlow)

    @property
    def abstract_assembly_power_flow(self: "CastSelf") -> "AbstractAssemblyPowerFlow":
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
class AbstractAssemblyPowerFlow(_4220.PartPowerFlow):
    """AbstractAssemblyPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2489.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2489.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyPowerFlow
        """
        return _Cast_AbstractAssemblyPowerFlow(self)
