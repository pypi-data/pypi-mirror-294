"""GearSetSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.system_deflections import _2892

_GEAR_SET_IMPLEMENTATION_DETAIL = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetImplementationDetail"
)
_GEAR_SET_MODES = python_net_import("SMT.MastaAPI.Gears", "GearSetModes")
_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_BOOLEAN = python_net_import("System", "Boolean")
_GEAR_SET_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "GearSetSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private import _7728
    from mastapy._private.gears import _341
    from mastapy._private.gears.analysis import _1268, _1271
    from mastapy._private.gears.rating import _376
    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7716,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4199
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2769,
        _2774,
        _2786,
        _2791,
        _2805,
        _2809,
        _2826,
        _2827,
        _2828,
        _2839,
        _2843,
        _2845,
        _2848,
        _2853,
        _2856,
        _2859,
        _2871,
        _2894,
        _2900,
        _2903,
        _2923,
        _2926,
    )
    from mastapy._private.system_model.part_model.gears import _2589

    Self = TypeVar("Self", bound="GearSetSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetSystemDeflection._Cast_GearSetSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetSystemDeflection:
    """Special nested class for casting GearSetSystemDeflection to subclasses."""

    __parent__: "GearSetSystemDeflection"

    @property
    def specialised_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2892.SpecialisedAssemblySystemDeflection":
        return self.__parent__._cast(_2892.SpecialisedAssemblySystemDeflection)

    @property
    def abstract_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2769.AbstractAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2769,
        )

        return self.__parent__._cast(_2769.AbstractAssemblySystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2871.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2871,
        )

        return self.__parent__._cast(_2871.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7716.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7716,
        )

        return self.__parent__._cast(_7716.PartFEAnalysis)

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
    def agma_gleason_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2774.AGMAGleasonConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2774,
        )

        return self.__parent__._cast(_2774.AGMAGleasonConicalGearSetSystemDeflection)

    @property
    def bevel_differential_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2786.BevelDifferentialGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2786,
        )

        return self.__parent__._cast(_2786.BevelDifferentialGearSetSystemDeflection)

    @property
    def bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2791.BevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2791,
        )

        return self.__parent__._cast(_2791.BevelGearSetSystemDeflection)

    @property
    def concept_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2805.ConceptGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2805,
        )

        return self.__parent__._cast(_2805.ConceptGearSetSystemDeflection)

    @property
    def conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2809.ConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2809,
        )

        return self.__parent__._cast(_2809.ConicalGearSetSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2826.CylindricalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2826,
        )

        return self.__parent__._cast(_2826.CylindricalGearSetSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2827.CylindricalGearSetSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2827,
        )

        return self.__parent__._cast(_2827.CylindricalGearSetSystemDeflectionTimestep)

    @property
    def cylindrical_gear_set_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2828.CylindricalGearSetSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2828,
        )

        return self.__parent__._cast(
            _2828.CylindricalGearSetSystemDeflectionWithLTCAResults
        )

    @property
    def face_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2839.FaceGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2839,
        )

        return self.__parent__._cast(_2839.FaceGearSetSystemDeflection)

    @property
    def hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2848.HypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2848,
        )

        return self.__parent__._cast(_2848.HypoidGearSetSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2853.KlingelnbergCycloPalloidConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2853,
        )

        return self.__parent__._cast(
            _2853.KlingelnbergCycloPalloidConicalGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2856.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2856,
        )

        return self.__parent__._cast(
            _2856.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2859.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2859,
        )

        return self.__parent__._cast(
            _2859.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
        )

    @property
    def spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2894.SpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2894,
        )

        return self.__parent__._cast(_2894.SpiralBevelGearSetSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2900.StraightBevelDiffGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2900,
        )

        return self.__parent__._cast(_2900.StraightBevelDiffGearSetSystemDeflection)

    @property
    def straight_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2903.StraightBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2903,
        )

        return self.__parent__._cast(_2903.StraightBevelGearSetSystemDeflection)

    @property
    def worm_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2923.WormGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2923,
        )

        return self.__parent__._cast(_2923.WormGearSetSystemDeflection)

    @property
    def zerol_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2926.ZerolBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2926,
        )

        return self.__parent__._cast(_2926.ZerolBevelGearSetSystemDeflection)

    @property
    def gear_set_system_deflection(self: "CastSelf") -> "GearSetSystemDeflection":
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
class GearSetSystemDeflection(_2892.SpecialisedAssemblySystemDeflection):
    """GearSetSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2589.GearSet":
        """mastapy.system_model.part_model.gears.GearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rating(self: "Self") -> "_376.GearSetRating":
        """mastapy.gears.rating.GearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears_system_deflection(self: "Self") -> "List[_2845.GearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.GearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsSystemDeflection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes_system_deflection(
        self: "Self",
    ) -> "List[_2843.GearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.GearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesSystemDeflection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def power_flow_results(self: "Self") -> "_4199.GearSetPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def analysis_for(
        self: "Self",
        gear_set_imp_detail: "_1271.GearSetImplementationDetail",
        gear_set_mode: "_341.GearSetModes",
    ) -> "_1268.GearSetImplementationAnalysis":
        """mastapy.gears.analysis.GearSetImplementationAnalysis

        Args:
            gear_set_imp_detail (mastapy.gears.analysis.GearSetImplementationDetail)
            gear_set_mode (mastapy.gears.GearSetModes)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        method_result = pythonnet_method_call(
            self.wrapped,
            "AnalysisFor",
            gear_set_imp_detail.wrapped if gear_set_imp_detail else None,
            gear_set_mode,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def implementation_detail_results_failed_for(
        self: "Self",
        gear_set_imp_detail: "_1271.GearSetImplementationDetail",
        gear_set_mode: "_341.GearSetModes",
    ) -> "bool":
        """bool

        Args:
            gear_set_imp_detail (mastapy.gears.analysis.GearSetImplementationDetail)
            gear_set_mode (mastapy.gears.GearSetModes)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        method_result = pythonnet_method_call(
            self.wrapped,
            "ImplementationDetailResultsFailedFor",
            gear_set_imp_detail.wrapped if gear_set_imp_detail else None,
            gear_set_mode,
        )
        return method_result

    @enforce_parameter_types
    def perform_implementation_detail_analysis_with_progress(
        self: "Self",
        imp_detail: "_1271.GearSetImplementationDetail",
        gear_set_mode: "_341.GearSetModes",
        progress: "_7728.TaskProgress",
        run_all_planetary_meshes: "bool" = True,
    ) -> None:
        """Method does not return.

        Args:
            imp_detail (mastapy.gears.analysis.GearSetImplementationDetail)
            gear_set_mode (mastapy.gears.GearSetModes)
            progress (mastapy.TaskProgress)
            run_all_planetary_meshes (bool, optional)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformImplementationDetailAnalysis",
            [
                _GEAR_SET_IMPLEMENTATION_DETAIL,
                _GEAR_SET_MODES,
                _TASK_PROGRESS,
                _BOOLEAN,
            ],
            imp_detail.wrapped if imp_detail else None,
            gear_set_mode,
            progress.wrapped if progress else None,
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )

    @enforce_parameter_types
    def perform_implementation_detail_analysis(
        self: "Self",
        imp_detail: "_1271.GearSetImplementationDetail",
        gear_set_mode: "_341.GearSetModes",
        run_all_planetary_meshes: "bool" = True,
    ) -> None:
        """Method does not return.

        Args:
            imp_detail (mastapy.gears.analysis.GearSetImplementationDetail)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool, optional)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformImplementationDetailAnalysis",
            [_GEAR_SET_IMPLEMENTATION_DETAIL, _GEAR_SET_MODES, _BOOLEAN],
            imp_detail.wrapped if imp_detail else None,
            gear_set_mode,
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_GearSetSystemDeflection
        """
        return _Cast_GearSetSystemDeflection(self)
