"""ConnectorAdvancedSystemDeflection"""

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
    _7508,
)

_CONNECTOR_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "ConnectorAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7434,
        _7451,
        _7509,
        _7510,
        _7527,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.part_model import _2502

    Self = TypeVar("Self", bound="ConnectorAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectorAdvancedSystemDeflection._Cast_ConnectorAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectorAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectorAdvancedSystemDeflection:
    """Special nested class for casting ConnectorAdvancedSystemDeflection to subclasses."""

    __parent__: "ConnectorAdvancedSystemDeflection"

    @property
    def mountable_component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7508.MountableComponentAdvancedSystemDeflection":
        return self.__parent__._cast(_7508.MountableComponentAdvancedSystemDeflection)

    @property
    def component_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7451.ComponentAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7451,
        )

        return self.__parent__._cast(_7451.ComponentAdvancedSystemDeflection)

    @property
    def part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7510.PartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7510,
        )

        return self.__parent__._cast(_7510.PartAdvancedSystemDeflection)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7717.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7714.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7714,
        )

        return self.__parent__._cast(_7714.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2741.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2741

        return self.__parent__._cast(_2741.PartAnalysis)

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
    def bearing_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7434.BearingAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7434,
        )

        return self.__parent__._cast(_7434.BearingAdvancedSystemDeflection)

    @property
    def oil_seal_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7509.OilSealAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7509,
        )

        return self.__parent__._cast(_7509.OilSealAdvancedSystemDeflection)

    @property
    def shaft_hub_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7527.ShaftHubConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7527,
        )

        return self.__parent__._cast(_7527.ShaftHubConnectionAdvancedSystemDeflection)

    @property
    def connector_advanced_system_deflection(
        self: "CastSelf",
    ) -> "ConnectorAdvancedSystemDeflection":
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
class ConnectorAdvancedSystemDeflection(
    _7508.MountableComponentAdvancedSystemDeflection
):
    """ConnectorAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTOR_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2502.Connector":
        """mastapy.system_model.part_model.Connector

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConnectorAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_ConnectorAdvancedSystemDeflection
        """
        return _Cast_ConnectorAdvancedSystemDeflection(self)
