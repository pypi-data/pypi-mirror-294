"""AbstractAssemblyModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4776

_ABSTRACT_ASSEMBLY_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "AbstractAssemblyModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4690,
        _4691,
        _4694,
        _4697,
        _4702,
        _4703,
        _4707,
        _4709,
        _4712,
        _4715,
        _4718,
        _4724,
        _4726,
        _4728,
        _4734,
        _4743,
        _4745,
        _4747,
        _4749,
        _4753,
        _4757,
        _4760,
        _4763,
        _4766,
        _4779,
        _4781,
        _4788,
        _4791,
        _4796,
        _4799,
        _4802,
        _4805,
        _4808,
        _4812,
        _4816,
        _4826,
        _4829,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2769,
    )
    from mastapy._private.system_model.part_model import _2489

    Self = TypeVar("Self", bound="AbstractAssemblyModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyModalAnalysis._Cast_AbstractAssemblyModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyModalAnalysis:
    """Special nested class for casting AbstractAssemblyModalAnalysis to subclasses."""

    __parent__: "AbstractAssemblyModalAnalysis"

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4776.PartModalAnalysis":
        return self.__parent__._cast(_4776.PartModalAnalysis)

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
    def agma_gleason_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4690.AGMAGleasonConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4690,
        )

        return self.__parent__._cast(_4690.AGMAGleasonConicalGearSetModalAnalysis)

    @property
    def assembly_modal_analysis(self: "CastSelf") -> "_4691.AssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4691,
        )

        return self.__parent__._cast(_4691.AssemblyModalAnalysis)

    @property
    def belt_drive_modal_analysis(self: "CastSelf") -> "_4694.BeltDriveModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4694,
        )

        return self.__parent__._cast(_4694.BeltDriveModalAnalysis)

    @property
    def bevel_differential_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4697.BevelDifferentialGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4697,
        )

        return self.__parent__._cast(_4697.BevelDifferentialGearSetModalAnalysis)

    @property
    def bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4702.BevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4702,
        )

        return self.__parent__._cast(_4702.BevelGearSetModalAnalysis)

    @property
    def bolted_joint_modal_analysis(
        self: "CastSelf",
    ) -> "_4703.BoltedJointModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4703,
        )

        return self.__parent__._cast(_4703.BoltedJointModalAnalysis)

    @property
    def clutch_modal_analysis(self: "CastSelf") -> "_4707.ClutchModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4707,
        )

        return self.__parent__._cast(_4707.ClutchModalAnalysis)

    @property
    def concept_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4712.ConceptCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4712,
        )

        return self.__parent__._cast(_4712.ConceptCouplingModalAnalysis)

    @property
    def concept_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4715.ConceptGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4715,
        )

        return self.__parent__._cast(_4715.ConceptGearSetModalAnalysis)

    @property
    def conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4718.ConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4718,
        )

        return self.__parent__._cast(_4718.ConicalGearSetModalAnalysis)

    @property
    def coupling_modal_analysis(self: "CastSelf") -> "_4724.CouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4724,
        )

        return self.__parent__._cast(_4724.CouplingModalAnalysis)

    @property
    def cvt_modal_analysis(self: "CastSelf") -> "_4726.CVTModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4726,
        )

        return self.__parent__._cast(_4726.CVTModalAnalysis)

    @property
    def cycloidal_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4728.CycloidalAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4728,
        )

        return self.__parent__._cast(_4728.CycloidalAssemblyModalAnalysis)

    @property
    def cylindrical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4734.CylindricalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4734,
        )

        return self.__parent__._cast(_4734.CylindricalGearSetModalAnalysis)

    @property
    def face_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4743.FaceGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4743,
        )

        return self.__parent__._cast(_4743.FaceGearSetModalAnalysis)

    @property
    def flexible_pin_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4745.FlexiblePinAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4745,
        )

        return self.__parent__._cast(_4745.FlexiblePinAssemblyModalAnalysis)

    @property
    def gear_set_modal_analysis(self: "CastSelf") -> "_4749.GearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4749,
        )

        return self.__parent__._cast(_4749.GearSetModalAnalysis)

    @property
    def hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4753.HypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4753,
        )

        return self.__parent__._cast(_4753.HypoidGearSetModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4757.KlingelnbergCycloPalloidConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4757,
        )

        return self.__parent__._cast(
            _4757.KlingelnbergCycloPalloidConicalGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4760.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4760,
        )

        return self.__parent__._cast(
            _4760.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4763.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4763,
        )

        return self.__parent__._cast(
            _4763.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis
        )

    @property
    def microphone_array_modal_analysis(
        self: "CastSelf",
    ) -> "_4766.MicrophoneArrayModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4766,
        )

        return self.__parent__._cast(_4766.MicrophoneArrayModalAnalysis)

    @property
    def part_to_part_shear_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4779.PartToPartShearCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4779,
        )

        return self.__parent__._cast(_4779.PartToPartShearCouplingModalAnalysis)

    @property
    def planetary_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4781.PlanetaryGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4781,
        )

        return self.__parent__._cast(_4781.PlanetaryGearSetModalAnalysis)

    @property
    def rolling_ring_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4788.RollingRingAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4788,
        )

        return self.__parent__._cast(_4788.RollingRingAssemblyModalAnalysis)

    @property
    def root_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4791.RootAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4791,
        )

        return self.__parent__._cast(_4791.RootAssemblyModalAnalysis)

    @property
    def specialised_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4796.SpecialisedAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4796,
        )

        return self.__parent__._cast(_4796.SpecialisedAssemblyModalAnalysis)

    @property
    def spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4799.SpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4799,
        )

        return self.__parent__._cast(_4799.SpiralBevelGearSetModalAnalysis)

    @property
    def spring_damper_modal_analysis(
        self: "CastSelf",
    ) -> "_4802.SpringDamperModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4802,
        )

        return self.__parent__._cast(_4802.SpringDamperModalAnalysis)

    @property
    def straight_bevel_diff_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4805.StraightBevelDiffGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4805,
        )

        return self.__parent__._cast(_4805.StraightBevelDiffGearSetModalAnalysis)

    @property
    def straight_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4808.StraightBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4808,
        )

        return self.__parent__._cast(_4808.StraightBevelGearSetModalAnalysis)

    @property
    def synchroniser_modal_analysis(
        self: "CastSelf",
    ) -> "_4812.SynchroniserModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4812,
        )

        return self.__parent__._cast(_4812.SynchroniserModalAnalysis)

    @property
    def torque_converter_modal_analysis(
        self: "CastSelf",
    ) -> "_4816.TorqueConverterModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4816,
        )

        return self.__parent__._cast(_4816.TorqueConverterModalAnalysis)

    @property
    def worm_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4826.WormGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4826,
        )

        return self.__parent__._cast(_4826.WormGearSetModalAnalysis)

    @property
    def zerol_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4829.ZerolBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4829,
        )

        return self.__parent__._cast(_4829.ZerolBevelGearSetModalAnalysis)

    @property
    def abstract_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "AbstractAssemblyModalAnalysis":
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
class AbstractAssemblyModalAnalysis(_4776.PartModalAnalysis):
    """AbstractAssemblyModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_MODAL_ANALYSIS

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
    def gear_meshes(self: "Self") -> "List[_4747.GearMeshModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.GearMeshModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def rigidly_connected_groups(self: "Self") -> "List[_4709.ComponentModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ComponentModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RigidlyConnectedGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2769.AbstractAssemblySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.AbstractAssemblySystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyModalAnalysis
        """
        return _Cast_AbstractAssemblyModalAnalysis(self)
