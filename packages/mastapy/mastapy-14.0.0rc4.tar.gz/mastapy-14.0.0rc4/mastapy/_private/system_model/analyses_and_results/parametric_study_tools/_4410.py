"""AGMAGleasonConicalGearSetParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4438,
)

_AGMA_GLEASON_CONICAL_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "AGMAGleasonConicalGearSetParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4404,
        _4408,
        _4409,
        _4417,
        _4422,
        _4471,
        _4475,
        _4503,
        _4522,
        _4525,
        _4531,
        _4534,
        _4552,
    )
    from mastapy._private.system_model.part_model.gears import _2571

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSetParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearSetParametricStudyTool._Cast_AGMAGleasonConicalGearSetParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSetParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSetParametricStudyTool:
    """Special nested class for casting AGMAGleasonConicalGearSetParametricStudyTool to subclasses."""

    __parent__: "AGMAGleasonConicalGearSetParametricStudyTool"

    @property
    def conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4438.ConicalGearSetParametricStudyTool":
        return self.__parent__._cast(_4438.ConicalGearSetParametricStudyTool)

    @property
    def gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4471.GearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4471,
        )

        return self.__parent__._cast(_4471.GearSetParametricStudyTool)

    @property
    def specialised_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4522.SpecialisedAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4522,
        )

        return self.__parent__._cast(_4522.SpecialisedAssemblyParametricStudyTool)

    @property
    def abstract_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4404.AbstractAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4404,
        )

        return self.__parent__._cast(_4404.AbstractAssemblyParametricStudyTool)

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "_4503.PartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4503,
        )

        return self.__parent__._cast(_4503.PartParametricStudyTool)

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
    def bevel_differential_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4417.BevelDifferentialGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4417,
        )

        return self.__parent__._cast(_4417.BevelDifferentialGearSetParametricStudyTool)

    @property
    def bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4422.BevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4422,
        )

        return self.__parent__._cast(_4422.BevelGearSetParametricStudyTool)

    @property
    def hypoid_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4475.HypoidGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4475,
        )

        return self.__parent__._cast(_4475.HypoidGearSetParametricStudyTool)

    @property
    def spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4525.SpiralBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4525,
        )

        return self.__parent__._cast(_4525.SpiralBevelGearSetParametricStudyTool)

    @property
    def straight_bevel_diff_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4531.StraightBevelDiffGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4531,
        )

        return self.__parent__._cast(_4531.StraightBevelDiffGearSetParametricStudyTool)

    @property
    def straight_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4534.StraightBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4534,
        )

        return self.__parent__._cast(_4534.StraightBevelGearSetParametricStudyTool)

    @property
    def zerol_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4552.ZerolBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4552,
        )

        return self.__parent__._cast(_4552.ZerolBevelGearSetParametricStudyTool)

    @property
    def agma_gleason_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearSetParametricStudyTool":
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
class AGMAGleasonConicalGearSetParametricStudyTool(
    _4438.ConicalGearSetParametricStudyTool
):
    """AGMAGleasonConicalGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_SET_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2571.AGMAGleasonConicalGearSet":
        """mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gears_parametric_study_tool(
        self: "Self",
    ) -> "List[_4409.AGMAGleasonConicalGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearsParametricStudyTool")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def agma_gleason_conical_gears_parametric_study_tool(
        self: "Self",
    ) -> "List[_4409.AGMAGleasonConicalGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalGearsParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_meshes_parametric_study_tool(
        self: "Self",
    ) -> "List[_4408.AGMAGleasonConicalGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshesParametricStudyTool")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def agma_gleason_conical_meshes_parametric_study_tool(
        self: "Self",
    ) -> "List[_4408.AGMAGleasonConicalGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalMeshesParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearSetParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSetParametricStudyTool
        """
        return _Cast_AGMAGleasonConicalGearSetParametricStudyTool(self)
