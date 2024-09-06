"""ComponentHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
    _6226,
)

_COMPONENT_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation",
    "ComponentHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7714,
        _7717,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6144,
        _6145,
        _6147,
        _6151,
        _6154,
        _6157,
        _6158,
        _6159,
        _6163,
        _6165,
        _6170,
        _6172,
        _6175,
        _6179,
        _6181,
        _6185,
        _6188,
        _6190,
        _6193,
        _6194,
        _6195,
        _6196,
        _6199,
        _6201,
        _6204,
        _6206,
        _6210,
        _6213,
        _6216,
        _6219,
        _6220,
        _6222,
        _6224,
        _6225,
        _6228,
        _6232,
        _6233,
        _6234,
        _6235,
        _6236,
        _6240,
        _6242,
        _6243,
        _6246,
        _6250,
        _6252,
        _6255,
        _6258,
        _6259,
        _6260,
        _6262,
        _6263,
        _6266,
        _6267,
        _6268,
        _6269,
        _6270,
        _6273,
    )
    from mastapy._private.system_model.part_model import _2499

    Self = TypeVar("Self", bound="ComponentHarmonicAnalysisOfSingleExcitation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentHarmonicAnalysisOfSingleExcitation._Cast_ComponentHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting ComponentHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "ComponentHarmonicAnalysisOfSingleExcitation"

    @property
    def part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6226.PartHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(_6226.PartHarmonicAnalysisOfSingleExcitation)

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
    def abstract_shaft_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6144.AbstractShaftHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6144,
        )

        return self.__parent__._cast(
            _6144.AbstractShaftHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_shaft_or_housing_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6145.AbstractShaftOrHousingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6145,
        )

        return self.__parent__._cast(
            _6145.AbstractShaftOrHousingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6147.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6147,
        )

        return self.__parent__._cast(
            _6147.AGMAGleasonConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bearing_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6151.BearingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6151,
        )

        return self.__parent__._cast(_6151.BearingHarmonicAnalysisOfSingleExcitation)

    @property
    def bevel_differential_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6154.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6154,
        )

        return self.__parent__._cast(
            _6154.BevelDifferentialGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6157.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6157,
        )

        return self.__parent__._cast(
            _6157.BevelDifferentialPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_differential_sun_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6158.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6158,
        )

        return self.__parent__._cast(
            _6158.BevelDifferentialSunGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6159.BevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6159,
        )

        return self.__parent__._cast(_6159.BevelGearHarmonicAnalysisOfSingleExcitation)

    @property
    def bolt_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6163.BoltHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6163,
        )

        return self.__parent__._cast(_6163.BoltHarmonicAnalysisOfSingleExcitation)

    @property
    def clutch_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6165.ClutchHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6165,
        )

        return self.__parent__._cast(_6165.ClutchHalfHarmonicAnalysisOfSingleExcitation)

    @property
    def concept_coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6170.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6170,
        )

        return self.__parent__._cast(
            _6170.ConceptCouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def concept_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6172.ConceptGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6172,
        )

        return self.__parent__._cast(
            _6172.ConceptGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6175.ConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6175,
        )

        return self.__parent__._cast(
            _6175.ConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connector_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6179.ConnectorHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6179,
        )

        return self.__parent__._cast(_6179.ConnectorHarmonicAnalysisOfSingleExcitation)

    @property
    def coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6181.CouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6181,
        )

        return self.__parent__._cast(
            _6181.CouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cvt_pulley_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6185.CVTPulleyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6185,
        )

        return self.__parent__._cast(_6185.CVTPulleyHarmonicAnalysisOfSingleExcitation)

    @property
    def cycloidal_disc_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6188.CycloidalDiscHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6188,
        )

        return self.__parent__._cast(
            _6188.CycloidalDiscHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6190.CylindricalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6190,
        )

        return self.__parent__._cast(
            _6190.CylindricalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def cylindrical_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6193.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6193,
        )

        return self.__parent__._cast(
            _6193.CylindricalPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def datum_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6194.DatumHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6194,
        )

        return self.__parent__._cast(_6194.DatumHarmonicAnalysisOfSingleExcitation)

    @property
    def external_cad_model_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6195.ExternalCADModelHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6195,
        )

        return self.__parent__._cast(
            _6195.ExternalCADModelHarmonicAnalysisOfSingleExcitation
        )

    @property
    def face_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6196.FaceGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6196,
        )

        return self.__parent__._cast(_6196.FaceGearHarmonicAnalysisOfSingleExcitation)

    @property
    def fe_part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6199.FEPartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6199,
        )

        return self.__parent__._cast(_6199.FEPartHarmonicAnalysisOfSingleExcitation)

    @property
    def gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6201.GearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6201,
        )

        return self.__parent__._cast(_6201.GearHarmonicAnalysisOfSingleExcitation)

    @property
    def guide_dxf_model_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6204.GuideDxfModelHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6204,
        )

        return self.__parent__._cast(
            _6204.GuideDxfModelHarmonicAnalysisOfSingleExcitation
        )

    @property
    def hypoid_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6206.HypoidGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6206,
        )

        return self.__parent__._cast(_6206.HypoidGearHarmonicAnalysisOfSingleExcitation)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6210.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6210,
        )

        return self.__parent__._cast(
            _6210.KlingelnbergCycloPalloidConicalGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6213.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6213,
        )

        return self.__parent__._cast(
            _6213.KlingelnbergCycloPalloidHypoidGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6216.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6216,
        )

        return self.__parent__._cast(
            _6216.KlingelnbergCycloPalloidSpiralBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def mass_disc_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6219.MassDiscHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6219,
        )

        return self.__parent__._cast(_6219.MassDiscHarmonicAnalysisOfSingleExcitation)

    @property
    def measurement_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6220.MeasurementComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6220,
        )

        return self.__parent__._cast(
            _6220.MeasurementComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def microphone_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6222.MicrophoneHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6222,
        )

        return self.__parent__._cast(_6222.MicrophoneHarmonicAnalysisOfSingleExcitation)

    @property
    def mountable_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6224.MountableComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6224,
        )

        return self.__parent__._cast(
            _6224.MountableComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def oil_seal_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6225.OilSealHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6225,
        )

        return self.__parent__._cast(_6225.OilSealHarmonicAnalysisOfSingleExcitation)

    @property
    def part_to_part_shear_coupling_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6228.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6228,
        )

        return self.__parent__._cast(
            _6228.PartToPartShearCouplingHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def planet_carrier_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6232.PlanetCarrierHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6232,
        )

        return self.__parent__._cast(
            _6232.PlanetCarrierHarmonicAnalysisOfSingleExcitation
        )

    @property
    def point_load_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6233.PointLoadHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6233,
        )

        return self.__parent__._cast(_6233.PointLoadHarmonicAnalysisOfSingleExcitation)

    @property
    def power_load_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6234.PowerLoadHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6234,
        )

        return self.__parent__._cast(_6234.PowerLoadHarmonicAnalysisOfSingleExcitation)

    @property
    def pulley_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6235.PulleyHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6235,
        )

        return self.__parent__._cast(_6235.PulleyHarmonicAnalysisOfSingleExcitation)

    @property
    def ring_pins_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6236.RingPinsHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6236,
        )

        return self.__parent__._cast(_6236.RingPinsHarmonicAnalysisOfSingleExcitation)

    @property
    def rolling_ring_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6240.RollingRingHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6240,
        )

        return self.__parent__._cast(
            _6240.RollingRingHarmonicAnalysisOfSingleExcitation
        )

    @property
    def shaft_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6242.ShaftHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6242,
        )

        return self.__parent__._cast(_6242.ShaftHarmonicAnalysisOfSingleExcitation)

    @property
    def shaft_hub_connection_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6243.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6243,
        )

        return self.__parent__._cast(
            _6243.ShaftHubConnectionHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spiral_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6246.SpiralBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6246,
        )

        return self.__parent__._cast(
            _6246.SpiralBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def spring_damper_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6250.SpringDamperHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6250,
        )

        return self.__parent__._cast(
            _6250.SpringDamperHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_diff_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6252.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6252,
        )

        return self.__parent__._cast(
            _6252.StraightBevelDiffGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6255.StraightBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6255,
        )

        return self.__parent__._cast(
            _6255.StraightBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_planet_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6258.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6258,
        )

        return self.__parent__._cast(
            _6258.StraightBevelPlanetGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def straight_bevel_sun_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6259.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6259,
        )

        return self.__parent__._cast(
            _6259.StraightBevelSunGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_half_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6260.SynchroniserHalfHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6260,
        )

        return self.__parent__._cast(
            _6260.SynchroniserHalfHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_part_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6262.SynchroniserPartHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6262,
        )

        return self.__parent__._cast(
            _6262.SynchroniserPartHarmonicAnalysisOfSingleExcitation
        )

    @property
    def synchroniser_sleeve_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6263.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6263,
        )

        return self.__parent__._cast(
            _6263.SynchroniserSleeveHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_pump_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6266.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6266,
        )

        return self.__parent__._cast(
            _6266.TorqueConverterPumpHarmonicAnalysisOfSingleExcitation
        )

    @property
    def torque_converter_turbine_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6267.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6267,
        )

        return self.__parent__._cast(
            _6267.TorqueConverterTurbineHarmonicAnalysisOfSingleExcitation
        )

    @property
    def unbalanced_mass_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6268.UnbalancedMassHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6268,
        )

        return self.__parent__._cast(
            _6268.UnbalancedMassHarmonicAnalysisOfSingleExcitation
        )

    @property
    def virtual_component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6269.VirtualComponentHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6269,
        )

        return self.__parent__._cast(
            _6269.VirtualComponentHarmonicAnalysisOfSingleExcitation
        )

    @property
    def worm_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6270.WormGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6270,
        )

        return self.__parent__._cast(_6270.WormGearHarmonicAnalysisOfSingleExcitation)

    @property
    def zerol_bevel_gear_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6273.ZerolBevelGearHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6273,
        )

        return self.__parent__._cast(
            _6273.ZerolBevelGearHarmonicAnalysisOfSingleExcitation
        )

    @property
    def component_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "ComponentHarmonicAnalysisOfSingleExcitation":
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
class ComponentHarmonicAnalysisOfSingleExcitation(
    _6226.PartHarmonicAnalysisOfSingleExcitation
):
    """ComponentHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_ComponentHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_ComponentHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_ComponentHarmonicAnalysisOfSingleExcitation(self)
