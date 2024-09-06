"""AbstractAssemblyCompoundPowerFlow"""

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
    _4354,
)

_ABSTRACT_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "AbstractAssemblyCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4136
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4279,
        _4280,
        _4283,
        _4286,
        _4291,
        _4293,
        _4294,
        _4299,
        _4304,
        _4307,
        _4310,
        _4314,
        _4316,
        _4322,
        _4328,
        _4330,
        _4333,
        _4337,
        _4341,
        _4344,
        _4347,
        _4350,
        _4355,
        _4359,
        _4366,
        _4369,
        _4373,
        _4376,
        _4377,
        _4382,
        _4385,
        _4388,
        _4392,
        _4400,
        _4403,
    )

    Self = TypeVar("Self", bound="AbstractAssemblyCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyCompoundPowerFlow._Cast_AbstractAssemblyCompoundPowerFlow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyCompoundPowerFlow:
    """Special nested class for casting AbstractAssemblyCompoundPowerFlow to subclasses."""

    __parent__: "AbstractAssemblyCompoundPowerFlow"

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4354.PartCompoundPowerFlow":
        return self.__parent__._cast(_4354.PartCompoundPowerFlow)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7715.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.PartCompoundAnalysis)

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
    def agma_gleason_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4279.AGMAGleasonConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4279,
        )

        return self.__parent__._cast(_4279.AGMAGleasonConicalGearSetCompoundPowerFlow)

    @property
    def assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4280.AssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4280,
        )

        return self.__parent__._cast(_4280.AssemblyCompoundPowerFlow)

    @property
    def belt_drive_compound_power_flow(
        self: "CastSelf",
    ) -> "_4283.BeltDriveCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4283,
        )

        return self.__parent__._cast(_4283.BeltDriveCompoundPowerFlow)

    @property
    def bevel_differential_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4286.BevelDifferentialGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4286,
        )

        return self.__parent__._cast(_4286.BevelDifferentialGearSetCompoundPowerFlow)

    @property
    def bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4291.BevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4291,
        )

        return self.__parent__._cast(_4291.BevelGearSetCompoundPowerFlow)

    @property
    def bolted_joint_compound_power_flow(
        self: "CastSelf",
    ) -> "_4293.BoltedJointCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4293,
        )

        return self.__parent__._cast(_4293.BoltedJointCompoundPowerFlow)

    @property
    def clutch_compound_power_flow(self: "CastSelf") -> "_4294.ClutchCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4294,
        )

        return self.__parent__._cast(_4294.ClutchCompoundPowerFlow)

    @property
    def concept_coupling_compound_power_flow(
        self: "CastSelf",
    ) -> "_4299.ConceptCouplingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4299,
        )

        return self.__parent__._cast(_4299.ConceptCouplingCompoundPowerFlow)

    @property
    def concept_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4304.ConceptGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4304,
        )

        return self.__parent__._cast(_4304.ConceptGearSetCompoundPowerFlow)

    @property
    def conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4307.ConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4307,
        )

        return self.__parent__._cast(_4307.ConicalGearSetCompoundPowerFlow)

    @property
    def coupling_compound_power_flow(
        self: "CastSelf",
    ) -> "_4310.CouplingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4310,
        )

        return self.__parent__._cast(_4310.CouplingCompoundPowerFlow)

    @property
    def cvt_compound_power_flow(self: "CastSelf") -> "_4314.CVTCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4314,
        )

        return self.__parent__._cast(_4314.CVTCompoundPowerFlow)

    @property
    def cycloidal_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4316.CycloidalAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4316,
        )

        return self.__parent__._cast(_4316.CycloidalAssemblyCompoundPowerFlow)

    @property
    def cylindrical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4322.CylindricalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4322,
        )

        return self.__parent__._cast(_4322.CylindricalGearSetCompoundPowerFlow)

    @property
    def face_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4328.FaceGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4328,
        )

        return self.__parent__._cast(_4328.FaceGearSetCompoundPowerFlow)

    @property
    def flexible_pin_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4330.FlexiblePinAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4330,
        )

        return self.__parent__._cast(_4330.FlexiblePinAssemblyCompoundPowerFlow)

    @property
    def gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4333.GearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4333,
        )

        return self.__parent__._cast(_4333.GearSetCompoundPowerFlow)

    @property
    def hypoid_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4337.HypoidGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4337,
        )

        return self.__parent__._cast(_4337.HypoidGearSetCompoundPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4341.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4341,
        )

        return self.__parent__._cast(
            _4341.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4344.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4344,
        )

        return self.__parent__._cast(
            _4344.KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4347.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4347,
        )

        return self.__parent__._cast(
            _4347.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundPowerFlow
        )

    @property
    def microphone_array_compound_power_flow(
        self: "CastSelf",
    ) -> "_4350.MicrophoneArrayCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4350,
        )

        return self.__parent__._cast(_4350.MicrophoneArrayCompoundPowerFlow)

    @property
    def part_to_part_shear_coupling_compound_power_flow(
        self: "CastSelf",
    ) -> "_4355.PartToPartShearCouplingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4355,
        )

        return self.__parent__._cast(_4355.PartToPartShearCouplingCompoundPowerFlow)

    @property
    def planetary_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4359.PlanetaryGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4359,
        )

        return self.__parent__._cast(_4359.PlanetaryGearSetCompoundPowerFlow)

    @property
    def rolling_ring_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4366.RollingRingAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4366,
        )

        return self.__parent__._cast(_4366.RollingRingAssemblyCompoundPowerFlow)

    @property
    def root_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4369.RootAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4369,
        )

        return self.__parent__._cast(_4369.RootAssemblyCompoundPowerFlow)

    @property
    def specialised_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4373.SpecialisedAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4373,
        )

        return self.__parent__._cast(_4373.SpecialisedAssemblyCompoundPowerFlow)

    @property
    def spiral_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4376.SpiralBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4376,
        )

        return self.__parent__._cast(_4376.SpiralBevelGearSetCompoundPowerFlow)

    @property
    def spring_damper_compound_power_flow(
        self: "CastSelf",
    ) -> "_4377.SpringDamperCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4377,
        )

        return self.__parent__._cast(_4377.SpringDamperCompoundPowerFlow)

    @property
    def straight_bevel_diff_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4382.StraightBevelDiffGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4382,
        )

        return self.__parent__._cast(_4382.StraightBevelDiffGearSetCompoundPowerFlow)

    @property
    def straight_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4385.StraightBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4385,
        )

        return self.__parent__._cast(_4385.StraightBevelGearSetCompoundPowerFlow)

    @property
    def synchroniser_compound_power_flow(
        self: "CastSelf",
    ) -> "_4388.SynchroniserCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4388,
        )

        return self.__parent__._cast(_4388.SynchroniserCompoundPowerFlow)

    @property
    def torque_converter_compound_power_flow(
        self: "CastSelf",
    ) -> "_4392.TorqueConverterCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4392,
        )

        return self.__parent__._cast(_4392.TorqueConverterCompoundPowerFlow)

    @property
    def worm_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4400.WormGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4400,
        )

        return self.__parent__._cast(_4400.WormGearSetCompoundPowerFlow)

    @property
    def zerol_bevel_gear_set_compound_power_flow(
        self: "CastSelf",
    ) -> "_4403.ZerolBevelGearSetCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4403,
        )

        return self.__parent__._cast(_4403.ZerolBevelGearSetCompoundPowerFlow)

    @property
    def abstract_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "AbstractAssemblyCompoundPowerFlow":
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
class AbstractAssemblyCompoundPowerFlow(_4354.PartCompoundPowerFlow):
    """AbstractAssemblyCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_4136.AbstractAssemblyPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.AbstractAssemblyPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4136.AbstractAssemblyPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.AbstractAssemblyPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyCompoundPowerFlow
        """
        return _Cast_AbstractAssemblyCompoundPowerFlow(self)
