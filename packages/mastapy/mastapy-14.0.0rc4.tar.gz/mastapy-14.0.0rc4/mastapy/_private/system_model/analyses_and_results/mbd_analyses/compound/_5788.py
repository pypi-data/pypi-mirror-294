"""ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5676,
)

_ZEROL_BEVEL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5650
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5658,
        _5664,
        _5692,
        _5718,
        _5739,
        _5758,
        _5786,
        _5787,
    )
    from mastapy._private.system_model.part_model.gears import _2611

    Self = TypeVar("Self", bound="ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis._Cast_ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis"

    @property
    def bevel_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5676.BevelGearSetCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5676.BevelGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5664.AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5664,
        )

        return self.__parent__._cast(
            _5664.AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def conical_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5692.ConicalGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5692,
        )

        return self.__parent__._cast(
            _5692.ConicalGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5718.GearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5718,
        )

        return self.__parent__._cast(_5718.GearSetCompoundMultibodyDynamicsAnalysis)

    @property
    def specialised_assembly_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5758.SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5758,
        )

        return self.__parent__._cast(
            _5758.SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis
        )

    @property
    def abstract_assembly_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5658.AbstractAssemblyCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5658,
        )

        return self.__parent__._cast(
            _5658.AbstractAssemblyCompoundMultibodyDynamicsAnalysis
        )

    @property
    def part_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5739.PartCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5739,
        )

        return self.__parent__._cast(_5739.PartCompoundMultibodyDynamicsAnalysis)

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
    def zerol_bevel_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis":
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
class ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis(
    _5676.BevelGearSetCompoundMultibodyDynamicsAnalysis
):
    """ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2611.ZerolBevelGearSet":
        """mastapy.system_model.part_model.gears.ZerolBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2611.ZerolBevelGearSet":
        """mastapy.system_model.part_model.gears.ZerolBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5650.ZerolBevelGearSetMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.ZerolBevelGearSetMultibodyDynamicsAnalysis]

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
    def zerol_bevel_gears_compound_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5786.ZerolBevelGearCompoundMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.compound.ZerolBevelGearCompoundMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ZerolBevelGearsCompoundMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_meshes_compound_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5787.ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.compound.ZerolBevelGearMeshCompoundMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ZerolBevelMeshesCompoundMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5650.ZerolBevelGearSetMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.ZerolBevelGearSetMultibodyDynamicsAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis(self)
