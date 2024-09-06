"""ConicalGearSetCompoundSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _2998,
)

_CONICAL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "ConicalGearSetCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.conical import _554
    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2809,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2937,
        _2943,
        _2950,
        _2955,
        _3002,
        _3006,
        _3009,
        _3012,
        _3019,
        _3039,
        _3042,
        _3048,
        _3051,
        _3069,
    )

    Self = TypeVar("Self", bound="ConicalGearSetCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetCompoundSystemDeflection._Cast_ConicalGearSetCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetCompoundSystemDeflection:
    """Special nested class for casting ConicalGearSetCompoundSystemDeflection to subclasses."""

    __parent__: "ConicalGearSetCompoundSystemDeflection"

    @property
    def gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2998.GearSetCompoundSystemDeflection":
        return self.__parent__._cast(_2998.GearSetCompoundSystemDeflection)

    @property
    def specialised_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3039.SpecialisedAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3039,
        )

        return self.__parent__._cast(_3039.SpecialisedAssemblyCompoundSystemDeflection)

    @property
    def abstract_assembly_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2937.AbstractAssemblyCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2937,
        )

        return self.__parent__._cast(_2937.AbstractAssemblyCompoundSystemDeflection)

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
    def agma_gleason_conical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2943.AGMAGleasonConicalGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2943,
        )

        return self.__parent__._cast(
            _2943.AGMAGleasonConicalGearSetCompoundSystemDeflection
        )

    @property
    def bevel_differential_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2950.BevelDifferentialGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2950,
        )

        return self.__parent__._cast(
            _2950.BevelDifferentialGearSetCompoundSystemDeflection
        )

    @property
    def bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2955.BevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2955,
        )

        return self.__parent__._cast(_2955.BevelGearSetCompoundSystemDeflection)

    @property
    def hypoid_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3002.HypoidGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3002,
        )

        return self.__parent__._cast(_3002.HypoidGearSetCompoundSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3006.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3006,
        )

        return self.__parent__._cast(
            _3006.KlingelnbergCycloPalloidConicalGearSetCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3009.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3009,
        )

        return self.__parent__._cast(
            _3009.KlingelnbergCycloPalloidHypoidGearSetCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3012.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3012,
        )

        return self.__parent__._cast(
            _3012.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSystemDeflection
        )

    @property
    def spiral_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3042.SpiralBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3042,
        )

        return self.__parent__._cast(_3042.SpiralBevelGearSetCompoundSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3048.StraightBevelDiffGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3048,
        )

        return self.__parent__._cast(
            _3048.StraightBevelDiffGearSetCompoundSystemDeflection
        )

    @property
    def straight_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3051.StraightBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3051,
        )

        return self.__parent__._cast(_3051.StraightBevelGearSetCompoundSystemDeflection)

    @property
    def zerol_bevel_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3069.ZerolBevelGearSetCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3069,
        )

        return self.__parent__._cast(_3069.ZerolBevelGearSetCompoundSystemDeflection)

    @property
    def conical_gear_set_compound_system_deflection(
        self: "CastSelf",
    ) -> "ConicalGearSetCompoundSystemDeflection":
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
class ConicalGearSetCompoundSystemDeflection(_2998.GearSetCompoundSystemDeflection):
    """ConicalGearSetCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def conical_gear_set_duty_cycle_rating(
        self: "Self",
    ) -> "_554.ConicalGearSetDutyCycleRating":
        """mastapy.gears.rating.conical.ConicalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDutyCycleRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_2809.ConicalGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSetSystemDeflection]

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
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2809.ConicalGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSetSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetCompoundSystemDeflection
        """
        return _Cast_ConicalGearSetCompoundSystemDeflection(self)
