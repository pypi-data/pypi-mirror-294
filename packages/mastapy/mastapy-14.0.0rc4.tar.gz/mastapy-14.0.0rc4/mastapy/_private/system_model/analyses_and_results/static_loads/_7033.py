"""FaceGearMeshLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7040

_FACE_GEAR_MESH_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "FaceGearMeshLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6997,
        _7059,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2365

    Self = TypeVar("Self", bound="FaceGearMeshLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="FaceGearMeshLoadCase._Cast_FaceGearMeshLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearMeshLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearMeshLoadCase:
    """Special nested class for casting FaceGearMeshLoadCase to subclasses."""

    __parent__: "FaceGearMeshLoadCase"

    @property
    def gear_mesh_load_case(self: "CastSelf") -> "_7040.GearMeshLoadCase":
        return self.__parent__._cast(_7040.GearMeshLoadCase)

    @property
    def inter_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7059.InterMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7059,
        )

        return self.__parent__._cast(_7059.InterMountableComponentConnectionLoadCase)

    @property
    def connection_load_case(self: "CastSelf") -> "_6997.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6997,
        )

        return self.__parent__._cast(_6997.ConnectionLoadCase)

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
    def face_gear_mesh_load_case(self: "CastSelf") -> "FaceGearMeshLoadCase":
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
class FaceGearMeshLoadCase(_7040.GearMeshLoadCase):
    """FaceGearMeshLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_MESH_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2365.FaceGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.FaceGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearMeshLoadCase":
        """Cast to another type.

        Returns:
            _Cast_FaceGearMeshLoadCase
        """
        return _Cast_FaceGearMeshLoadCase(self)
