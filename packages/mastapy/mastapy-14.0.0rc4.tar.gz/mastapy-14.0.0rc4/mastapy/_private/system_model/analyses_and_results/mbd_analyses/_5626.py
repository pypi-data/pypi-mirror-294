"""StraightBevelDiffGearSetMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5521

_STRAIGHT_BEVEL_DIFF_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "StraightBevelDiffGearSetMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5500,
        _5506,
        _5538,
        _5565,
        _5594,
        _5616,
        _5624,
        _5625,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7111
    from mastapy._private.system_model.part_model.gears import _2603

    Self = TypeVar("Self", bound="StraightBevelDiffGearSetMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearSetMultibodyDynamicsAnalysis._Cast_StraightBevelDiffGearSetMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearSetMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearSetMultibodyDynamicsAnalysis:
    """Special nested class for casting StraightBevelDiffGearSetMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "StraightBevelDiffGearSetMultibodyDynamicsAnalysis"

    @property
    def bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5521.BevelGearSetMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5521.BevelGearSetMultibodyDynamicsAnalysis)

    @property
    def agma_gleason_conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5506.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5506,
        )

        return self.__parent__._cast(
            _5506.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis
        )

    @property
    def conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5538.ConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5538,
        )

        return self.__parent__._cast(_5538.ConicalGearSetMultibodyDynamicsAnalysis)

    @property
    def gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5565.GearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5565,
        )

        return self.__parent__._cast(_5565.GearSetMultibodyDynamicsAnalysis)

    @property
    def specialised_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5616.SpecialisedAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5616,
        )

        return self.__parent__._cast(_5616.SpecialisedAssemblyMultibodyDynamicsAnalysis)

    @property
    def abstract_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5500.AbstractAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5500,
        )

        return self.__parent__._cast(_5500.AbstractAssemblyMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5594.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5594,
        )

        return self.__parent__._cast(_5594.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7718.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartTimeSeriesLoadAnalysisCase)

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
    def straight_bevel_diff_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearSetMultibodyDynamicsAnalysis":
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
class StraightBevelDiffGearSetMultibodyDynamicsAnalysis(
    _5521.BevelGearSetMultibodyDynamicsAnalysis
):
    """StraightBevelDiffGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2603.StraightBevelDiffGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelDiffGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_7111.StraightBevelDiffGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gears_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5625.StraightBevelDiffGearMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelGearsMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_gears_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5625.StraightBevelDiffGearMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelDiffGearsMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_meshes_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5624.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelMeshesMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_meshes_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5624.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelDiffMeshesMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_StraightBevelDiffGearSetMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearSetMultibodyDynamicsAnalysis
        """
        return _Cast_StraightBevelDiffGearSetMultibodyDynamicsAnalysis(self)
