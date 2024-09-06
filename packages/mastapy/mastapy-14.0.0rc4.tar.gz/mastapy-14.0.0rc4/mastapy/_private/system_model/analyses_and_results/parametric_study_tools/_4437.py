"""ConicalGearParametricStudyTool"""

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
    _4470,
)

_CONICAL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ConicalGearParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7714
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4409,
        _4416,
        _4418,
        _4419,
        _4421,
        _4429,
        _4474,
        _4478,
        _4481,
        _4484,
        _4491,
        _4503,
        _4524,
        _4530,
        _4533,
        _4535,
        _4536,
        _4551,
    )
    from mastapy._private.system_model.part_model.gears import _2580

    Self = TypeVar("Self", bound="ConicalGearParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearParametricStudyTool._Cast_ConicalGearParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearParametricStudyTool:
    """Special nested class for casting ConicalGearParametricStudyTool to subclasses."""

    __parent__: "ConicalGearParametricStudyTool"

    @property
    def gear_parametric_study_tool(self: "CastSelf") -> "_4470.GearParametricStudyTool":
        return self.__parent__._cast(_4470.GearParametricStudyTool)

    @property
    def mountable_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4491.MountableComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4491,
        )

        return self.__parent__._cast(_4491.MountableComponentParametricStudyTool)

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4429.ComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4429,
        )

        return self.__parent__._cast(_4429.ComponentParametricStudyTool)

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
    def agma_gleason_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4409.AGMAGleasonConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4409,
        )

        return self.__parent__._cast(_4409.AGMAGleasonConicalGearParametricStudyTool)

    @property
    def bevel_differential_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4416.BevelDifferentialGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4416,
        )

        return self.__parent__._cast(_4416.BevelDifferentialGearParametricStudyTool)

    @property
    def bevel_differential_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4418.BevelDifferentialPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4418,
        )

        return self.__parent__._cast(
            _4418.BevelDifferentialPlanetGearParametricStudyTool
        )

    @property
    def bevel_differential_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4419.BevelDifferentialSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4419,
        )

        return self.__parent__._cast(_4419.BevelDifferentialSunGearParametricStudyTool)

    @property
    def bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4421.BevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4421,
        )

        return self.__parent__._cast(_4421.BevelGearParametricStudyTool)

    @property
    def hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4474.HypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4474,
        )

        return self.__parent__._cast(_4474.HypoidGearParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4478.KlingelnbergCycloPalloidConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4478,
        )

        return self.__parent__._cast(
            _4478.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4481.KlingelnbergCycloPalloidHypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4481,
        )

        return self.__parent__._cast(
            _4481.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4484.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4484,
        )

        return self.__parent__._cast(
            _4484.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        )

    @property
    def spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4524.SpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4524,
        )

        return self.__parent__._cast(_4524.SpiralBevelGearParametricStudyTool)

    @property
    def straight_bevel_diff_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4530.StraightBevelDiffGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4530,
        )

        return self.__parent__._cast(_4530.StraightBevelDiffGearParametricStudyTool)

    @property
    def straight_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4533.StraightBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4533,
        )

        return self.__parent__._cast(_4533.StraightBevelGearParametricStudyTool)

    @property
    def straight_bevel_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4535.StraightBevelPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4535,
        )

        return self.__parent__._cast(_4535.StraightBevelPlanetGearParametricStudyTool)

    @property
    def straight_bevel_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4536.StraightBevelSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4536,
        )

        return self.__parent__._cast(_4536.StraightBevelSunGearParametricStudyTool)

    @property
    def zerol_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4551.ZerolBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4551,
        )

        return self.__parent__._cast(_4551.ZerolBevelGearParametricStudyTool)

    @property
    def conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "ConicalGearParametricStudyTool":
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
class ConicalGearParametricStudyTool(_4470.GearParametricStudyTool):
    """ConicalGearParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_PARAMETRIC_STUDY_TOOL

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
    def planetaries(self: "Self") -> "List[ConicalGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearParametricStudyTool
        """
        return _Cast_ConicalGearParametricStudyTool(self)
