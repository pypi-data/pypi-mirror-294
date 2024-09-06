"""ComponentAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7242,
)

_COMPONENT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "ComponentAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7156,
        _7157,
        _7163,
        _7168,
        _7171,
        _7174,
        _7175,
        _7176,
        _7179,
        _7183,
        _7188,
        _7189,
        _7192,
        _7196,
        _7199,
        _7202,
        _7204,
        _7207,
        _7210,
        _7211,
        _7212,
        _7213,
        _7216,
        _7218,
        _7221,
        _7223,
        _7227,
        _7230,
        _7233,
        _7236,
        _7237,
        _7238,
        _7240,
        _7241,
        _7245,
        _7248,
        _7249,
        _7250,
        _7251,
        _7252,
        _7254,
        _7258,
        _7259,
        _7262,
        _7267,
        _7268,
        _7271,
        _7274,
        _7275,
        _7277,
        _7278,
        _7279,
        _7282,
        _7283,
        _7284,
        _7285,
        _7286,
        _7289,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _5998,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2799,
    )
    from mastapy._private.system_model.part_model import _2499

    Self = TypeVar("Self", bound="ComponentAdvancedTimeSteppingAnalysisForModulation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentAdvancedTimeSteppingAnalysisForModulation._Cast_ComponentAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting ComponentAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "ComponentAdvancedTimeSteppingAnalysisForModulation"

    @property
    def part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7242.PartAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7242.PartAdvancedTimeSteppingAnalysisForModulation
        )

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
    def abstract_shaft_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7156.AbstractShaftAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7156,
        )

        return self.__parent__._cast(
            _7156.AbstractShaftAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_shaft_or_housing_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7157.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7157,
        )

        return self.__parent__._cast(
            _7157.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def agma_gleason_conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7163.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7163,
        )

        return self.__parent__._cast(
            _7163.AGMAGleasonConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bearing_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7168.BearingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7168,
        )

        return self.__parent__._cast(
            _7168.BearingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7171.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7171,
        )

        return self.__parent__._cast(
            _7171.BevelDifferentialGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7174.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7174,
        )

        return self.__parent__._cast(
            _7174.BevelDifferentialPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_sun_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7175.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7175,
        )

        return self.__parent__._cast(
            _7175.BevelDifferentialSunGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7176.BevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7176,
        )

        return self.__parent__._cast(
            _7176.BevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bolt_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7179.BoltAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7179,
        )

        return self.__parent__._cast(
            _7179.BoltAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def clutch_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7183.ClutchHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7183,
        )

        return self.__parent__._cast(
            _7183.ClutchHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7188.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7188,
        )

        return self.__parent__._cast(
            _7188.ConceptCouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def concept_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7189.ConceptGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7189,
        )

        return self.__parent__._cast(
            _7189.ConceptGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7192.ConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7192,
        )

        return self.__parent__._cast(
            _7192.ConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connector_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7196.ConnectorAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7196,
        )

        return self.__parent__._cast(
            _7196.ConnectorAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7199.CouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7199,
        )

        return self.__parent__._cast(
            _7199.CouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cvt_pulley_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7202.CVTPulleyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7202,
        )

        return self.__parent__._cast(
            _7202.CVTPulleyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cycloidal_disc_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7204.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7204,
        )

        return self.__parent__._cast(
            _7204.CycloidalDiscAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7207.CylindricalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7207,
        )

        return self.__parent__._cast(
            _7207.CylindricalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def cylindrical_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7210.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7210,
        )

        return self.__parent__._cast(
            _7210.CylindricalPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def datum_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7211.DatumAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7211,
        )

        return self.__parent__._cast(
            _7211.DatumAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def external_cad_model_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7212.ExternalCADModelAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7212,
        )

        return self.__parent__._cast(
            _7212.ExternalCADModelAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def face_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7213.FaceGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7213,
        )

        return self.__parent__._cast(
            _7213.FaceGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def fe_part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7216.FEPartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7216,
        )

        return self.__parent__._cast(
            _7216.FEPartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7218.GearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7218,
        )

        return self.__parent__._cast(
            _7218.GearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def guide_dxf_model_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7221.GuideDxfModelAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7221,
        )

        return self.__parent__._cast(
            _7221.GuideDxfModelAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7223.HypoidGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7223,
        )

        return self.__parent__._cast(
            _7223.HypoidGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7227.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7227,
        )

        return self.__parent__._cast(
            _7227.KlingelnbergCycloPalloidConicalGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7230.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7230,
        )

        return self.__parent__._cast(
            _7230.KlingelnbergCycloPalloidHypoidGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7233.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7233,
        )

        return self.__parent__._cast(
            _7233.KlingelnbergCycloPalloidSpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mass_disc_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7236.MassDiscAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7236,
        )

        return self.__parent__._cast(
            _7236.MassDiscAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def measurement_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7237.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7237,
        )

        return self.__parent__._cast(
            _7237.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def microphone_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7238.MicrophoneAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7238,
        )

        return self.__parent__._cast(
            _7238.MicrophoneAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mountable_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7240.MountableComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7240,
        )

        return self.__parent__._cast(
            _7240.MountableComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def oil_seal_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7241.OilSealAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7241,
        )

        return self.__parent__._cast(
            _7241.OilSealAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_to_part_shear_coupling_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7245.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7245,
        )

        return self.__parent__._cast(
            _7245.PartToPartShearCouplingHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def planet_carrier_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7248.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7248,
        )

        return self.__parent__._cast(
            _7248.PlanetCarrierAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def point_load_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7249.PointLoadAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7249,
        )

        return self.__parent__._cast(
            _7249.PointLoadAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def power_load_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7250.PowerLoadAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7250,
        )

        return self.__parent__._cast(
            _7250.PowerLoadAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def pulley_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7251.PulleyAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7251,
        )

        return self.__parent__._cast(
            _7251.PulleyAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def ring_pins_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7252.RingPinsAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7252,
        )

        return self.__parent__._cast(
            _7252.RingPinsAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def rolling_ring_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7254.RollingRingAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7254,
        )

        return self.__parent__._cast(
            _7254.RollingRingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7258.ShaftAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7258,
        )

        return self.__parent__._cast(
            _7258.ShaftAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def shaft_hub_connection_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7259.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7259,
        )

        return self.__parent__._cast(
            _7259.ShaftHubConnectionAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7262.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7262,
        )

        return self.__parent__._cast(
            _7262.SpiralBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spring_damper_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7267.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7267,
        )

        return self.__parent__._cast(
            _7267.SpringDamperHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7268.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7268,
        )

        return self.__parent__._cast(
            _7268.StraightBevelDiffGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7271.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7271,
        )

        return self.__parent__._cast(
            _7271.StraightBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_planet_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7274.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7274,
        )

        return self.__parent__._cast(
            _7274.StraightBevelPlanetGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_sun_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7275.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7275,
        )

        return self.__parent__._cast(
            _7275.StraightBevelSunGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_half_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7277.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7277,
        )

        return self.__parent__._cast(
            _7277.SynchroniserHalfAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7278.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7278,
        )

        return self.__parent__._cast(
            _7278.SynchroniserPartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def synchroniser_sleeve_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7279.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7279,
        )

        return self.__parent__._cast(
            _7279.SynchroniserSleeveAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_pump_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7282.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7282,
        )

        return self.__parent__._cast(
            _7282.TorqueConverterPumpAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def torque_converter_turbine_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7283.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7283,
        )

        return self.__parent__._cast(
            _7283.TorqueConverterTurbineAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def unbalanced_mass_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7284.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7284,
        )

        return self.__parent__._cast(
            _7284.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def virtual_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7285.VirtualComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7285,
        )

        return self.__parent__._cast(
            _7285.VirtualComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def worm_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7286.WormGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7286,
        )

        return self.__parent__._cast(
            _7286.WormGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7289.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7289,
        )

        return self.__parent__._cast(
            _7289.ZerolBevelGearAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "ComponentAdvancedTimeSteppingAnalysisForModulation":
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
class ComponentAdvancedTimeSteppingAnalysisForModulation(
    _7242.PartAdvancedTimeSteppingAnalysisForModulation
):
    """ComponentAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def magnitude_of_rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MagnitudeOfRotation")

        if temp is None:
            return 0.0

        return temp

    @magnitude_of_rotation.setter
    @enforce_parameter_types
    def magnitude_of_rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MagnitudeOfRotation",
            float(value) if value is not None else 0.0,
        )

    @property
    def component_design(self: "Self") -> "_2499.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def results(self: "Self") -> "_5998.HarmonicAnalysisResultsPropertyAccessor":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.HarmonicAnalysisResultsPropertyAccessor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Results")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: "Self") -> "_2799.ComponentSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ComponentSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ComponentAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_ComponentAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_ComponentAdvancedTimeSteppingAnalysisForModulation(self)
