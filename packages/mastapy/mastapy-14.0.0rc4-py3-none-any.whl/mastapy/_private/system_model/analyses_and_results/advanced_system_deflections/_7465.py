"""CouplingConnectionAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7493,
)

_COUPLING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "CouplingConnectionAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2733, _2735, _2737
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7448,
        _7453,
        _7461,
        _7512,
        _7534,
        _7549,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7710,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2400

    Self = TypeVar("Self", bound="CouplingConnectionAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionAdvancedSystemDeflection._Cast_CouplingConnectionAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionAdvancedSystemDeflection:
    """Special nested class for casting CouplingConnectionAdvancedSystemDeflection to subclasses."""

    __parent__: "CouplingConnectionAdvancedSystemDeflection"

    @property
    def inter_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7493.InterMountableComponentConnectionAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7493.InterMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7461.ConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7461,
        )

        return self.__parent__._cast(_7461.ConnectionAdvancedSystemDeflection)

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
    def clutch_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7448.ClutchConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7448,
        )

        return self.__parent__._cast(_7448.ClutchConnectionAdvancedSystemDeflection)

    @property
    def concept_coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7453.ConceptCouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7453,
        )

        return self.__parent__._cast(
            _7453.ConceptCouplingConnectionAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7512.PartToPartShearCouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7512,
        )

        return self.__parent__._cast(
            _7512.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        )

    @property
    def spring_damper_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7534.SpringDamperConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7534,
        )

        return self.__parent__._cast(
            _7534.SpringDamperConnectionAdvancedSystemDeflection
        )

    @property
    def torque_converter_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7549.TorqueConverterConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7549,
        )

        return self.__parent__._cast(
            _7549.TorqueConverterConnectionAdvancedSystemDeflection
        )

    @property
    def coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "CouplingConnectionAdvancedSystemDeflection":
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
class CouplingConnectionAdvancedSystemDeflection(
    _7493.InterMountableComponentConnectionAdvancedSystemDeflection
):
    """CouplingConnectionAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2400.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionAdvancedSystemDeflection
        """
        return _Cast_CouplingConnectionAdvancedSystemDeflection(self)
