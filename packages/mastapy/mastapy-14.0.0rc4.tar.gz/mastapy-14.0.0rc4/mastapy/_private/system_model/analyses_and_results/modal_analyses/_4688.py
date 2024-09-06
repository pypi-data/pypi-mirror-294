"""AGMAGleasonConicalGearMeshModalAnalysis"""

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

_AGMA_GLEASON_CONICAL_GEAR_MESH_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "AGMAGleasonConicalGearMeshModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4695,
        _4700,
        _4719,
        _4747,
        _4751,
        _4754,
        _4797,
        _4803,
        _4806,
        _4827,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2773,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2353

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshModalAnalysis._Cast_AGMAGleasonConicalGearMeshModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshModalAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearMeshModalAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshModalAnalysis"

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
    def bevel_differential_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4695.BevelDifferentialGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4695,
        )

        return self.__parent__._cast(_4695.BevelDifferentialGearMeshModalAnalysis)

    @property
    def bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4700.BevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4700,
        )

        return self.__parent__._cast(_4700.BevelGearMeshModalAnalysis)

    @property
    def hypoid_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4751.HypoidGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4751,
        )

        return self.__parent__._cast(_4751.HypoidGearMeshModalAnalysis)

    @property
    def spiral_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4797.SpiralBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4797,
        )

        return self.__parent__._cast(_4797.SpiralBevelGearMeshModalAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4803.StraightBevelDiffGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4803,
        )

        return self.__parent__._cast(_4803.StraightBevelDiffGearMeshModalAnalysis)

    @property
    def straight_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4806.StraightBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4806,
        )

        return self.__parent__._cast(_4806.StraightBevelGearMeshModalAnalysis)

    @property
    def zerol_bevel_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "_4827.ZerolBevelGearMeshModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4827,
        )

        return self.__parent__._cast(_4827.ZerolBevelGearMeshModalAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshModalAnalysis":
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
class AGMAGleasonConicalGearMeshModalAnalysis(_4716.ConicalGearMeshModalAnalysis):
    """AGMAGleasonConicalGearMeshModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2353.AGMAGleasonConicalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh

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
    ) -> "_2773.AGMAGleasonConicalGearMeshSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.AGMAGleasonConicalGearMeshSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearMeshModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshModalAnalysis
        """
        return _Cast_AGMAGleasonConicalGearMeshModalAnalysis(self)
