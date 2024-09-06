"""SpecialisedAssemblyModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5237,
)

_SPECIALISED_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "SpecialisedAssemblyModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5243,
        _5247,
        _5250,
        _5255,
        _5256,
        _5260,
        _5265,
        _5268,
        _5271,
        _5276,
        _5278,
        _5280,
        _5286,
        _5292,
        _5294,
        _5297,
        _5301,
        _5305,
        _5308,
        _5311,
        _5314,
        _5319,
        _5322,
        _5324,
        _5331,
        _5341,
        _5344,
        _5347,
        _5350,
        _5354,
        _5358,
        _5365,
        _5368,
    )
    from mastapy._private.system_model.part_model import _2533

    Self = TypeVar("Self", bound="SpecialisedAssemblyModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyModalAnalysisAtASpeed._Cast_SpecialisedAssemblyModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyModalAnalysisAtASpeed:
    """Special nested class for casting SpecialisedAssemblyModalAnalysisAtASpeed to subclasses."""

    __parent__: "SpecialisedAssemblyModalAnalysisAtASpeed"

    @property
    def abstract_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5237.AbstractAssemblyModalAnalysisAtASpeed":
        return self.__parent__._cast(_5237.AbstractAssemblyModalAnalysisAtASpeed)

    @property
    def part_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5319.PartModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5319,
        )

        return self.__parent__._cast(_5319.PartModalAnalysisAtASpeed)

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
    def agma_gleason_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5243.AGMAGleasonConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5243,
        )

        return self.__parent__._cast(
            _5243.AGMAGleasonConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def belt_drive_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5247.BeltDriveModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5247,
        )

        return self.__parent__._cast(_5247.BeltDriveModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5250.BevelDifferentialGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5250,
        )

        return self.__parent__._cast(
            _5250.BevelDifferentialGearSetModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5255.BevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5255,
        )

        return self.__parent__._cast(_5255.BevelGearSetModalAnalysisAtASpeed)

    @property
    def bolted_joint_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5256.BoltedJointModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5256,
        )

        return self.__parent__._cast(_5256.BoltedJointModalAnalysisAtASpeed)

    @property
    def clutch_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5260.ClutchModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5260,
        )

        return self.__parent__._cast(_5260.ClutchModalAnalysisAtASpeed)

    @property
    def concept_coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5265.ConceptCouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5265,
        )

        return self.__parent__._cast(_5265.ConceptCouplingModalAnalysisAtASpeed)

    @property
    def concept_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5268.ConceptGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5268,
        )

        return self.__parent__._cast(_5268.ConceptGearSetModalAnalysisAtASpeed)

    @property
    def conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5271.ConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5271,
        )

        return self.__parent__._cast(_5271.ConicalGearSetModalAnalysisAtASpeed)

    @property
    def coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5276.CouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5276,
        )

        return self.__parent__._cast(_5276.CouplingModalAnalysisAtASpeed)

    @property
    def cvt_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5278.CVTModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5278,
        )

        return self.__parent__._cast(_5278.CVTModalAnalysisAtASpeed)

    @property
    def cycloidal_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5280.CycloidalAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5280,
        )

        return self.__parent__._cast(_5280.CycloidalAssemblyModalAnalysisAtASpeed)

    @property
    def cylindrical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5286.CylindricalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5286,
        )

        return self.__parent__._cast(_5286.CylindricalGearSetModalAnalysisAtASpeed)

    @property
    def face_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5292.FaceGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5292,
        )

        return self.__parent__._cast(_5292.FaceGearSetModalAnalysisAtASpeed)

    @property
    def flexible_pin_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5294.FlexiblePinAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5294,
        )

        return self.__parent__._cast(_5294.FlexiblePinAssemblyModalAnalysisAtASpeed)

    @property
    def gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5297.GearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5297,
        )

        return self.__parent__._cast(_5297.GearSetModalAnalysisAtASpeed)

    @property
    def hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5301.HypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5301,
        )

        return self.__parent__._cast(_5301.HypoidGearSetModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5305.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5305,
        )

        return self.__parent__._cast(
            _5305.KlingelnbergCycloPalloidConicalGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5308.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5308,
        )

        return self.__parent__._cast(
            _5308.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5311.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5311,
        )

        return self.__parent__._cast(
            _5311.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtASpeed
        )

    @property
    def microphone_array_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5314.MicrophoneArrayModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5314,
        )

        return self.__parent__._cast(_5314.MicrophoneArrayModalAnalysisAtASpeed)

    @property
    def part_to_part_shear_coupling_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5322.PartToPartShearCouplingModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5322,
        )

        return self.__parent__._cast(_5322.PartToPartShearCouplingModalAnalysisAtASpeed)

    @property
    def planetary_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5324.PlanetaryGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5324,
        )

        return self.__parent__._cast(_5324.PlanetaryGearSetModalAnalysisAtASpeed)

    @property
    def rolling_ring_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5331.RollingRingAssemblyModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5331,
        )

        return self.__parent__._cast(_5331.RollingRingAssemblyModalAnalysisAtASpeed)

    @property
    def spiral_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5341.SpiralBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5341,
        )

        return self.__parent__._cast(_5341.SpiralBevelGearSetModalAnalysisAtASpeed)

    @property
    def spring_damper_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5344.SpringDamperModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5344,
        )

        return self.__parent__._cast(_5344.SpringDamperModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5347.StraightBevelDiffGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5347,
        )

        return self.__parent__._cast(
            _5347.StraightBevelDiffGearSetModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5350.StraightBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5350,
        )

        return self.__parent__._cast(_5350.StraightBevelGearSetModalAnalysisAtASpeed)

    @property
    def synchroniser_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5354.SynchroniserModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5354,
        )

        return self.__parent__._cast(_5354.SynchroniserModalAnalysisAtASpeed)

    @property
    def torque_converter_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5358.TorqueConverterModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5358,
        )

        return self.__parent__._cast(_5358.TorqueConverterModalAnalysisAtASpeed)

    @property
    def worm_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5365.WormGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5365,
        )

        return self.__parent__._cast(_5365.WormGearSetModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_set_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5368.ZerolBevelGearSetModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5368,
        )

        return self.__parent__._cast(_5368.ZerolBevelGearSetModalAnalysisAtASpeed)

    @property
    def specialised_assembly_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyModalAnalysisAtASpeed":
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
class SpecialisedAssemblyModalAnalysisAtASpeed(
    _5237.AbstractAssemblyModalAnalysisAtASpeed
):
    """SpecialisedAssemblyModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2533.SpecialisedAssembly":
        """mastapy.system_model.part_model.SpecialisedAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssemblyModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyModalAnalysisAtASpeed
        """
        return _Cast_SpecialisedAssemblyModalAnalysisAtASpeed(self)
