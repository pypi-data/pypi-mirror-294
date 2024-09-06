"""AGMAGleasonConicalGearMeshStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses import _3895

_AGMA_GLEASON_CONICAL_GEAR_MESH_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "AGMAGleasonConicalGearMeshStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3874,
        _3879,
        _3898,
        _3923,
        _3927,
        _3930,
        _3966,
        _3975,
        _3978,
        _3996,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2353

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshStabilityAnalysis._Cast_AGMAGleasonConicalGearMeshStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshStabilityAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearMeshStabilityAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshStabilityAnalysis"

    @property
    def conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3895.ConicalGearMeshStabilityAnalysis":
        return self.__parent__._cast(_3895.ConicalGearMeshStabilityAnalysis)

    @property
    def gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3923.GearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3923,
        )

        return self.__parent__._cast(_3923.GearMeshStabilityAnalysis)

    @property
    def inter_mountable_component_connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3930.InterMountableComponentConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3930,
        )

        return self.__parent__._cast(
            _3930.InterMountableComponentConnectionStabilityAnalysis
        )

    @property
    def connection_stability_analysis(
        self: "CastSelf",
    ) -> "_3898.ConnectionStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3898,
        )

        return self.__parent__._cast(_3898.ConnectionStabilityAnalysis)

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
    def bevel_differential_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3874.BevelDifferentialGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3874,
        )

        return self.__parent__._cast(_3874.BevelDifferentialGearMeshStabilityAnalysis)

    @property
    def bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3879.BevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3879,
        )

        return self.__parent__._cast(_3879.BevelGearMeshStabilityAnalysis)

    @property
    def hypoid_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3927.HypoidGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3927,
        )

        return self.__parent__._cast(_3927.HypoidGearMeshStabilityAnalysis)

    @property
    def spiral_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3966.SpiralBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3966,
        )

        return self.__parent__._cast(_3966.SpiralBevelGearMeshStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3975.StraightBevelDiffGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3975,
        )

        return self.__parent__._cast(_3975.StraightBevelDiffGearMeshStabilityAnalysis)

    @property
    def straight_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3978.StraightBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3978,
        )

        return self.__parent__._cast(_3978.StraightBevelGearMeshStabilityAnalysis)

    @property
    def zerol_bevel_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "_3996.ZerolBevelGearMeshStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3996,
        )

        return self.__parent__._cast(_3996.ZerolBevelGearMeshStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_stability_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshStabilityAnalysis":
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
class AGMAGleasonConicalGearMeshStabilityAnalysis(
    _3895.ConicalGearMeshStabilityAnalysis
):
    """AGMAGleasonConicalGearMeshStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_STABILITY_ANALYSIS

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
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearMeshStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshStabilityAnalysis
        """
        return _Cast_AGMAGleasonConicalGearMeshStabilityAnalysis(self)
