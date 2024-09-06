"""AGMAGleasonConicalGearCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6581,
)

_AGMA_GLEASON_CONICAL_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "AGMAGleasonConicalGearCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6420,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6560,
        _6563,
        _6564,
        _6565,
        _6574,
        _6607,
        _6611,
        _6628,
        _6630,
        _6650,
        _6656,
        _6659,
        _6662,
        _6663,
        _6677,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearCompoundDynamicAnalysis._Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearCompoundDynamicAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearCompoundDynamicAnalysis"

    @property
    def conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6581.ConicalGearCompoundDynamicAnalysis":
        return self.__parent__._cast(_6581.ConicalGearCompoundDynamicAnalysis)

    @property
    def gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6607.GearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6607,
        )

        return self.__parent__._cast(_6607.GearCompoundDynamicAnalysis)

    @property
    def mountable_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6628.MountableComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6628,
        )

        return self.__parent__._cast(_6628.MountableComponentCompoundDynamicAnalysis)

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6574.ComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6574,
        )

        return self.__parent__._cast(_6574.ComponentCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6630.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6630,
        )

        return self.__parent__._cast(_6630.PartCompoundDynamicAnalysis)

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
    def bevel_differential_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6560.BevelDifferentialGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6560,
        )

        return self.__parent__._cast(_6560.BevelDifferentialGearCompoundDynamicAnalysis)

    @property
    def bevel_differential_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6563.BevelDifferentialPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6563,
        )

        return self.__parent__._cast(
            _6563.BevelDifferentialPlanetGearCompoundDynamicAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6564.BevelDifferentialSunGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6564,
        )

        return self.__parent__._cast(
            _6564.BevelDifferentialSunGearCompoundDynamicAnalysis
        )

    @property
    def bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6565.BevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6565,
        )

        return self.__parent__._cast(_6565.BevelGearCompoundDynamicAnalysis)

    @property
    def hypoid_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6611.HypoidGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6611,
        )

        return self.__parent__._cast(_6611.HypoidGearCompoundDynamicAnalysis)

    @property
    def spiral_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6650.SpiralBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6650,
        )

        return self.__parent__._cast(_6650.SpiralBevelGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6656.StraightBevelDiffGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6656,
        )

        return self.__parent__._cast(_6656.StraightBevelDiffGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6659.StraightBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6659,
        )

        return self.__parent__._cast(_6659.StraightBevelGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6662.StraightBevelPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6662,
        )

        return self.__parent__._cast(
            _6662.StraightBevelPlanetGearCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6663.StraightBevelSunGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6663,
        )

        return self.__parent__._cast(_6663.StraightBevelSunGearCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6677.ZerolBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6677,
        )

        return self.__parent__._cast(_6677.ZerolBevelGearCompoundDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearCompoundDynamicAnalysis":
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
class AGMAGleasonConicalGearCompoundDynamicAnalysis(
    _6581.ConicalGearCompoundDynamicAnalysis
):
    """AGMAGleasonConicalGearCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6420.AGMAGleasonConicalGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6420.AGMAGleasonConicalGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AGMAGleasonConicalGearDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis
        """
        return _Cast_AGMAGleasonConicalGearCompoundDynamicAnalysis(self)
