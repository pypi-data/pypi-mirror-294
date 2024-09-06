"""BevelGearMeshAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7164,
)

_BEVEL_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "BevelGearMeshAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7172,
        _7193,
        _7195,
        _7219,
        _7226,
        _7263,
        _7269,
        _7272,
        _7290,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2790,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2357

    Self = TypeVar(
        "Self", bound="BevelGearMeshAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearMeshAdvancedTimeSteppingAnalysisForModulation._Cast_BevelGearMeshAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearMeshAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearMeshAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting BevelGearMeshAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "BevelGearMeshAdvancedTimeSteppingAnalysisForModulation"

    @property
    def agma_gleason_conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7164.AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7164.AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7193.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7193,
        )

        return self.__parent__._cast(
            _7193.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7219.GearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7219,
        )

        return self.__parent__._cast(
            _7219.GearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def inter_mountable_component_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7226.InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7226,
        )

        return self.__parent__._cast(
            _7226.InterMountableComponentConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7195.ConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7195,
        )

        return self.__parent__._cast(
            _7195.ConnectionAdvancedTimeSteppingAnalysisForModulation
        )

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
    def bevel_differential_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7172.BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7172,
        )

        return self.__parent__._cast(
            _7172.BevelDifferentialGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7263.SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7263,
        )

        return self.__parent__._cast(
            _7263.SpiralBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7269.StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7269,
        )

        return self.__parent__._cast(
            _7269.StraightBevelDiffGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7272.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7272,
        )

        return self.__parent__._cast(
            _7272.StraightBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7290.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7290,
        )

        return self.__parent__._cast(
            _7290.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_mesh_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "BevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
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
class BevelGearMeshAdvancedTimeSteppingAnalysisForModulation(
    _7164.AGMAGleasonConicalGearMeshAdvancedTimeSteppingAnalysisForModulation
):
    """BevelGearMeshAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _BEVEL_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2357.BevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.BevelGearMesh

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
    ) -> "_2790.BevelGearMeshSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.BevelGearMeshSystemDeflection

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
    ) -> "_Cast_BevelGearMeshAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_BevelGearMeshAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_BevelGearMeshAdvancedTimeSteppingAnalysisForModulation(self)
