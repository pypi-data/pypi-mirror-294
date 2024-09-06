"""BevelGearCompoundSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _2941,
)

_BEVEL_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "BevelGearCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2792,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2948,
        _2951,
        _2952,
        _2962,
        _2969,
        _2996,
        _3017,
        _3019,
        _3040,
        _3046,
        _3049,
        _3052,
        _3053,
        _3067,
    )

    Self = TypeVar("Self", bound="BevelGearCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearCompoundSystemDeflection._Cast_BevelGearCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearCompoundSystemDeflection:
    """Special nested class for casting BevelGearCompoundSystemDeflection to subclasses."""

    __parent__: "BevelGearCompoundSystemDeflection"

    @property
    def agma_gleason_conical_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2941.AGMAGleasonConicalGearCompoundSystemDeflection":
        return self.__parent__._cast(
            _2941.AGMAGleasonConicalGearCompoundSystemDeflection
        )

    @property
    def conical_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2969.ConicalGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2969,
        )

        return self.__parent__._cast(_2969.ConicalGearCompoundSystemDeflection)

    @property
    def gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2996.GearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2996,
        )

        return self.__parent__._cast(_2996.GearCompoundSystemDeflection)

    @property
    def mountable_component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3017.MountableComponentCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3017,
        )

        return self.__parent__._cast(_3017.MountableComponentCompoundSystemDeflection)

    @property
    def component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2962.ComponentCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2962,
        )

        return self.__parent__._cast(_2962.ComponentCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3019.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3019,
        )

        return self.__parent__._cast(_3019.PartCompoundSystemDeflection)

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
    def bevel_differential_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2948.BevelDifferentialGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2948,
        )

        return self.__parent__._cast(
            _2948.BevelDifferentialGearCompoundSystemDeflection
        )

    @property
    def bevel_differential_planet_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2951.BevelDifferentialPlanetGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2951,
        )

        return self.__parent__._cast(
            _2951.BevelDifferentialPlanetGearCompoundSystemDeflection
        )

    @property
    def bevel_differential_sun_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2952.BevelDifferentialSunGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2952,
        )

        return self.__parent__._cast(
            _2952.BevelDifferentialSunGearCompoundSystemDeflection
        )

    @property
    def spiral_bevel_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3040.SpiralBevelGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3040,
        )

        return self.__parent__._cast(_3040.SpiralBevelGearCompoundSystemDeflection)

    @property
    def straight_bevel_diff_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3046.StraightBevelDiffGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3046,
        )

        return self.__parent__._cast(
            _3046.StraightBevelDiffGearCompoundSystemDeflection
        )

    @property
    def straight_bevel_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3049.StraightBevelGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3049,
        )

        return self.__parent__._cast(_3049.StraightBevelGearCompoundSystemDeflection)

    @property
    def straight_bevel_planet_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3052.StraightBevelPlanetGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3052,
        )

        return self.__parent__._cast(
            _3052.StraightBevelPlanetGearCompoundSystemDeflection
        )

    @property
    def straight_bevel_sun_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3053.StraightBevelSunGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3053,
        )

        return self.__parent__._cast(_3053.StraightBevelSunGearCompoundSystemDeflection)

    @property
    def zerol_bevel_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3067.ZerolBevelGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3067,
        )

        return self.__parent__._cast(_3067.ZerolBevelGearCompoundSystemDeflection)

    @property
    def bevel_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "BevelGearCompoundSystemDeflection":
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
class BevelGearCompoundSystemDeflection(
    _2941.AGMAGleasonConicalGearCompoundSystemDeflection
):
    """BevelGearCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_2792.BevelGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BevelGearSystemDeflection]

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
    ) -> "List[_2792.BevelGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.BevelGearSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_BevelGearCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_BevelGearCompoundSystemDeflection
        """
        return _Cast_BevelGearCompoundSystemDeflection(self)
