"""ConicalGearModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5296,
)

_CONICAL_GEAR_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "ConicalGearModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5242,
        _5249,
        _5251,
        _5252,
        _5254,
        _5262,
        _5300,
        _5304,
        _5307,
        _5310,
        _5317,
        _5319,
        _5340,
        _5346,
        _5349,
        _5351,
        _5352,
        _5367,
    )
    from mastapy._private.system_model.part_model.gears import _2580

    Self = TypeVar("Self", bound="ConicalGearModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearModalAnalysisAtASpeed._Cast_ConicalGearModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearModalAnalysisAtASpeed:
    """Special nested class for casting ConicalGearModalAnalysisAtASpeed to subclasses."""

    __parent__: "ConicalGearModalAnalysisAtASpeed"

    @property
    def gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5296.GearModalAnalysisAtASpeed":
        return self.__parent__._cast(_5296.GearModalAnalysisAtASpeed)

    @property
    def mountable_component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5317.MountableComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5317,
        )

        return self.__parent__._cast(_5317.MountableComponentModalAnalysisAtASpeed)

    @property
    def component_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5262.ComponentModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5262,
        )

        return self.__parent__._cast(_5262.ComponentModalAnalysisAtASpeed)

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
    def agma_gleason_conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5242.AGMAGleasonConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5242,
        )

        return self.__parent__._cast(_5242.AGMAGleasonConicalGearModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5249.BevelDifferentialGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5249,
        )

        return self.__parent__._cast(_5249.BevelDifferentialGearModalAnalysisAtASpeed)

    @property
    def bevel_differential_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5251.BevelDifferentialPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5251,
        )

        return self.__parent__._cast(
            _5251.BevelDifferentialPlanetGearModalAnalysisAtASpeed
        )

    @property
    def bevel_differential_sun_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5252.BevelDifferentialSunGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5252,
        )

        return self.__parent__._cast(
            _5252.BevelDifferentialSunGearModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5254.BevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5254,
        )

        return self.__parent__._cast(_5254.BevelGearModalAnalysisAtASpeed)

    @property
    def hypoid_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5300.HypoidGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5300,
        )

        return self.__parent__._cast(_5300.HypoidGearModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5304.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5304,
        )

        return self.__parent__._cast(
            _5304.KlingelnbergCycloPalloidConicalGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5307.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5307,
        )

        return self.__parent__._cast(
            _5307.KlingelnbergCycloPalloidHypoidGearModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5310.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5310,
        )

        return self.__parent__._cast(
            _5310.KlingelnbergCycloPalloidSpiralBevelGearModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5340.SpiralBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5340,
        )

        return self.__parent__._cast(_5340.SpiralBevelGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5346.StraightBevelDiffGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5346,
        )

        return self.__parent__._cast(_5346.StraightBevelDiffGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5349.StraightBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5349,
        )

        return self.__parent__._cast(_5349.StraightBevelGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_planet_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5351.StraightBevelPlanetGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5351,
        )

        return self.__parent__._cast(_5351.StraightBevelPlanetGearModalAnalysisAtASpeed)

    @property
    def straight_bevel_sun_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5352.StraightBevelSunGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5352,
        )

        return self.__parent__._cast(_5352.StraightBevelSunGearModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5367.ZerolBevelGearModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5367,
        )

        return self.__parent__._cast(_5367.ZerolBevelGearModalAnalysisAtASpeed)

    @property
    def conical_gear_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "ConicalGearModalAnalysisAtASpeed":
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
class ConicalGearModalAnalysisAtASpeed(_5296.GearModalAnalysisAtASpeed):
    """ConicalGearModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MODAL_ANALYSIS_AT_A_SPEED

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
    def planetaries(self: "Self") -> "List[ConicalGearModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.ConicalGearModalAnalysisAtASpeed]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearModalAnalysisAtASpeed
        """
        return _Cast_ConicalGearModalAnalysisAtASpeed(self)
