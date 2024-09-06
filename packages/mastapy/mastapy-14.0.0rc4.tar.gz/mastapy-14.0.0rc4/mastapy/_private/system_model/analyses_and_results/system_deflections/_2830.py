"""CylindricalGearSystemDeflectionTimestep"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.system_deflections import _2829

_CYLINDRICAL_GEAR_SYSTEM_DEFLECTION_TIMESTEP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CylindricalGearSystemDeflectionTimestep",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7716,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2799,
        _2845,
        _2868,
        _2871,
    )

    Self = TypeVar("Self", bound="CylindricalGearSystemDeflectionTimestep")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSystemDeflectionTimestep._Cast_CylindricalGearSystemDeflectionTimestep",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSystemDeflectionTimestep",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSystemDeflectionTimestep:
    """Special nested class for casting CylindricalGearSystemDeflectionTimestep to subclasses."""

    __parent__: "CylindricalGearSystemDeflectionTimestep"

    @property
    def cylindrical_gear_system_deflection(
        self: "CastSelf",
    ) -> "_2829.CylindricalGearSystemDeflection":
        return self.__parent__._cast(_2829.CylindricalGearSystemDeflection)

    @property
    def gear_system_deflection(self: "CastSelf") -> "_2845.GearSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2845,
        )

        return self.__parent__._cast(_2845.GearSystemDeflection)

    @property
    def mountable_component_system_deflection(
        self: "CastSelf",
    ) -> "_2868.MountableComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2868,
        )

        return self.__parent__._cast(_2868.MountableComponentSystemDeflection)

    @property
    def component_system_deflection(
        self: "CastSelf",
    ) -> "_2799.ComponentSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2799,
        )

        return self.__parent__._cast(_2799.ComponentSystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2871.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2871,
        )

        return self.__parent__._cast(_2871.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7716.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7716,
        )

        return self.__parent__._cast(_7716.PartFEAnalysis)

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
    def cylindrical_gear_system_deflection_timestep(
        self: "CastSelf",
    ) -> "CylindricalGearSystemDeflectionTimestep":
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
class CylindricalGearSystemDeflectionTimestep(_2829.CylindricalGearSystemDeflection):
    """CylindricalGearSystemDeflectionTimestep

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SYSTEM_DEFLECTION_TIMESTEP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSystemDeflectionTimestep":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSystemDeflectionTimestep
        """
        return _Cast_CylindricalGearSystemDeflectionTimestep(self)
