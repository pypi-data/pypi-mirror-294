"""KlingelnbergCycloPalloidConicalGearMeshModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4716

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "KlingelnbergCycloPalloidConicalGearMeshModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4719,
        _4747,
        _4754,
        _4758,
        _4761,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2852,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2372

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearMeshModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMeshModalAnalysis._Cast_KlingelnbergCycloPalloidConicalGearMeshModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMeshModalAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshModalAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMeshModalAnalysis"

    @property
    def conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4716.ConicalGearMeshModalAnalysis":
        return self.__parent__._cast(_4716.ConicalGearMeshModalAnalysis)

    @property
    def gear_mesh_modal_analysis(self: "CastSelf") -> "_4747.GearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4747,
        )

        return self.__parent__._cast(_4747.GearMeshModalAnalysis)

    @property
    def inter_mountable_component_connection_modal_analysis(
        self: "CastSelf",
    ) -> "_4754.InterMountableComponentConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4754,
        )

        return self.__parent__._cast(
            _4754.InterMountableComponentConnectionModalAnalysis
        )

    @property
    def connection_modal_analysis(self: "CastSelf") -> "_4719.ConnectionModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4719,
        )

        return self.__parent__._cast(_4719.ConnectionModalAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7710.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7707.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7707,
        )

        return self.__parent__._cast(_7707.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2733.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2733

        return self.__parent__._cast(_2733.ConnectionAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4758.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4758,
        )

        return self.__parent__._cast(
            _4758.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4761.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4761,
        )

        return self.__parent__._cast(
            _4761.KlingelnbergCycloPalloidSpiralBevelGearMeshModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMeshModalAnalysis":
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
class KlingelnbergCycloPalloidConicalGearMeshModalAnalysis(
    _4716.ConicalGearMeshModalAnalysis
):
    """KlingelnbergCycloPalloidConicalGearMeshModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_MODAL_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(
        self: "Self",
    ) -> "_2372.KlingelnbergCycloPalloidConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2852.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearMeshModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMeshModalAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMeshModalAnalysis(self)
