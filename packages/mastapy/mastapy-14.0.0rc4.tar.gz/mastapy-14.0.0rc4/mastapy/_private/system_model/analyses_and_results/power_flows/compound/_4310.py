"""CouplingCompoundPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
    _4373,
)

_COUPLING_COMPOUND_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound",
    "CouplingCompoundPowerFlow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4175
    from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
        _4273,
        _4294,
        _4299,
        _4354,
        _4355,
        _4377,
        _4392,
    )

    Self = TypeVar("Self", bound="CouplingCompoundPowerFlow")
    CastSelf = TypeVar(
        "CastSelf", bound="CouplingCompoundPowerFlow._Cast_CouplingCompoundPowerFlow"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingCompoundPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingCompoundPowerFlow:
    """Special nested class for casting CouplingCompoundPowerFlow to subclasses."""

    __parent__: "CouplingCompoundPowerFlow"

    @property
    def specialised_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4373.SpecialisedAssemblyCompoundPowerFlow":
        return self.__parent__._cast(_4373.SpecialisedAssemblyCompoundPowerFlow)

    @property
    def abstract_assembly_compound_power_flow(
        self: "CastSelf",
    ) -> "_4273.AbstractAssemblyCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4273,
        )

        return self.__parent__._cast(_4273.AbstractAssemblyCompoundPowerFlow)

    @property
    def part_compound_power_flow(self: "CastSelf") -> "_4354.PartCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4354,
        )

        return self.__parent__._cast(_4354.PartCompoundPowerFlow)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7715.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.PartCompoundAnalysis)

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
    def clutch_compound_power_flow(self: "CastSelf") -> "_4294.ClutchCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4294,
        )

        return self.__parent__._cast(_4294.ClutchCompoundPowerFlow)

    @property
    def concept_coupling_compound_power_flow(
        self: "CastSelf",
    ) -> "_4299.ConceptCouplingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4299,
        )

        return self.__parent__._cast(_4299.ConceptCouplingCompoundPowerFlow)

    @property
    def part_to_part_shear_coupling_compound_power_flow(
        self: "CastSelf",
    ) -> "_4355.PartToPartShearCouplingCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4355,
        )

        return self.__parent__._cast(_4355.PartToPartShearCouplingCompoundPowerFlow)

    @property
    def spring_damper_compound_power_flow(
        self: "CastSelf",
    ) -> "_4377.SpringDamperCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4377,
        )

        return self.__parent__._cast(_4377.SpringDamperCompoundPowerFlow)

    @property
    def torque_converter_compound_power_flow(
        self: "CastSelf",
    ) -> "_4392.TorqueConverterCompoundPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows.compound import (
            _4392,
        )

        return self.__parent__._cast(_4392.TorqueConverterCompoundPowerFlow)

    @property
    def coupling_compound_power_flow(self: "CastSelf") -> "CouplingCompoundPowerFlow":
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
class CouplingCompoundPowerFlow(_4373.SpecialisedAssemblyCompoundPowerFlow):
    """CouplingCompoundPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_COMPOUND_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_4175.CouplingPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(self: "Self") -> "List[_4175.CouplingPowerFlow]":
        """List[mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingCompoundPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_CouplingCompoundPowerFlow
        """
        return _Cast_CouplingCompoundPowerFlow(self)
