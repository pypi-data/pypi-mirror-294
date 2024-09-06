"""TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
    _6314,
)

_TORQUE_CONVERTER_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7708,
        _7712,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6264,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
        _6311,
        _6341,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2406

    Self = TypeVar(
        "Self",
        bound="TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation._Cast_TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation"

    @property
    def coupling_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6314.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(
            _6314.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6341.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6341,
        )

        return self.__parent__._cast(
            _6341.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6311.ConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6311,
        )

        return self.__parent__._cast(
            _6311.ConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

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
    def torque_converter_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation":
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
class TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation(
    _6314.CouplingConnectionCompoundHarmonicAnalysisOfSingleExcitation
):
    """TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _TORQUE_CONVERTER_CONNECTION_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2406.TorqueConverterConnection":
        """mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2406.TorqueConverterConnection":
        """mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6264.TorqueConverterConnectionHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.TorqueConverterConnectionHarmonicAnalysisOfSingleExcitation]

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
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6264.TorqueConverterConnectionHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.TorqueConverterConnectionHarmonicAnalysisOfSingleExcitation]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation
        """
        return (
            _Cast_TorqueConverterConnectionCompoundHarmonicAnalysisOfSingleExcitation(
                self
            )
        )
