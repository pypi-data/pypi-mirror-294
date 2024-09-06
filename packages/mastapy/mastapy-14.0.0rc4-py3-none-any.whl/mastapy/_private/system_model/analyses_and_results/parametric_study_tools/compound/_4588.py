"""ConnectionCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7708

_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "ConnectionCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7712
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4439,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4556,
        _4558,
        _4562,
        _4565,
        _4570,
        _4575,
        _4577,
        _4580,
        _4583,
        _4586,
        _4591,
        _4593,
        _4597,
        _4599,
        _4601,
        _4607,
        _4612,
        _4616,
        _4618,
        _4620,
        _4623,
        _4626,
        _4636,
        _4638,
        _4645,
        _4648,
        _4652,
        _4655,
        _4658,
        _4661,
        _4664,
        _4673,
        _4679,
        _4682,
    )
    from mastapy._private.utility_gui import _1903

    Self = TypeVar("Self", bound="ConnectionCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionCompoundParametricStudyTool._Cast_ConnectionCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionCompoundParametricStudyTool:
    """Special nested class for casting ConnectionCompoundParametricStudyTool to subclasses."""

    __parent__: "ConnectionCompoundParametricStudyTool"

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7708.ConnectionCompoundAnalysis":
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
    def abstract_shaft_to_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4556.AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4556,
        )

        return self.__parent__._cast(
            _4556.AbstractShaftToMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4558.AGMAGleasonConicalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4558,
        )

        return self.__parent__._cast(
            _4558.AGMAGleasonConicalGearMeshCompoundParametricStudyTool
        )

    @property
    def belt_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4562.BeltConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4562,
        )

        return self.__parent__._cast(_4562.BeltConnectionCompoundParametricStudyTool)

    @property
    def bevel_differential_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4565.BevelDifferentialGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4565,
        )

        return self.__parent__._cast(
            _4565.BevelDifferentialGearMeshCompoundParametricStudyTool
        )

    @property
    def bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4570.BevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4570,
        )

        return self.__parent__._cast(_4570.BevelGearMeshCompoundParametricStudyTool)

    @property
    def clutch_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4575.ClutchConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4575,
        )

        return self.__parent__._cast(_4575.ClutchConnectionCompoundParametricStudyTool)

    @property
    def coaxial_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4577.CoaxialConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4577,
        )

        return self.__parent__._cast(_4577.CoaxialConnectionCompoundParametricStudyTool)

    @property
    def concept_coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4580.ConceptCouplingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4580,
        )

        return self.__parent__._cast(
            _4580.ConceptCouplingConnectionCompoundParametricStudyTool
        )

    @property
    def concept_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4583.ConceptGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4583,
        )

        return self.__parent__._cast(_4583.ConceptGearMeshCompoundParametricStudyTool)

    @property
    def conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4586.ConicalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4586,
        )

        return self.__parent__._cast(_4586.ConicalGearMeshCompoundParametricStudyTool)

    @property
    def coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4591.CouplingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4591,
        )

        return self.__parent__._cast(
            _4591.CouplingConnectionCompoundParametricStudyTool
        )

    @property
    def cvt_belt_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4593.CVTBeltConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4593,
        )

        return self.__parent__._cast(_4593.CVTBeltConnectionCompoundParametricStudyTool)

    @property
    def cycloidal_disc_central_bearing_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4597.CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4597,
        )

        return self.__parent__._cast(
            _4597.CycloidalDiscCentralBearingConnectionCompoundParametricStudyTool
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4599.CycloidalDiscPlanetaryBearingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4599,
        )

        return self.__parent__._cast(
            _4599.CycloidalDiscPlanetaryBearingConnectionCompoundParametricStudyTool
        )

    @property
    def cylindrical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4601.CylindricalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4601,
        )

        return self.__parent__._cast(
            _4601.CylindricalGearMeshCompoundParametricStudyTool
        )

    @property
    def face_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4607.FaceGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4607,
        )

        return self.__parent__._cast(_4607.FaceGearMeshCompoundParametricStudyTool)

    @property
    def gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4612.GearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4612,
        )

        return self.__parent__._cast(_4612.GearMeshCompoundParametricStudyTool)

    @property
    def hypoid_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4616.HypoidGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4616,
        )

        return self.__parent__._cast(_4616.HypoidGearMeshCompoundParametricStudyTool)

    @property
    def inter_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4618.InterMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4618,
        )

        return self.__parent__._cast(
            _4618.InterMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4620.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4620,
        )

        return self.__parent__._cast(
            _4620.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4623.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4623,
        )

        return self.__parent__._cast(
            _4623.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4626.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4626,
        )

        return self.__parent__._cast(
            _4626.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def part_to_part_shear_coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4636.PartToPartShearCouplingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4636,
        )

        return self.__parent__._cast(
            _4636.PartToPartShearCouplingConnectionCompoundParametricStudyTool
        )

    @property
    def planetary_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4638.PlanetaryConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4638,
        )

        return self.__parent__._cast(
            _4638.PlanetaryConnectionCompoundParametricStudyTool
        )

    @property
    def ring_pins_to_disc_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4645.RingPinsToDiscConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4645,
        )

        return self.__parent__._cast(
            _4645.RingPinsToDiscConnectionCompoundParametricStudyTool
        )

    @property
    def rolling_ring_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4648.RollingRingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4648,
        )

        return self.__parent__._cast(
            _4648.RollingRingConnectionCompoundParametricStudyTool
        )

    @property
    def shaft_to_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4652.ShaftToMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4652,
        )

        return self.__parent__._cast(
            _4652.ShaftToMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def spiral_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4655.SpiralBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4655,
        )

        return self.__parent__._cast(
            _4655.SpiralBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def spring_damper_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4658.SpringDamperConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4658,
        )

        return self.__parent__._cast(
            _4658.SpringDamperConnectionCompoundParametricStudyTool
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4661.StraightBevelDiffGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4661,
        )

        return self.__parent__._cast(
            _4661.StraightBevelDiffGearMeshCompoundParametricStudyTool
        )

    @property
    def straight_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4664.StraightBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4664,
        )

        return self.__parent__._cast(
            _4664.StraightBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def torque_converter_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4673.TorqueConverterConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4673,
        )

        return self.__parent__._cast(
            _4673.TorqueConverterConnectionCompoundParametricStudyTool
        )

    @property
    def worm_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4679.WormGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4679,
        )

        return self.__parent__._cast(_4679.WormGearMeshCompoundParametricStudyTool)

    @property
    def zerol_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4682.ZerolBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4682,
        )

        return self.__parent__._cast(
            _4682.ZerolBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "ConnectionCompoundParametricStudyTool":
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
class ConnectionCompoundParametricStudyTool(_7708.ConnectionCompoundAnalysis):
    """ConnectionCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def data_logger(self: "Self") -> "_1903.DataLoggerWithCharts":
        """mastapy.utility_gui.DataLoggerWithCharts

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DataLogger")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4439.ConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool]

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
    ) -> "List[_4439.ConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_ConnectionCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ConnectionCompoundParametricStudyTool
        """
        return _Cast_ConnectionCompoundParametricStudyTool(self)
