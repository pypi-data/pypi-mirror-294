"""CoaxialConnectionParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4521,
)

_COAXIAL_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "CoaxialConnectionParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7707
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4407,
        _4439,
        _4448,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6984
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2798,
    )
    from mastapy._private.system_model.connections_and_sockets import _2323

    Self = TypeVar("Self", bound="CoaxialConnectionParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoaxialConnectionParametricStudyTool._Cast_CoaxialConnectionParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoaxialConnectionParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoaxialConnectionParametricStudyTool:
    """Special nested class for casting CoaxialConnectionParametricStudyTool to subclasses."""

    __parent__: "CoaxialConnectionParametricStudyTool"

    @property
    def shaft_to_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4521.ShaftToMountableComponentConnectionParametricStudyTool":
        return self.__parent__._cast(
            _4521.ShaftToMountableComponentConnectionParametricStudyTool
        )

    @property
    def abstract_shaft_to_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4407.AbstractShaftToMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4407,
        )

        return self.__parent__._cast(
            _4407.AbstractShaftToMountableComponentConnectionParametricStudyTool
        )

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4439.ConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4439,
        )

        return self.__parent__._cast(_4439.ConnectionParametricStudyTool)

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
    def cycloidal_disc_central_bearing_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4448.CycloidalDiscCentralBearingConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4448,
        )

        return self.__parent__._cast(
            _4448.CycloidalDiscCentralBearingConnectionParametricStudyTool
        )

    @property
    def coaxial_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "CoaxialConnectionParametricStudyTool":
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
class CoaxialConnectionParametricStudyTool(
    _4521.ShaftToMountableComponentConnectionParametricStudyTool
):
    """CoaxialConnectionParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COAXIAL_CONNECTION_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2323.CoaxialConnection":
        """mastapy.system_model.connections_and_sockets.CoaxialConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_6984.CoaxialConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_system_deflection_results(
        self: "Self",
    ) -> "List[_2798.CoaxialConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CoaxialConnectionSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionSystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CoaxialConnectionParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_CoaxialConnectionParametricStudyTool
        """
        return _Cast_CoaxialConnectionParametricStudyTool(self)
