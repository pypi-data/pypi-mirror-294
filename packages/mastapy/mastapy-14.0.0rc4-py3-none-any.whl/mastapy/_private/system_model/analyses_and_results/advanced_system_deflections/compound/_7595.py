"""ConicalGearSetCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7621,
)

_CONICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "ConicalGearSetCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.conical import _554
    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7460,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7561,
        _7567,
        _7574,
        _7579,
        _7625,
        _7629,
        _7632,
        _7635,
        _7642,
        _7661,
        _7664,
        _7670,
        _7673,
        _7691,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )

    Self = TypeVar("Self", bound="ConicalGearSetCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetCompoundAdvancedSystemDeflection._Cast_ConicalGearSetCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetCompoundAdvancedSystemDeflection:
    """Special nested class for casting ConicalGearSetCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "ConicalGearSetCompoundAdvancedSystemDeflection"

    @property
    def gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7621.GearSetCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(_7621.GearSetCompoundAdvancedSystemDeflection)

    @property
    def specialised_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7661.SpecialisedAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7661,
        )

        return self.__parent__._cast(
            _7661.SpecialisedAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def abstract_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7561.AbstractAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7561,
        )

        return self.__parent__._cast(
            _7561.AbstractAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7642.PartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7642,
        )

        return self.__parent__._cast(_7642.PartCompoundAdvancedSystemDeflection)

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
    def agma_gleason_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7567.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7567,
        )

        return self.__parent__._cast(
            _7567.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_differential_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7574.BevelDifferentialGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7574,
        )

        return self.__parent__._cast(
            _7574.BevelDifferentialGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7579.BevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7579,
        )

        return self.__parent__._cast(_7579.BevelGearSetCompoundAdvancedSystemDeflection)

    @property
    def hypoid_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7625.HypoidGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7625,
        )

        return self.__parent__._cast(
            _7625.HypoidGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7629.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7629,
        )

        return self.__parent__._cast(
            _7629.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7632.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7632,
        )

        return self.__parent__._cast(
            _7632.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7635.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7635,
        )

        return self.__parent__._cast(
            _7635.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7664.SpiralBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7664,
        )

        return self.__parent__._cast(
            _7664.SpiralBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7670.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7670,
        )

        return self.__parent__._cast(
            _7670.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7673.StraightBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7673,
        )

        return self.__parent__._cast(
            _7673.StraightBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def zerol_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7691.ZerolBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7691,
        )

        return self.__parent__._cast(
            _7691.ZerolBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "ConicalGearSetCompoundAdvancedSystemDeflection":
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
class ConicalGearSetCompoundAdvancedSystemDeflection(
    _7621.GearSetCompoundAdvancedSystemDeflection
):
    """ConicalGearSetCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gear_duty_cycle_rating(self: "Self") -> "_554.ConicalGearSetDutyCycleRating":
        """mastapy.gears.rating.conical.ConicalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDutyCycleRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gear_duty_cycle_rating(
        self: "Self",
    ) -> "_554.ConicalGearSetDutyCycleRating":
        """mastapy.gears.rating.conical.ConicalGearSetDutyCycleRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearDutyCycleRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_7460.ConicalGearSetAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection]

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
    ) -> "List[_7460.ConicalGearSetAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetCompoundAdvancedSystemDeflection
        """
        return _Cast_ConicalGearSetCompoundAdvancedSystemDeflection(self)
