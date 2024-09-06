"""ConnectionCompoundSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7708

_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "ConnectionCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7712
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2811,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2940,
        _2942,
        _2946,
        _2949,
        _2954,
        _2959,
        _2961,
        _2964,
        _2967,
        _2970,
        _2975,
        _2977,
        _2981,
        _2983,
        _2985,
        _2992,
        _2997,
        _3001,
        _3003,
        _3005,
        _3008,
        _3011,
        _3021,
        _3023,
        _3030,
        _3033,
        _3038,
        _3041,
        _3044,
        _3047,
        _3050,
        _3059,
        _3065,
        _3068,
    )

    Self = TypeVar("Self", bound="ConnectionCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundSystemDeflection._Cast_ConnectionCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundSystemDeflection:
    """Special nested class for casting ConnectionCompoundSystemDeflection to subclasses."""

    __parent__: "ConnectionCompoundSystemDeflection"

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7708.ConnectionCompoundAnalysis":
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
    def abstract_shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2940.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2940,
        )

        return self.__parent__._cast(
            _2940.AbstractShaftToMountableComponentConnectionCompoundSystemDeflection
        )

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
    def belt_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2946.BeltConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2946,
        )

        return self.__parent__._cast(_2946.BeltConnectionCompoundSystemDeflection)

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
    def clutch_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2959.ClutchConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2959,
        )

        return self.__parent__._cast(_2959.ClutchConnectionCompoundSystemDeflection)

    @property
    def coaxial_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2961.CoaxialConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2961,
        )

        return self.__parent__._cast(_2961.CoaxialConnectionCompoundSystemDeflection)

    @property
    def concept_coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2964.ConceptCouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2964,
        )

        return self.__parent__._cast(
            _2964.ConceptCouplingConnectionCompoundSystemDeflection
        )

    @property
    def concept_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2967.ConceptGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2967,
        )

        return self.__parent__._cast(_2967.ConceptGearMeshCompoundSystemDeflection)

    @property
    def conical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2970.ConicalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2970,
        )

        return self.__parent__._cast(_2970.ConicalGearMeshCompoundSystemDeflection)

    @property
    def coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2975.CouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2975,
        )

        return self.__parent__._cast(_2975.CouplingConnectionCompoundSystemDeflection)

    @property
    def cvt_belt_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2977.CVTBeltConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2977,
        )

        return self.__parent__._cast(_2977.CVTBeltConnectionCompoundSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2981.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2981,
        )

        return self.__parent__._cast(
            _2981.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2983.CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2983,
        )

        return self.__parent__._cast(
            _2983.CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection
        )

    @property
    def cylindrical_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2985.CylindricalGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2985,
        )

        return self.__parent__._cast(_2985.CylindricalGearMeshCompoundSystemDeflection)

    @property
    def face_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2992.FaceGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2992,
        )

        return self.__parent__._cast(_2992.FaceGearMeshCompoundSystemDeflection)

    @property
    def gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2997.GearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2997,
        )

        return self.__parent__._cast(_2997.GearMeshCompoundSystemDeflection)

    @property
    def hypoid_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3001.HypoidGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3001,
        )

        return self.__parent__._cast(_3001.HypoidGearMeshCompoundSystemDeflection)

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
    def part_to_part_shear_coupling_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3021.PartToPartShearCouplingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3021,
        )

        return self.__parent__._cast(
            _3021.PartToPartShearCouplingConnectionCompoundSystemDeflection
        )

    @property
    def planetary_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3023.PlanetaryConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3023,
        )

        return self.__parent__._cast(_3023.PlanetaryConnectionCompoundSystemDeflection)

    @property
    def ring_pins_to_disc_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3030.RingPinsToDiscConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3030,
        )

        return self.__parent__._cast(
            _3030.RingPinsToDiscConnectionCompoundSystemDeflection
        )

    @property
    def rolling_ring_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3033.RollingRingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3033,
        )

        return self.__parent__._cast(
            _3033.RollingRingConnectionCompoundSystemDeflection
        )

    @property
    def shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3038.ShaftToMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3038,
        )

        return self.__parent__._cast(
            _3038.ShaftToMountableComponentConnectionCompoundSystemDeflection
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
    def spring_damper_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3044.SpringDamperConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3044,
        )

        return self.__parent__._cast(
            _3044.SpringDamperConnectionCompoundSystemDeflection
        )

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
    def torque_converter_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3059.TorqueConverterConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3059,
        )

        return self.__parent__._cast(
            _3059.TorqueConverterConnectionCompoundSystemDeflection
        )

    @property
    def worm_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3065.WormGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3065,
        )

        return self.__parent__._cast(_3065.WormGearMeshCompoundSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3068.ZerolBevelGearMeshCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3068,
        )

        return self.__parent__._cast(_3068.ZerolBevelGearMeshCompoundSystemDeflection)

    @property
    def connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "ConnectionCompoundSystemDeflection":
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
class ConnectionCompoundSystemDeflection(_7708.ConnectionCompoundAnalysis):
    """ConnectionCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_2811.ConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection]

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
    ) -> "List[_2811.ConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ConnectionSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_ConnectionCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundSystemDeflection
        """
        return _Cast_ConnectionCompoundSystemDeflection(self)
