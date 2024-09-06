"""ConicalGearMeshCompoundSystemDeflection"""

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
    _2997,
)

_CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "ConicalGearMeshCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2808,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2942,
        _2949,
        _2954,
        _2972,
        _3001,
        _3003,
        _3005,
        _3008,
        _3011,
        _3041,
        _3047,
        _3050,
        _3068,
    )

    Self = TypeVar("Self", bound="ConicalGearMeshCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshCompoundSystemDeflection._Cast_ConicalGearMeshCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshCompoundSystemDeflection:
    """Special nested class for casting ConicalGearMeshCompoundSystemDeflection to subclasses."""

    __parent__: "ConicalGearMeshCompoundSystemDeflection"

    @property
    def gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2997.GearMeshCompoundSystemDeflection":
        return self.__parent__._cast(_2997.GearMeshCompoundSystemDeflection)

    @property
    def inter_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3003.InterMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3003,
        )

        return self.__parent__._cast(
            _3003.InterMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2972.ConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2972,
        )

        return self.__parent__._cast(_2972.ConnectionCompoundSystemDeflection)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7708.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7708,
        )

        return self.__parent__._cast(_7708.ConnectionCompoundAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2942.AGMAGleasonConicalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2942,
        )

        return self.__parent__._cast(
            _2942.AGMAGleasonConicalGearMeshCompoundSystemDeflection
        )

    @property
    def bevel_differential_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2949.BevelDifferentialGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2949,
        )

        return self.__parent__._cast(
            _2949.BevelDifferentialGearMeshCompoundSystemDeflection
        )

    @property
    def bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2954.BevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2954,
        )

        return self.__parent__._cast(_2954.BevelGearMeshCompoundSystemDeflection)

    @property
    def hypoid_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3001.HypoidGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3001,
        )

        return self.__parent__._cast(_3001.HypoidGearMeshCompoundSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3005.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3005,
        )

        return self.__parent__._cast(
            _3005.KlingelnbergCycloPalloidConicalGearMeshCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3008.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3008,
        )

        return self.__parent__._cast(
            _3008.KlingelnbergCycloPalloidHypoidGearMeshCompoundSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3011.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3011,
        )

        return self.__parent__._cast(
            _3011.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3041.SpiralBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3041,
        )

        return self.__parent__._cast(_3041.SpiralBevelGearMeshCompoundSystemDeflection)

    @property
    def straight_bevel_diff_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3047.StraightBevelDiffGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3047,
        )

        return self.__parent__._cast(
            _3047.StraightBevelDiffGearMeshCompoundSystemDeflection
        )

    @property
    def straight_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3050.StraightBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3050,
        )

        return self.__parent__._cast(
            _3050.StraightBevelGearMeshCompoundSystemDeflection
        )

    @property
    def zerol_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3068.ZerolBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3068,
        )

        return self.__parent__._cast(_3068.ZerolBevelGearMeshCompoundSystemDeflection)

    @property
    def conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "ConicalGearMeshCompoundSystemDeflection":
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
class ConicalGearMeshCompoundSystemDeflection(_2997.GearMeshCompoundSystemDeflection):
    """ConicalGearMeshCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def planetaries(self: "Self") -> "List[ConicalGearMeshCompoundSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.compound.ConicalGearMeshCompoundSystemDeflection]

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
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_2808.ConicalGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConicalGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2808.ConicalGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConicalGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshCompoundSystemDeflection
        """
        return _Cast_ConicalGearMeshCompoundSystemDeflection(self)
