"""KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4066,
)

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
        "KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3934,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4032,
        _4034,
        _4058,
        _4064,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2373

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis._Cast_KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4066.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis":
        return self.__parent__._cast(
            _4066.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis
        )

    @property
    def conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4032.ConicalGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4032,
        )

        return self.__parent__._cast(_4032.ConicalGearMeshCompoundStabilityAnalysis)

    @property
    def gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4058.GearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4058,
        )

        return self.__parent__._cast(_4058.GearMeshCompoundStabilityAnalysis)

    @property
    def inter_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4064.InterMountableComponentConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4064,
        )

        return self.__parent__._cast(
            _4064.InterMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4034.ConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4034,
        )

        return self.__parent__._cast(_4034.ConnectionCompoundStabilityAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis":
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
class KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis(
    _4066.KlingelnbergCycloPalloidConicalGearMeshCompoundStabilityAnalysis
):
    """KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(
        self: "Self",
    ) -> "_2373.KlingelnbergCycloPalloidHypoidGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(
        self: "Self",
    ) -> "_2373.KlingelnbergCycloPalloidHypoidGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3934.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]

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
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3934.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.KlingelnbergCycloPalloidHypoidGearMeshStabilityAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearMeshCompoundStabilityAnalysis(
            self
        )
