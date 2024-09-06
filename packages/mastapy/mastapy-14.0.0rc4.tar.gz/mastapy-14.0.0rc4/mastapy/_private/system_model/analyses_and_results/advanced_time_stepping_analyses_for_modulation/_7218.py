"""GearAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7240,
)

_GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "GearAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7163,
        _7171,
        _7174,
        _7175,
        _7176,
        _7185,
        _7189,
        _7192,
        _7207,
        _7210,
        _7213,
        _7223,
        _7227,
        _7230,
        _7233,
        _7242,
        _7262,
        _7268,
        _7271,
        _7274,
        _7275,
        _7286,
        _7289,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2845,
    )
    from mastapy._private.system_model.part_model.gears import _2587

    Self = TypeVar("Self", bound="GearAdvancedTimeSteppingAnalysisForModulation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearAdvancedTimeSteppingAnalysisForModulation._Cast_GearAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting GearAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "GearAdvancedTimeSteppingAnalysisForModulation"

    @property
    def mountable_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7240.MountableComponentAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7240.MountableComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7185.ComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7185,
        )

        return self.__parent__._cast(
            _7185.ComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7242.PartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7242,
        )

        return self.__parent__._cast(
            _7242.PartAdvancedTimeSteppingAnalysisForModulation
        )

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
    def agma_gleason_conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7163.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7163,
        )

        return self.__parent__._cast(
            _7163.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7171.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7171,
        )

        return self.__parent__._cast(
            _7171.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7174.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7174,
        )

        return self.__parent__._cast(
            _7174.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_sun_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7175.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7175,
        )

        return self.__parent__._cast(
            _7175.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7176.BevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7176,
        )

        return self.__parent__._cast(
            _7176.BevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7189.ConceptGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7189,
        )

        return self.__parent__._cast(
            _7189.ConceptGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7192.ConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7192,
        )

        return self.__parent__._cast(
            _7192.ConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7207.CylindricalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7207,
        )

        return self.__parent__._cast(
            _7207.CylindricalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7210.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7210,
        )

        return self.__parent__._cast(
            _7210.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7213.FaceGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7213,
        )

        return self.__parent__._cast(
            _7213.FaceGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7223.HypoidGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7223,
        )

        return self.__parent__._cast(
            _7223.HypoidGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7227.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7227,
        )

        return self.__parent__._cast(
            _7227.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7230.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7230,
        )

        return self.__parent__._cast(
            _7230.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7233.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7233,
        )

        return self.__parent__._cast(
            _7233.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7262.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7262,
        )

        return self.__parent__._cast(
            _7262.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7268.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7268,
        )

        return self.__parent__._cast(
            _7268.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7271.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7271,
        )

        return self.__parent__._cast(
            _7271.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7274.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7274,
        )

        return self.__parent__._cast(
            _7274.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_sun_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7275.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7275,
        )

        return self.__parent__._cast(
            _7275.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7286.WormGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7286,
        )

        return self.__parent__._cast(
            _7286.WormGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7289.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7289,
        )

        return self.__parent__._cast(
            _7289.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "GearAdvancedTimeSteppingAnalysisForModulation":
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
class GearAdvancedTimeSteppingAnalysisForModulation(
    _7240.MountableComponentAdvancedTimeSteppingAnalysisForModulation
):
    """GearAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2587.Gear":
        """mastapy.system_model.part_model.gears.Gear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: "Self") -> "_2845.GearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.GearSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_GearAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_GearAdvancedTimeSteppingAnalysisForModulation(self)
