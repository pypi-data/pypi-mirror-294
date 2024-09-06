"""BevelGearMeshParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4408,
)

_BEVEL_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "BevelGearMeshParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7707
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4415,
        _4436,
        _4439,
        _4469,
        _4476,
        _4523,
        _4529,
        _4532,
        _4550,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2357

    Self = TypeVar("Self", bound="BevelGearMeshParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearMeshParametricStudyTool._Cast_BevelGearMeshParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshParametricStudyTool:
    """Special nested class for casting BevelGearMeshParametricStudyTool to subclasses."""

    __parent__: "BevelGearMeshParametricStudyTool"

    @property
    def agma_gleason_conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4408.AGMAGleasonConicalGearMeshParametricStudyTool":
        return self.__parent__._cast(
            _4408.AGMAGleasonConicalGearMeshParametricStudyTool
        )

    @property
    def conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4436.ConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4436,
        )

        return self.__parent__._cast(_4436.ConicalGearMeshParametricStudyTool)

    @property
    def gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4469.GearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4469,
        )

        return self.__parent__._cast(_4469.GearMeshParametricStudyTool)

    @property
    def inter_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4476.InterMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4476,
        )

        return self.__parent__._cast(
            _4476.InterMountableComponentConnectionParametricStudyTool
        )

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4439.ConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4439,
        )

        return self.__parent__._cast(_4439.ConnectionParametricStudyTool)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7707.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7707,
        )

        return self.__parent__._cast(_7707.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2733.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2733

        return self.__parent__._cast(_2733.ConnectionAnalysis)

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
    def bevel_differential_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4415.BevelDifferentialGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4415,
        )

        return self.__parent__._cast(_4415.BevelDifferentialGearMeshParametricStudyTool)

    @property
    def spiral_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4523.SpiralBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4523,
        )

        return self.__parent__._cast(_4523.SpiralBevelGearMeshParametricStudyTool)

    @property
    def straight_bevel_diff_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4529.StraightBevelDiffGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4529,
        )

        return self.__parent__._cast(_4529.StraightBevelDiffGearMeshParametricStudyTool)

    @property
    def straight_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4532.StraightBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4532,
        )

        return self.__parent__._cast(_4532.StraightBevelGearMeshParametricStudyTool)

    @property
    def zerol_bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4550.ZerolBevelGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4550,
        )

        return self.__parent__._cast(_4550.ZerolBevelGearMeshParametricStudyTool)

    @property
    def bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "BevelGearMeshParametricStudyTool":
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
class BevelGearMeshParametricStudyTool(
    _4408.AGMAGleasonConicalGearMeshParametricStudyTool
):
    """BevelGearMeshParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_MESH_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2357.BevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.BevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearMeshParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshParametricStudyTool
        """
        return _Cast_BevelGearMeshParametricStudyTool(self)
