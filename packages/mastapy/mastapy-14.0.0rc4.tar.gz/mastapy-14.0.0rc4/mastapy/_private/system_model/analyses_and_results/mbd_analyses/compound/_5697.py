"""CouplingHalfCompoundMultibodyDynamicsAnalysis"""

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
    _5737,
)

_COUPLING_HALF_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "CouplingHalfCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5542
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5681,
        _5683,
        _5686,
        _5700,
        _5739,
        _5742,
        _5748,
        _5752,
        _5764,
        _5774,
        _5775,
        _5776,
        _5779,
        _5780,
    )

    Self = TypeVar("Self", bound="CouplingHalfCompoundMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfCompoundMultibodyDynamicsAnalysis._Cast_CouplingHalfCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting CouplingHalfCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "CouplingHalfCompoundMultibodyDynamicsAnalysis"

    @property
    def mountable_component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5737.MountableComponentCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5737.MountableComponentCompoundMultibodyDynamicsAnalysis
        )

    @property
    def component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5683.ComponentCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5683,
        )

        return self.__parent__._cast(_5683.ComponentCompoundMultibodyDynamicsAnalysis)

    @property
    def part_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5739.PartCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5739,
        )

        return self.__parent__._cast(_5739.PartCompoundMultibodyDynamicsAnalysis)

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
    def clutch_half_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5681.ClutchHalfCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5681,
        )

        return self.__parent__._cast(_5681.ClutchHalfCompoundMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_half_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5686.ConceptCouplingHalfCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5686,
        )

        return self.__parent__._cast(
            _5686.ConceptCouplingHalfCompoundMultibodyDynamicsAnalysis
        )

    @property
    def cvt_pulley_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5700.CVTPulleyCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5700,
        )

        return self.__parent__._cast(_5700.CVTPulleyCompoundMultibodyDynamicsAnalysis)

    @property
    def part_to_part_shear_coupling_half_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5742.PartToPartShearCouplingHalfCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5742,
        )

        return self.__parent__._cast(
            _5742.PartToPartShearCouplingHalfCompoundMultibodyDynamicsAnalysis
        )

    @property
    def pulley_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5748.PulleyCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5748,
        )

        return self.__parent__._cast(_5748.PulleyCompoundMultibodyDynamicsAnalysis)

    @property
    def rolling_ring_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5752.RollingRingCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5752,
        )

        return self.__parent__._cast(_5752.RollingRingCompoundMultibodyDynamicsAnalysis)

    @property
    def spring_damper_half_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5764.SpringDamperHalfCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5764,
        )

        return self.__parent__._cast(
            _5764.SpringDamperHalfCompoundMultibodyDynamicsAnalysis
        )

    @property
    def synchroniser_half_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5774.SynchroniserHalfCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5774,
        )

        return self.__parent__._cast(
            _5774.SynchroniserHalfCompoundMultibodyDynamicsAnalysis
        )

    @property
    def synchroniser_part_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5775.SynchroniserPartCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5775,
        )

        return self.__parent__._cast(
            _5775.SynchroniserPartCompoundMultibodyDynamicsAnalysis
        )

    @property
    def synchroniser_sleeve_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5776.SynchroniserSleeveCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5776,
        )

        return self.__parent__._cast(
            _5776.SynchroniserSleeveCompoundMultibodyDynamicsAnalysis
        )

    @property
    def torque_converter_pump_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5779.TorqueConverterPumpCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5779,
        )

        return self.__parent__._cast(
            _5779.TorqueConverterPumpCompoundMultibodyDynamicsAnalysis
        )

    @property
    def torque_converter_turbine_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5780.TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5780,
        )

        return self.__parent__._cast(
            _5780.TorqueConverterTurbineCompoundMultibodyDynamicsAnalysis
        )

    @property
    def coupling_half_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "CouplingHalfCompoundMultibodyDynamicsAnalysis":
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
class CouplingHalfCompoundMultibodyDynamicsAnalysis(
    _5737.MountableComponentCompoundMultibodyDynamicsAnalysis
):
    """CouplingHalfCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5542.CouplingHalfMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CouplingHalfMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5542.CouplingHalfMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CouplingHalfMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalfCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_CouplingHalfCompoundMultibodyDynamicsAnalysis(self)
