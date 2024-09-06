"""CouplingMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5616

_COUPLING_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "CouplingMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5500,
        _5526,
        _5532,
        _5594,
        _5597,
        _5623,
        _5638,
    )
    from mastapy._private.system_model.part_model.couplings import _2642

    Self = TypeVar("Self", bound="CouplingMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingMultibodyDynamicsAnalysis._Cast_CouplingMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingMultibodyDynamicsAnalysis:
    """Special nested class for casting CouplingMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "CouplingMultibodyDynamicsAnalysis"

    @property
    def specialised_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5616.SpecialisedAssemblyMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5616.SpecialisedAssemblyMultibodyDynamicsAnalysis)

    @property
    def abstract_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5500.AbstractAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5500,
        )

        return self.__parent__._cast(_5500.AbstractAssemblyMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5594.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5594,
        )

        return self.__parent__._cast(_5594.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7718.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartTimeSeriesLoadAnalysisCase)

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
    def clutch_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5526.ClutchMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5526,
        )

        return self.__parent__._cast(_5526.ClutchMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5532.ConceptCouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5532,
        )

        return self.__parent__._cast(_5532.ConceptCouplingMultibodyDynamicsAnalysis)

    @property
    def part_to_part_shear_coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5597.PartToPartShearCouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5597,
        )

        return self.__parent__._cast(
            _5597.PartToPartShearCouplingMultibodyDynamicsAnalysis
        )

    @property
    def spring_damper_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5623.SpringDamperMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5623,
        )

        return self.__parent__._cast(_5623.SpringDamperMultibodyDynamicsAnalysis)

    @property
    def torque_converter_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5638.TorqueConverterMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5638,
        )

        return self.__parent__._cast(_5638.TorqueConverterMultibodyDynamicsAnalysis)

    @property
    def coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "CouplingMultibodyDynamicsAnalysis":
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
class CouplingMultibodyDynamicsAnalysis(
    _5616.SpecialisedAssemblyMultibodyDynamicsAnalysis
):
    """CouplingMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2642.Coupling":
        """mastapy.system_model.part_model.couplings.Coupling

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingMultibodyDynamicsAnalysis
        """
        return _Cast_CouplingMultibodyDynamicsAnalysis(self)
