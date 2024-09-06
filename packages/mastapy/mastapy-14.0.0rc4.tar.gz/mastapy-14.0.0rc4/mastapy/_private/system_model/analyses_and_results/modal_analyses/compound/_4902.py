"""GearSetCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4942,
)

_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "GearSetCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7712,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4749
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4842,
        _4848,
        _4855,
        _4860,
        _4873,
        _4876,
        _4891,
        _4897,
        _4906,
        _4910,
        _4913,
        _4916,
        _4923,
        _4928,
        _4945,
        _4951,
        _4954,
        _4969,
        _4972,
    )

    Self = TypeVar("Self", bound="GearSetCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearSetCompoundModalAnalysis._Cast_GearSetCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetCompoundModalAnalysis:
    """Special nested class for casting GearSetCompoundModalAnalysis to subclasses."""

    __parent__: "GearSetCompoundModalAnalysis"

    @property
    def specialised_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4942.SpecialisedAssemblyCompoundModalAnalysis":
        return self.__parent__._cast(_4942.SpecialisedAssemblyCompoundModalAnalysis)

    @property
    def abstract_assembly_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4842.AbstractAssemblyCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4842,
        )

        return self.__parent__._cast(_4842.AbstractAssemblyCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4923.PartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4923,
        )

        return self.__parent__._cast(_4923.PartCompoundModalAnalysis)

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
    def agma_gleason_conical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4848.AGMAGleasonConicalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4848,
        )

        return self.__parent__._cast(
            _4848.AGMAGleasonConicalGearSetCompoundModalAnalysis
        )

    @property
    def bevel_differential_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4855.BevelDifferentialGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4855,
        )

        return self.__parent__._cast(
            _4855.BevelDifferentialGearSetCompoundModalAnalysis
        )

    @property
    def bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4860.BevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4860,
        )

        return self.__parent__._cast(_4860.BevelGearSetCompoundModalAnalysis)

    @property
    def concept_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4873.ConceptGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4873,
        )

        return self.__parent__._cast(_4873.ConceptGearSetCompoundModalAnalysis)

    @property
    def conical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4876.ConicalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4876,
        )

        return self.__parent__._cast(_4876.ConicalGearSetCompoundModalAnalysis)

    @property
    def cylindrical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4891.CylindricalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4891,
        )

        return self.__parent__._cast(_4891.CylindricalGearSetCompoundModalAnalysis)

    @property
    def face_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4897.FaceGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4897,
        )

        return self.__parent__._cast(_4897.FaceGearSetCompoundModalAnalysis)

    @property
    def hypoid_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4906.HypoidGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4906,
        )

        return self.__parent__._cast(_4906.HypoidGearSetCompoundModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4910.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4910,
        )

        return self.__parent__._cast(
            _4910.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4913.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4913,
        )

        return self.__parent__._cast(
            _4913.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4916.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4916,
        )

        return self.__parent__._cast(
            _4916.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysis
        )

    @property
    def planetary_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4928.PlanetaryGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4928,
        )

        return self.__parent__._cast(_4928.PlanetaryGearSetCompoundModalAnalysis)

    @property
    def spiral_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4945.SpiralBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4945,
        )

        return self.__parent__._cast(_4945.SpiralBevelGearSetCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4951.StraightBevelDiffGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4951,
        )

        return self.__parent__._cast(
            _4951.StraightBevelDiffGearSetCompoundModalAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4954.StraightBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4954,
        )

        return self.__parent__._cast(_4954.StraightBevelGearSetCompoundModalAnalysis)

    @property
    def worm_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4969.WormGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4969,
        )

        return self.__parent__._cast(_4969.WormGearSetCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4972.ZerolBevelGearSetCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4972,
        )

        return self.__parent__._cast(_4972.ZerolBevelGearSetCompoundModalAnalysis)

    @property
    def gear_set_compound_modal_analysis(
        self: "CastSelf",
    ) -> "GearSetCompoundModalAnalysis":
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
class GearSetCompoundModalAnalysis(_4942.SpecialisedAssemblyCompoundModalAnalysis):
    """GearSetCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_4749.GearSetModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.GearSetModalAnalysis]

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
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4749.GearSetModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.GearSetModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_GearSetCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearSetCompoundModalAnalysis
        """
        return _Cast_GearSetCompoundModalAnalysis(self)
