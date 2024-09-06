"""AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5693,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5503
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5682,
        _5702,
        _5704,
        _5743,
        _5757,
    )

    Self = TypeVar(
        "Self",
        bound="AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis._Cast_AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: (
        "AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis"
    )

    @property
    def connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5693.ConnectionCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5693.ConnectionCompoundMultibodyDynamicsAnalysis)

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
    def coaxial_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5682.CoaxialConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5682,
        )

        return self.__parent__._cast(
            _5682.CoaxialConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def cycloidal_disc_central_bearing_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5702.CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5702,
        )

        return self.__parent__._cast(
            _5702.CycloidalDiscCentralBearingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> (
        "_5704.CycloidalDiscPlanetaryBearingConnectionCompoundMultibodyDynamicsAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5704,
        )

        return self.__parent__._cast(
            _5704.CycloidalDiscPlanetaryBearingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def planetary_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5743.PlanetaryConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5743,
        )

        return self.__parent__._cast(
            _5743.PlanetaryConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def shaft_to_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5757.ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5757,
        )

        return self.__parent__._cast(
            _5757.ShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
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
class AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis(
    _5693.ConnectionCompoundMultibodyDynamicsAnalysis
):
    """AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5503.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis]

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
    ) -> "List[_5503.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.AbstractShaftToMountableComponentConnectionMultibodyDynamicsAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_AbstractShaftToMountableComponentConnectionCompoundMultibodyDynamicsAnalysis(
            self
        )
