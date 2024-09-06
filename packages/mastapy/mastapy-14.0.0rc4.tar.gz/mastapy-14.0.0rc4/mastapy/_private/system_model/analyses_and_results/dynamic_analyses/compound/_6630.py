"""PartCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7715

_PART_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "PartCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7712
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6499,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6549,
        _6550,
        _6551,
        _6553,
        _6555,
        _6556,
        _6557,
        _6559,
        _6560,
        _6562,
        _6563,
        _6564,
        _6565,
        _6567,
        _6568,
        _6569,
        _6570,
        _6572,
        _6574,
        _6575,
        _6577,
        _6578,
        _6580,
        _6581,
        _6583,
        _6585,
        _6586,
        _6588,
        _6590,
        _6591,
        _6592,
        _6594,
        _6596,
        _6598,
        _6599,
        _6600,
        _6601,
        _6602,
        _6604,
        _6605,
        _6606,
        _6607,
        _6609,
        _6610,
        _6611,
        _6613,
        _6615,
        _6617,
        _6618,
        _6620,
        _6621,
        _6623,
        _6624,
        _6625,
        _6626,
        _6627,
        _6628,
        _6629,
        _6631,
        _6633,
        _6635,
        _6636,
        _6637,
        _6638,
        _6639,
        _6640,
        _6642,
        _6643,
        _6645,
        _6646,
        _6647,
        _6649,
        _6650,
        _6652,
        _6653,
        _6655,
        _6656,
        _6658,
        _6659,
        _6661,
        _6662,
        _6663,
        _6664,
        _6665,
        _6666,
        _6667,
        _6668,
        _6670,
        _6671,
        _6672,
        _6673,
        _6674,
        _6676,
        _6677,
        _6679,
    )

    Self = TypeVar("Self", bound="PartCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartCompoundDynamicAnalysis._Cast_PartCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundDynamicAnalysis:
    """Special nested class for casting PartCompoundDynamicAnalysis to subclasses."""

    __parent__: "PartCompoundDynamicAnalysis"

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7715.PartCompoundAnalysis":
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
    def abstract_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6549.AbstractAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6549,
        )

        return self.__parent__._cast(_6549.AbstractAssemblyCompoundDynamicAnalysis)

    @property
    def abstract_shaft_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6550.AbstractShaftCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6550,
        )

        return self.__parent__._cast(_6550.AbstractShaftCompoundDynamicAnalysis)

    @property
    def abstract_shaft_or_housing_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6551.AbstractShaftOrHousingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6551,
        )

        return self.__parent__._cast(
            _6551.AbstractShaftOrHousingCompoundDynamicAnalysis
        )

    @property
    def agma_gleason_conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6553.AGMAGleasonConicalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6553,
        )

        return self.__parent__._cast(
            _6553.AGMAGleasonConicalGearCompoundDynamicAnalysis
        )

    @property
    def agma_gleason_conical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6555.AGMAGleasonConicalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6555,
        )

        return self.__parent__._cast(
            _6555.AGMAGleasonConicalGearSetCompoundDynamicAnalysis
        )

    @property
    def assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6556.AssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6556,
        )

        return self.__parent__._cast(_6556.AssemblyCompoundDynamicAnalysis)

    @property
    def bearing_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6557.BearingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6557,
        )

        return self.__parent__._cast(_6557.BearingCompoundDynamicAnalysis)

    @property
    def belt_drive_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6559.BeltDriveCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6559,
        )

        return self.__parent__._cast(_6559.BeltDriveCompoundDynamicAnalysis)

    @property
    def bevel_differential_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6560.BevelDifferentialGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6560,
        )

        return self.__parent__._cast(_6560.BevelDifferentialGearCompoundDynamicAnalysis)

    @property
    def bevel_differential_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6562.BevelDifferentialGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6562,
        )

        return self.__parent__._cast(
            _6562.BevelDifferentialGearSetCompoundDynamicAnalysis
        )

    @property
    def bevel_differential_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6563.BevelDifferentialPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6563,
        )

        return self.__parent__._cast(
            _6563.BevelDifferentialPlanetGearCompoundDynamicAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6564.BevelDifferentialSunGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6564,
        )

        return self.__parent__._cast(
            _6564.BevelDifferentialSunGearCompoundDynamicAnalysis
        )

    @property
    def bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6565.BevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6565,
        )

        return self.__parent__._cast(_6565.BevelGearCompoundDynamicAnalysis)

    @property
    def bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6567.BevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6567,
        )

        return self.__parent__._cast(_6567.BevelGearSetCompoundDynamicAnalysis)

    @property
    def bolt_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6568.BoltCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6568,
        )

        return self.__parent__._cast(_6568.BoltCompoundDynamicAnalysis)

    @property
    def bolted_joint_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6569.BoltedJointCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6569,
        )

        return self.__parent__._cast(_6569.BoltedJointCompoundDynamicAnalysis)

    @property
    def clutch_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6570.ClutchCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6570,
        )

        return self.__parent__._cast(_6570.ClutchCompoundDynamicAnalysis)

    @property
    def clutch_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6572.ClutchHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6572,
        )

        return self.__parent__._cast(_6572.ClutchHalfCompoundDynamicAnalysis)

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6574.ComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6574,
        )

        return self.__parent__._cast(_6574.ComponentCompoundDynamicAnalysis)

    @property
    def concept_coupling_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6575.ConceptCouplingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6575,
        )

        return self.__parent__._cast(_6575.ConceptCouplingCompoundDynamicAnalysis)

    @property
    def concept_coupling_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6577.ConceptCouplingHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6577,
        )

        return self.__parent__._cast(_6577.ConceptCouplingHalfCompoundDynamicAnalysis)

    @property
    def concept_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6578.ConceptGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6578,
        )

        return self.__parent__._cast(_6578.ConceptGearCompoundDynamicAnalysis)

    @property
    def concept_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6580.ConceptGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6580,
        )

        return self.__parent__._cast(_6580.ConceptGearSetCompoundDynamicAnalysis)

    @property
    def conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6581.ConicalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6581,
        )

        return self.__parent__._cast(_6581.ConicalGearCompoundDynamicAnalysis)

    @property
    def conical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6583.ConicalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6583,
        )

        return self.__parent__._cast(_6583.ConicalGearSetCompoundDynamicAnalysis)

    @property
    def connector_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6585.ConnectorCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6585,
        )

        return self.__parent__._cast(_6585.ConnectorCompoundDynamicAnalysis)

    @property
    def coupling_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6586.CouplingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6586,
        )

        return self.__parent__._cast(_6586.CouplingCompoundDynamicAnalysis)

    @property
    def coupling_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6588.CouplingHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6588,
        )

        return self.__parent__._cast(_6588.CouplingHalfCompoundDynamicAnalysis)

    @property
    def cvt_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6590.CVTCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6590,
        )

        return self.__parent__._cast(_6590.CVTCompoundDynamicAnalysis)

    @property
    def cvt_pulley_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6591.CVTPulleyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6591,
        )

        return self.__parent__._cast(_6591.CVTPulleyCompoundDynamicAnalysis)

    @property
    def cycloidal_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6592.CycloidalAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6592,
        )

        return self.__parent__._cast(_6592.CycloidalAssemblyCompoundDynamicAnalysis)

    @property
    def cycloidal_disc_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6594.CycloidalDiscCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6594,
        )

        return self.__parent__._cast(_6594.CycloidalDiscCompoundDynamicAnalysis)

    @property
    def cylindrical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6596.CylindricalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6596,
        )

        return self.__parent__._cast(_6596.CylindricalGearCompoundDynamicAnalysis)

    @property
    def cylindrical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6598.CylindricalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6598,
        )

        return self.__parent__._cast(_6598.CylindricalGearSetCompoundDynamicAnalysis)

    @property
    def cylindrical_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6599.CylindricalPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6599,
        )

        return self.__parent__._cast(_6599.CylindricalPlanetGearCompoundDynamicAnalysis)

    @property
    def datum_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6600.DatumCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6600,
        )

        return self.__parent__._cast(_6600.DatumCompoundDynamicAnalysis)

    @property
    def external_cad_model_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6601.ExternalCADModelCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6601,
        )

        return self.__parent__._cast(_6601.ExternalCADModelCompoundDynamicAnalysis)

    @property
    def face_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6602.FaceGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6602,
        )

        return self.__parent__._cast(_6602.FaceGearCompoundDynamicAnalysis)

    @property
    def face_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6604.FaceGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6604,
        )

        return self.__parent__._cast(_6604.FaceGearSetCompoundDynamicAnalysis)

    @property
    def fe_part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6605.FEPartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6605,
        )

        return self.__parent__._cast(_6605.FEPartCompoundDynamicAnalysis)

    @property
    def flexible_pin_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6606.FlexiblePinAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6606,
        )

        return self.__parent__._cast(_6606.FlexiblePinAssemblyCompoundDynamicAnalysis)

    @property
    def gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6607.GearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6607,
        )

        return self.__parent__._cast(_6607.GearCompoundDynamicAnalysis)

    @property
    def gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6609.GearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6609,
        )

        return self.__parent__._cast(_6609.GearSetCompoundDynamicAnalysis)

    @property
    def guide_dxf_model_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6610.GuideDxfModelCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6610,
        )

        return self.__parent__._cast(_6610.GuideDxfModelCompoundDynamicAnalysis)

    @property
    def hypoid_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6611.HypoidGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6611,
        )

        return self.__parent__._cast(_6611.HypoidGearCompoundDynamicAnalysis)

    @property
    def hypoid_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6613.HypoidGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6613,
        )

        return self.__parent__._cast(_6613.HypoidGearSetCompoundDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6615.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6615,
        )

        return self.__parent__._cast(
            _6615.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6617.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6617,
        )

        return self.__parent__._cast(
            _6617.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6618.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6618,
        )

        return self.__parent__._cast(
            _6618.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6620.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6620,
        )

        return self.__parent__._cast(
            _6620.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6621.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6621,
        )

        return self.__parent__._cast(
            _6621.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6623.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6623,
        )

        return self.__parent__._cast(
            _6623.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis
        )

    @property
    def mass_disc_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6624.MassDiscCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6624,
        )

        return self.__parent__._cast(_6624.MassDiscCompoundDynamicAnalysis)

    @property
    def measurement_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6625.MeasurementComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6625,
        )

        return self.__parent__._cast(_6625.MeasurementComponentCompoundDynamicAnalysis)

    @property
    def microphone_array_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6626.MicrophoneArrayCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6626,
        )

        return self.__parent__._cast(_6626.MicrophoneArrayCompoundDynamicAnalysis)

    @property
    def microphone_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6627.MicrophoneCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6627,
        )

        return self.__parent__._cast(_6627.MicrophoneCompoundDynamicAnalysis)

    @property
    def mountable_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6628.MountableComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6628,
        )

        return self.__parent__._cast(_6628.MountableComponentCompoundDynamicAnalysis)

    @property
    def oil_seal_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6629.OilSealCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6629,
        )

        return self.__parent__._cast(_6629.OilSealCompoundDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6631.PartToPartShearCouplingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6631,
        )

        return self.__parent__._cast(
            _6631.PartToPartShearCouplingCompoundDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6633.PartToPartShearCouplingHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6633,
        )

        return self.__parent__._cast(
            _6633.PartToPartShearCouplingHalfCompoundDynamicAnalysis
        )

    @property
    def planetary_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6635.PlanetaryGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6635,
        )

        return self.__parent__._cast(_6635.PlanetaryGearSetCompoundDynamicAnalysis)

    @property
    def planet_carrier_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6636.PlanetCarrierCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6636,
        )

        return self.__parent__._cast(_6636.PlanetCarrierCompoundDynamicAnalysis)

    @property
    def point_load_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6637.PointLoadCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6637,
        )

        return self.__parent__._cast(_6637.PointLoadCompoundDynamicAnalysis)

    @property
    def power_load_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6638.PowerLoadCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6638,
        )

        return self.__parent__._cast(_6638.PowerLoadCompoundDynamicAnalysis)

    @property
    def pulley_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6639.PulleyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6639,
        )

        return self.__parent__._cast(_6639.PulleyCompoundDynamicAnalysis)

    @property
    def ring_pins_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6640.RingPinsCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6640,
        )

        return self.__parent__._cast(_6640.RingPinsCompoundDynamicAnalysis)

    @property
    def rolling_ring_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6642.RollingRingAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6642,
        )

        return self.__parent__._cast(_6642.RollingRingAssemblyCompoundDynamicAnalysis)

    @property
    def rolling_ring_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6643.RollingRingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6643,
        )

        return self.__parent__._cast(_6643.RollingRingCompoundDynamicAnalysis)

    @property
    def root_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6645.RootAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6645,
        )

        return self.__parent__._cast(_6645.RootAssemblyCompoundDynamicAnalysis)

    @property
    def shaft_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6646.ShaftCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6646,
        )

        return self.__parent__._cast(_6646.ShaftCompoundDynamicAnalysis)

    @property
    def shaft_hub_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6647.ShaftHubConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6647,
        )

        return self.__parent__._cast(_6647.ShaftHubConnectionCompoundDynamicAnalysis)

    @property
    def specialised_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6649.SpecialisedAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6649,
        )

        return self.__parent__._cast(_6649.SpecialisedAssemblyCompoundDynamicAnalysis)

    @property
    def spiral_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6650.SpiralBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6650,
        )

        return self.__parent__._cast(_6650.SpiralBevelGearCompoundDynamicAnalysis)

    @property
    def spiral_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6652.SpiralBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6652,
        )

        return self.__parent__._cast(_6652.SpiralBevelGearSetCompoundDynamicAnalysis)

    @property
    def spring_damper_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6653.SpringDamperCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6653,
        )

        return self.__parent__._cast(_6653.SpringDamperCompoundDynamicAnalysis)

    @property
    def spring_damper_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6655.SpringDamperHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6655,
        )

        return self.__parent__._cast(_6655.SpringDamperHalfCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6656.StraightBevelDiffGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6656,
        )

        return self.__parent__._cast(_6656.StraightBevelDiffGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6658.StraightBevelDiffGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6658,
        )

        return self.__parent__._cast(
            _6658.StraightBevelDiffGearSetCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6659.StraightBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6659,
        )

        return self.__parent__._cast(_6659.StraightBevelGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6661.StraightBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6661,
        )

        return self.__parent__._cast(_6661.StraightBevelGearSetCompoundDynamicAnalysis)

    @property
    def straight_bevel_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6662.StraightBevelPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6662,
        )

        return self.__parent__._cast(
            _6662.StraightBevelPlanetGearCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6663.StraightBevelSunGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6663,
        )

        return self.__parent__._cast(_6663.StraightBevelSunGearCompoundDynamicAnalysis)

    @property
    def synchroniser_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6664.SynchroniserCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6664,
        )

        return self.__parent__._cast(_6664.SynchroniserCompoundDynamicAnalysis)

    @property
    def synchroniser_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6665.SynchroniserHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6665,
        )

        return self.__parent__._cast(_6665.SynchroniserHalfCompoundDynamicAnalysis)

    @property
    def synchroniser_part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6666.SynchroniserPartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6666,
        )

        return self.__parent__._cast(_6666.SynchroniserPartCompoundDynamicAnalysis)

    @property
    def synchroniser_sleeve_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6667.SynchroniserSleeveCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6667,
        )

        return self.__parent__._cast(_6667.SynchroniserSleeveCompoundDynamicAnalysis)

    @property
    def torque_converter_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6668.TorqueConverterCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6668,
        )

        return self.__parent__._cast(_6668.TorqueConverterCompoundDynamicAnalysis)

    @property
    def torque_converter_pump_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6670.TorqueConverterPumpCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6670,
        )

        return self.__parent__._cast(_6670.TorqueConverterPumpCompoundDynamicAnalysis)

    @property
    def torque_converter_turbine_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6671.TorqueConverterTurbineCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6671,
        )

        return self.__parent__._cast(
            _6671.TorqueConverterTurbineCompoundDynamicAnalysis
        )

    @property
    def unbalanced_mass_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6672.UnbalancedMassCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6672,
        )

        return self.__parent__._cast(_6672.UnbalancedMassCompoundDynamicAnalysis)

    @property
    def virtual_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6673.VirtualComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6673,
        )

        return self.__parent__._cast(_6673.VirtualComponentCompoundDynamicAnalysis)

    @property
    def worm_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6674.WormGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6674,
        )

        return self.__parent__._cast(_6674.WormGearCompoundDynamicAnalysis)

    @property
    def worm_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6676.WormGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6676,
        )

        return self.__parent__._cast(_6676.WormGearSetCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6677.ZerolBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6677,
        )

        return self.__parent__._cast(_6677.ZerolBevelGearCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_set_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6679.ZerolBevelGearSetCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6679,
        )

        return self.__parent__._cast(_6679.ZerolBevelGearSetCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "PartCompoundDynamicAnalysis":
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
class PartCompoundDynamicAnalysis(_7715.PartCompoundAnalysis):
    """PartCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(self: "Self") -> "List[_6499.PartDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.PartDynamicAnalysis]

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
    ) -> "List[_6499.PartDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.PartDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_PartCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundDynamicAnalysis
        """
        return _Cast_PartCompoundDynamicAnalysis(self)
