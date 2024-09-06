"""AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5536

_AGMA_GLEASON_CONICAL_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7711,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5514,
        _5519,
        _5539,
        _5562,
        _5567,
        _5574,
        _5617,
        _5624,
        _5627,
        _5648,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2353

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis._Cast_AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis"

    @property
    def conical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5536.ConicalGearMeshMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5536.ConicalGearMeshMultibodyDynamicsAnalysis)

    @property
    def gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5562.GearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5562,
        )

        return self.__parent__._cast(_5562.GearMeshMultibodyDynamicsAnalysis)

    @property
    def inter_mountable_component_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5574.InterMountableComponentConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5574,
        )

        return self.__parent__._cast(
            _5574.InterMountableComponentConnectionMultibodyDynamicsAnalysis
        )

    @property
    def connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5539.ConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5539,
        )

        return self.__parent__._cast(_5539.ConnectionMultibodyDynamicsAnalysis)

    @property
    def connection_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7711.ConnectionTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConnectionTimeSeriesLoadAnalysisCase)

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
    def bevel_differential_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5514.BevelDifferentialGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5514,
        )

        return self.__parent__._cast(
            _5514.BevelDifferentialGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5519.BevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5519,
        )

        return self.__parent__._cast(_5519.BevelGearMeshMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5567.HypoidGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5567,
        )

        return self.__parent__._cast(_5567.HypoidGearMeshMultibodyDynamicsAnalysis)

    @property
    def spiral_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5617.SpiralBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5617,
        )

        return self.__parent__._cast(_5617.SpiralBevelGearMeshMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5624.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5624,
        )

        return self.__parent__._cast(
            _5624.StraightBevelDiffGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5627.StraightBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5627,
        )

        return self.__parent__._cast(
            _5627.StraightBevelGearMeshMultibodyDynamicsAnalysis
        )

    @property
    def zerol_bevel_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5648.ZerolBevelGearMeshMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5648,
        )

        return self.__parent__._cast(_5648.ZerolBevelGearMeshMultibodyDynamicsAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis":
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
class AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis(
    _5536.ConicalGearMeshMultibodyDynamicsAnalysis
):
    """AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_MULTIBODY_DYNAMICS_ANALYSIS

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis
        """
        return _Cast_AGMAGleasonConicalGearMeshMultibodyDynamicsAnalysis(self)
