"""PartCompoundAdvancedSystemDeflection"""

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

_PART_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "PartCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7510,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7561,
        _7562,
        _7563,
        _7565,
        _7567,
        _7568,
        _7569,
        _7571,
        _7572,
        _7574,
        _7575,
        _7576,
        _7577,
        _7579,
        _7580,
        _7581,
        _7582,
        _7584,
        _7586,
        _7587,
        _7589,
        _7590,
        _7592,
        _7593,
        _7595,
        _7597,
        _7598,
        _7600,
        _7602,
        _7603,
        _7604,
        _7606,
        _7608,
        _7610,
        _7611,
        _7612,
        _7613,
        _7614,
        _7616,
        _7617,
        _7618,
        _7619,
        _7621,
        _7622,
        _7623,
        _7625,
        _7627,
        _7629,
        _7630,
        _7632,
        _7633,
        _7635,
        _7636,
        _7637,
        _7638,
        _7639,
        _7640,
        _7641,
        _7643,
        _7645,
        _7647,
        _7648,
        _7649,
        _7650,
        _7651,
        _7652,
        _7654,
        _7655,
        _7657,
        _7658,
        _7659,
        _7661,
        _7662,
        _7664,
        _7665,
        _7667,
        _7668,
        _7670,
        _7671,
        _7673,
        _7674,
        _7675,
        _7676,
        _7677,
        _7678,
        _7679,
        _7680,
        _7682,
        _7683,
        _7684,
        _7685,
        _7686,
        _7688,
        _7689,
        _7691,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7712

    Self = TypeVar("Self", bound="PartCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartCompoundAdvancedSystemDeflection._Cast_PartCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartCompoundAdvancedSystemDeflection:
    """Special nested class for casting PartCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "PartCompoundAdvancedSystemDeflection"

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
    def abstract_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7561.AbstractAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7561,
        )

        return self.__parent__._cast(
            _7561.AbstractAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def abstract_shaft_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7562.AbstractShaftCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7562,
        )

        return self.__parent__._cast(
            _7562.AbstractShaftCompoundAdvancedSystemDeflection
        )

    @property
    def abstract_shaft_or_housing_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7563.AbstractShaftOrHousingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7563,
        )

        return self.__parent__._cast(
            _7563.AbstractShaftOrHousingCompoundAdvancedSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7565.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7565,
        )

        return self.__parent__._cast(
            _7565.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection
        )

    @property
    def agma_gleason_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7567.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7567,
        )

        return self.__parent__._cast(
            _7567.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7568.AssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7568,
        )

        return self.__parent__._cast(_7568.AssemblyCompoundAdvancedSystemDeflection)

    @property
    def bearing_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7569.BearingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7569,
        )

        return self.__parent__._cast(_7569.BearingCompoundAdvancedSystemDeflection)

    @property
    def belt_drive_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7571.BeltDriveCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7571,
        )

        return self.__parent__._cast(_7571.BeltDriveCompoundAdvancedSystemDeflection)

    @property
    def bevel_differential_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7572.BevelDifferentialGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7572,
        )

        return self.__parent__._cast(
            _7572.BevelDifferentialGearCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_differential_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7574.BevelDifferentialGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7574,
        )

        return self.__parent__._cast(
            _7574.BevelDifferentialGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_differential_planet_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7575.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7575,
        )

        return self.__parent__._cast(
            _7575.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_differential_sun_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7576.BevelDifferentialSunGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7576,
        )

        return self.__parent__._cast(
            _7576.BevelDifferentialSunGearCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7577.BevelGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7577,
        )

        return self.__parent__._cast(_7577.BevelGearCompoundAdvancedSystemDeflection)

    @property
    def bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7579.BevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7579,
        )

        return self.__parent__._cast(_7579.BevelGearSetCompoundAdvancedSystemDeflection)

    @property
    def bolt_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7580.BoltCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7580,
        )

        return self.__parent__._cast(_7580.BoltCompoundAdvancedSystemDeflection)

    @property
    def bolted_joint_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7581.BoltedJointCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7581,
        )

        return self.__parent__._cast(_7581.BoltedJointCompoundAdvancedSystemDeflection)

    @property
    def clutch_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7582.ClutchCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7582,
        )

        return self.__parent__._cast(_7582.ClutchCompoundAdvancedSystemDeflection)

    @property
    def clutch_half_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7584.ClutchHalfCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7584,
        )

        return self.__parent__._cast(_7584.ClutchHalfCompoundAdvancedSystemDeflection)

    @property
    def component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7586.ComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7586,
        )

        return self.__parent__._cast(_7586.ComponentCompoundAdvancedSystemDeflection)

    @property
    def concept_coupling_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7587.ConceptCouplingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7587,
        )

        return self.__parent__._cast(
            _7587.ConceptCouplingCompoundAdvancedSystemDeflection
        )

    @property
    def concept_coupling_half_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7589.ConceptCouplingHalfCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7589,
        )

        return self.__parent__._cast(
            _7589.ConceptCouplingHalfCompoundAdvancedSystemDeflection
        )

    @property
    def concept_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7590.ConceptGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7590,
        )

        return self.__parent__._cast(_7590.ConceptGearCompoundAdvancedSystemDeflection)

    @property
    def concept_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7592.ConceptGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7592,
        )

        return self.__parent__._cast(
            _7592.ConceptGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7593.ConicalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7593,
        )

        return self.__parent__._cast(_7593.ConicalGearCompoundAdvancedSystemDeflection)

    @property
    def conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7595.ConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7595,
        )

        return self.__parent__._cast(
            _7595.ConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def connector_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7597.ConnectorCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7597,
        )

        return self.__parent__._cast(_7597.ConnectorCompoundAdvancedSystemDeflection)

    @property
    def coupling_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7598.CouplingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7598,
        )

        return self.__parent__._cast(_7598.CouplingCompoundAdvancedSystemDeflection)

    @property
    def coupling_half_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7600.CouplingHalfCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7600,
        )

        return self.__parent__._cast(_7600.CouplingHalfCompoundAdvancedSystemDeflection)

    @property
    def cvt_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7602.CVTCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7602,
        )

        return self.__parent__._cast(_7602.CVTCompoundAdvancedSystemDeflection)

    @property
    def cvt_pulley_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7603.CVTPulleyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7603,
        )

        return self.__parent__._cast(_7603.CVTPulleyCompoundAdvancedSystemDeflection)

    @property
    def cycloidal_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7604.CycloidalAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7604,
        )

        return self.__parent__._cast(
            _7604.CycloidalAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def cycloidal_disc_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7606.CycloidalDiscCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7606,
        )

        return self.__parent__._cast(
            _7606.CycloidalDiscCompoundAdvancedSystemDeflection
        )

    @property
    def cylindrical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7608.CylindricalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7608,
        )

        return self.__parent__._cast(
            _7608.CylindricalGearCompoundAdvancedSystemDeflection
        )

    @property
    def cylindrical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7610.CylindricalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7610,
        )

        return self.__parent__._cast(
            _7610.CylindricalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def cylindrical_planet_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7611.CylindricalPlanetGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7611,
        )

        return self.__parent__._cast(
            _7611.CylindricalPlanetGearCompoundAdvancedSystemDeflection
        )

    @property
    def datum_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7612.DatumCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7612,
        )

        return self.__parent__._cast(_7612.DatumCompoundAdvancedSystemDeflection)

    @property
    def external_cad_model_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7613.ExternalCADModelCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7613,
        )

        return self.__parent__._cast(
            _7613.ExternalCADModelCompoundAdvancedSystemDeflection
        )

    @property
    def face_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7614.FaceGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7614,
        )

        return self.__parent__._cast(_7614.FaceGearCompoundAdvancedSystemDeflection)

    @property
    def face_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7616.FaceGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7616,
        )

        return self.__parent__._cast(_7616.FaceGearSetCompoundAdvancedSystemDeflection)

    @property
    def fe_part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7617.FEPartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7617,
        )

        return self.__parent__._cast(_7617.FEPartCompoundAdvancedSystemDeflection)

    @property
    def flexible_pin_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7618.FlexiblePinAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7618,
        )

        return self.__parent__._cast(
            _7618.FlexiblePinAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7619.GearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7619,
        )

        return self.__parent__._cast(_7619.GearCompoundAdvancedSystemDeflection)

    @property
    def gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7621.GearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7621,
        )

        return self.__parent__._cast(_7621.GearSetCompoundAdvancedSystemDeflection)

    @property
    def guide_dxf_model_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7622.GuideDxfModelCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7622,
        )

        return self.__parent__._cast(
            _7622.GuideDxfModelCompoundAdvancedSystemDeflection
        )

    @property
    def hypoid_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7623.HypoidGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7623,
        )

        return self.__parent__._cast(_7623.HypoidGearCompoundAdvancedSystemDeflection)

    @property
    def hypoid_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7625.HypoidGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7625,
        )

        return self.__parent__._cast(
            _7625.HypoidGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7627.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7627,
        )

        return self.__parent__._cast(
            _7627.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7629.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7629,
        )

        return self.__parent__._cast(
            _7629.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7630.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7630,
        )

        return self.__parent__._cast(
            _7630.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7632.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7632,
        )

        return self.__parent__._cast(
            _7632.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> (
        "_7633.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection"
    ):
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7633,
        )

        return self.__parent__._cast(
            _7633.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7635.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7635,
        )

        return self.__parent__._cast(
            _7635.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def mass_disc_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7636.MassDiscCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7636,
        )

        return self.__parent__._cast(_7636.MassDiscCompoundAdvancedSystemDeflection)

    @property
    def measurement_component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7637.MeasurementComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7637,
        )

        return self.__parent__._cast(
            _7637.MeasurementComponentCompoundAdvancedSystemDeflection
        )

    @property
    def microphone_array_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7638.MicrophoneArrayCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7638,
        )

        return self.__parent__._cast(
            _7638.MicrophoneArrayCompoundAdvancedSystemDeflection
        )

    @property
    def microphone_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7639.MicrophoneCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7639,
        )

        return self.__parent__._cast(_7639.MicrophoneCompoundAdvancedSystemDeflection)

    @property
    def mountable_component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7640.MountableComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7640,
        )

        return self.__parent__._cast(
            _7640.MountableComponentCompoundAdvancedSystemDeflection
        )

    @property
    def oil_seal_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7641.OilSealCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7641,
        )

        return self.__parent__._cast(_7641.OilSealCompoundAdvancedSystemDeflection)

    @property
    def part_to_part_shear_coupling_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7643.PartToPartShearCouplingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7643,
        )

        return self.__parent__._cast(
            _7643.PartToPartShearCouplingCompoundAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_half_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7645.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7645,
        )

        return self.__parent__._cast(
            _7645.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection
        )

    @property
    def planetary_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7647.PlanetaryGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7647,
        )

        return self.__parent__._cast(
            _7647.PlanetaryGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def planet_carrier_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7648.PlanetCarrierCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7648,
        )

        return self.__parent__._cast(
            _7648.PlanetCarrierCompoundAdvancedSystemDeflection
        )

    @property
    def point_load_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7649.PointLoadCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7649,
        )

        return self.__parent__._cast(_7649.PointLoadCompoundAdvancedSystemDeflection)

    @property
    def power_load_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7650.PowerLoadCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7650,
        )

        return self.__parent__._cast(_7650.PowerLoadCompoundAdvancedSystemDeflection)

    @property
    def pulley_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7651.PulleyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7651,
        )

        return self.__parent__._cast(_7651.PulleyCompoundAdvancedSystemDeflection)

    @property
    def ring_pins_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7652.RingPinsCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7652,
        )

        return self.__parent__._cast(_7652.RingPinsCompoundAdvancedSystemDeflection)

    @property
    def rolling_ring_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7654.RollingRingAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7654,
        )

        return self.__parent__._cast(
            _7654.RollingRingAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def rolling_ring_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7655.RollingRingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7655,
        )

        return self.__parent__._cast(_7655.RollingRingCompoundAdvancedSystemDeflection)

    @property
    def root_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7657.RootAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7657,
        )

        return self.__parent__._cast(_7657.RootAssemblyCompoundAdvancedSystemDeflection)

    @property
    def shaft_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7658.ShaftCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7658,
        )

        return self.__parent__._cast(_7658.ShaftCompoundAdvancedSystemDeflection)

    @property
    def shaft_hub_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7659.ShaftHubConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7659,
        )

        return self.__parent__._cast(
            _7659.ShaftHubConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def specialised_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7661.SpecialisedAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7661,
        )

        return self.__parent__._cast(
            _7661.SpecialisedAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7662.SpiralBevelGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7662,
        )

        return self.__parent__._cast(
            _7662.SpiralBevelGearCompoundAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7664.SpiralBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7664,
        )

        return self.__parent__._cast(
            _7664.SpiralBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def spring_damper_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7665.SpringDamperCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7665,
        )

        return self.__parent__._cast(_7665.SpringDamperCompoundAdvancedSystemDeflection)

    @property
    def spring_damper_half_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7667.SpringDamperHalfCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7667,
        )

        return self.__parent__._cast(
            _7667.SpringDamperHalfCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7668.StraightBevelDiffGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7668,
        )

        return self.__parent__._cast(
            _7668.StraightBevelDiffGearCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_diff_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7670.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7670,
        )

        return self.__parent__._cast(
            _7670.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7671.StraightBevelGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7671,
        )

        return self.__parent__._cast(
            _7671.StraightBevelGearCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7673.StraightBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7673,
        )

        return self.__parent__._cast(
            _7673.StraightBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_planet_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7674.StraightBevelPlanetGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7674,
        )

        return self.__parent__._cast(
            _7674.StraightBevelPlanetGearCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_sun_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7675.StraightBevelSunGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7675,
        )

        return self.__parent__._cast(
            _7675.StraightBevelSunGearCompoundAdvancedSystemDeflection
        )

    @property
    def synchroniser_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7676.SynchroniserCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7676,
        )

        return self.__parent__._cast(_7676.SynchroniserCompoundAdvancedSystemDeflection)

    @property
    def synchroniser_half_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7677.SynchroniserHalfCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7677,
        )

        return self.__parent__._cast(
            _7677.SynchroniserHalfCompoundAdvancedSystemDeflection
        )

    @property
    def synchroniser_part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7678.SynchroniserPartCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7678,
        )

        return self.__parent__._cast(
            _7678.SynchroniserPartCompoundAdvancedSystemDeflection
        )

    @property
    def synchroniser_sleeve_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7679.SynchroniserSleeveCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7679,
        )

        return self.__parent__._cast(
            _7679.SynchroniserSleeveCompoundAdvancedSystemDeflection
        )

    @property
    def torque_converter_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7680.TorqueConverterCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7680,
        )

        return self.__parent__._cast(
            _7680.TorqueConverterCompoundAdvancedSystemDeflection
        )

    @property
    def torque_converter_pump_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7682.TorqueConverterPumpCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7682,
        )

        return self.__parent__._cast(
            _7682.TorqueConverterPumpCompoundAdvancedSystemDeflection
        )

    @property
    def torque_converter_turbine_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7683.TorqueConverterTurbineCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7683,
        )

        return self.__parent__._cast(
            _7683.TorqueConverterTurbineCompoundAdvancedSystemDeflection
        )

    @property
    def unbalanced_mass_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7684.UnbalancedMassCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7684,
        )

        return self.__parent__._cast(
            _7684.UnbalancedMassCompoundAdvancedSystemDeflection
        )

    @property
    def virtual_component_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7685.VirtualComponentCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7685,
        )

        return self.__parent__._cast(
            _7685.VirtualComponentCompoundAdvancedSystemDeflection
        )

    @property
    def worm_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7686.WormGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7686,
        )

        return self.__parent__._cast(_7686.WormGearCompoundAdvancedSystemDeflection)

    @property
    def worm_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7688.WormGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7688,
        )

        return self.__parent__._cast(_7688.WormGearSetCompoundAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7689.ZerolBevelGearCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7689,
        )

        return self.__parent__._cast(
            _7689.ZerolBevelGearCompoundAdvancedSystemDeflection
        )

    @property
    def zerol_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7691.ZerolBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7691,
        )

        return self.__parent__._cast(
            _7691.ZerolBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "PartCompoundAdvancedSystemDeflection":
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
class PartCompoundAdvancedSystemDeflection(_7715.PartCompoundAnalysis):
    """PartCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_7510.PartAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection]

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
    ) -> "List[_7510.PartAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection]

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
    def cast_to(self: "Self") -> "_Cast_PartCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_PartCompoundAdvancedSystemDeflection
        """
        return _Cast_PartCompoundAdvancedSystemDeflection(self)
