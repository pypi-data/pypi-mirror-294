"""PartLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results import _2741
from mastapy._private.system_model.analyses_and_results.static_loads import _6952, _7045

_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PartLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1428
    from mastapy._private.system_model.analyses_and_results import _2735, _2737
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6953,
        _6954,
        _6955,
        _6956,
        _6961,
        _6963,
        _6966,
        _6967,
        _6969,
        _6970,
        _6972,
        _6973,
        _6974,
        _6975,
        _6977,
        _6978,
        _6979,
        _6981,
        _6982,
        _6985,
        _6987,
        _6988,
        _6989,
        _6991,
        _6992,
        _6996,
        _6998,
        _7000,
        _7001,
        _7003,
        _7004,
        _7005,
        _7007,
        _7009,
        _7013,
        _7014,
        _7017,
        _7031,
        _7032,
        _7034,
        _7035,
        _7036,
        _7038,
        _7043,
        _7044,
        _7053,
        _7055,
        _7060,
        _7062,
        _7063,
        _7065,
        _7066,
        _7068,
        _7069,
        _7070,
        _7072,
        _7073,
        _7074,
        _7076,
        _7080,
        _7081,
        _7083,
        _7085,
        _7088,
        _7089,
        _7090,
        _7093,
        _7095,
        _7097,
        _7098,
        _7099,
        _7100,
        _7102,
        _7103,
        _7105,
        _7107,
        _7108,
        _7109,
        _7111,
        _7112,
        _7114,
        _7115,
        _7116,
        _7117,
        _7118,
        _7119,
        _7120,
        _7123,
        _7124,
        _7125,
        _7130,
        _7131,
        _7132,
        _7134,
        _7135,
        _7137,
    )
    from mastapy._private.system_model.part_model import _2525

    Self = TypeVar("Self", bound="PartLoadCase")
    CastSelf = TypeVar("CastSelf", bound="PartLoadCase._Cast_PartLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("PartLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartLoadCase:
    """Special nested class for casting PartLoadCase to subclasses."""

    __parent__: "PartLoadCase"

    @property
    def part_analysis(self: "CastSelf") -> "_2741.PartAnalysis":
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
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6954.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6954,
        )

        return self.__parent__._cast(_6954.AbstractAssemblyLoadCase)

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "_6955.AbstractShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6955,
        )

        return self.__parent__._cast(_6955.AbstractShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_6956.AbstractShaftOrHousingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6956,
        )

        return self.__parent__._cast(_6956.AbstractShaftOrHousingLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_6961.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6961,
        )

        return self.__parent__._cast(_6961.AGMAGleasonConicalGearLoadCase)

    @property
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6963.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6963,
        )

        return self.__parent__._cast(_6963.AGMAGleasonConicalGearSetLoadCase)

    @property
    def assembly_load_case(self: "CastSelf") -> "_6966.AssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6966,
        )

        return self.__parent__._cast(_6966.AssemblyLoadCase)

    @property
    def bearing_load_case(self: "CastSelf") -> "_6967.BearingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6967,
        )

        return self.__parent__._cast(_6967.BearingLoadCase)

    @property
    def belt_drive_load_case(self: "CastSelf") -> "_6969.BeltDriveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6969,
        )

        return self.__parent__._cast(_6969.BeltDriveLoadCase)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_6970.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6970,
        )

        return self.__parent__._cast(_6970.BevelDifferentialGearLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6972.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6972,
        )

        return self.__parent__._cast(_6972.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_differential_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_6973.BevelDifferentialPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6973,
        )

        return self.__parent__._cast(_6973.BevelDifferentialPlanetGearLoadCase)

    @property
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_6974.BevelDifferentialSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6974,
        )

        return self.__parent__._cast(_6974.BevelDifferentialSunGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_6975.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6975,
        )

        return self.__parent__._cast(_6975.BevelGearLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_6977.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6977,
        )

        return self.__parent__._cast(_6977.BevelGearSetLoadCase)

    @property
    def bolted_joint_load_case(self: "CastSelf") -> "_6978.BoltedJointLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6978,
        )

        return self.__parent__._cast(_6978.BoltedJointLoadCase)

    @property
    def bolt_load_case(self: "CastSelf") -> "_6979.BoltLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6979,
        )

        return self.__parent__._cast(_6979.BoltLoadCase)

    @property
    def clutch_half_load_case(self: "CastSelf") -> "_6981.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6981,
        )

        return self.__parent__._cast(_6981.ClutchHalfLoadCase)

    @property
    def clutch_load_case(self: "CastSelf") -> "_6982.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6982,
        )

        return self.__parent__._cast(_6982.ClutchLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6985.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6985,
        )

        return self.__parent__._cast(_6985.ComponentLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_6987.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6987,
        )

        return self.__parent__._cast(_6987.ConceptCouplingHalfLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_6988.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6988,
        )

        return self.__parent__._cast(_6988.ConceptCouplingLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_6989.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6989,
        )

        return self.__parent__._cast(_6989.ConceptGearLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_6991.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6991,
        )

        return self.__parent__._cast(_6991.ConceptGearSetLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_6992.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6992,
        )

        return self.__parent__._cast(_6992.ConicalGearLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_6996.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6996,
        )

        return self.__parent__._cast(_6996.ConicalGearSetLoadCase)

    @property
    def connector_load_case(self: "CastSelf") -> "_6998.ConnectorLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6998,
        )

        return self.__parent__._cast(_6998.ConnectorLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7000.CouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7000,
        )

        return self.__parent__._cast(_7000.CouplingHalfLoadCase)

    @property
    def coupling_load_case(self: "CastSelf") -> "_7001.CouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7001,
        )

        return self.__parent__._cast(_7001.CouplingLoadCase)

    @property
    def cvt_load_case(self: "CastSelf") -> "_7003.CVTLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7003,
        )

        return self.__parent__._cast(_7003.CVTLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7004.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7004,
        )

        return self.__parent__._cast(_7004.CVTPulleyLoadCase)

    @property
    def cycloidal_assembly_load_case(
        self: "CastSelf",
    ) -> "_7005.CycloidalAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7005,
        )

        return self.__parent__._cast(_7005.CycloidalAssemblyLoadCase)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7007.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7007,
        )

        return self.__parent__._cast(_7007.CycloidalDiscLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_7009.CylindricalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7009,
        )

        return self.__parent__._cast(_7009.CylindricalGearLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7013.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7013,
        )

        return self.__parent__._cast(_7013.CylindricalGearSetLoadCase)

    @property
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7014.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7014,
        )

        return self.__parent__._cast(_7014.CylindricalPlanetGearLoadCase)

    @property
    def datum_load_case(self: "CastSelf") -> "_7017.DatumLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7017,
        )

        return self.__parent__._cast(_7017.DatumLoadCase)

    @property
    def external_cad_model_load_case(
        self: "CastSelf",
    ) -> "_7031.ExternalCADModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7031,
        )

        return self.__parent__._cast(_7031.ExternalCADModelLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_7032.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7032,
        )

        return self.__parent__._cast(_7032.FaceGearLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7034.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7034,
        )

        return self.__parent__._cast(_7034.FaceGearSetLoadCase)

    @property
    def fe_part_load_case(self: "CastSelf") -> "_7035.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7035,
        )

        return self.__parent__._cast(_7035.FEPartLoadCase)

    @property
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "_7036.FlexiblePinAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7036,
        )

        return self.__parent__._cast(_7036.FlexiblePinAssemblyLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7038.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7038,
        )

        return self.__parent__._cast(_7038.GearLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7043.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7043,
        )

        return self.__parent__._cast(_7043.GearSetLoadCase)

    @property
    def guide_dxf_model_load_case(self: "CastSelf") -> "_7044.GuideDxfModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7044,
        )

        return self.__parent__._cast(_7044.GuideDxfModelLoadCase)

    @property
    def hypoid_gear_load_case(self: "CastSelf") -> "_7053.HypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7053,
        )

        return self.__parent__._cast(_7053.HypoidGearLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7055.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7055,
        )

        return self.__parent__._cast(_7055.HypoidGearSetLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7060.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7060,
        )

        return self.__parent__._cast(_7060.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7062.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7062,
        )

        return self.__parent__._cast(
            _7062.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7063.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7063,
        )

        return self.__parent__._cast(_7063.KlingelnbergCycloPalloidHypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7065.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7065,
        )

        return self.__parent__._cast(
            _7065.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7066.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7066,
        )

        return self.__parent__._cast(
            _7066.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7068.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7068,
        )

        return self.__parent__._cast(
            _7068.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        )

    @property
    def mass_disc_load_case(self: "CastSelf") -> "_7069.MassDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7069,
        )

        return self.__parent__._cast(_7069.MassDiscLoadCase)

    @property
    def measurement_component_load_case(
        self: "CastSelf",
    ) -> "_7070.MeasurementComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7070,
        )

        return self.__parent__._cast(_7070.MeasurementComponentLoadCase)

    @property
    def microphone_array_load_case(self: "CastSelf") -> "_7072.MicrophoneArrayLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7072,
        )

        return self.__parent__._cast(_7072.MicrophoneArrayLoadCase)

    @property
    def microphone_load_case(self: "CastSelf") -> "_7073.MicrophoneLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7073,
        )

        return self.__parent__._cast(_7073.MicrophoneLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7074.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7074,
        )

        return self.__parent__._cast(_7074.MountableComponentLoadCase)

    @property
    def oil_seal_load_case(self: "CastSelf") -> "_7076.OilSealLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7076,
        )

        return self.__parent__._cast(_7076.OilSealLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7080.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7080,
        )

        return self.__parent__._cast(_7080.PartToPartShearCouplingHalfLoadCase)

    @property
    def part_to_part_shear_coupling_load_case(
        self: "CastSelf",
    ) -> "_7081.PartToPartShearCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7081,
        )

        return self.__parent__._cast(_7081.PartToPartShearCouplingLoadCase)

    @property
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7083.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PlanetaryGearSetLoadCase)

    @property
    def planet_carrier_load_case(self: "CastSelf") -> "_7085.PlanetCarrierLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7085,
        )

        return self.__parent__._cast(_7085.PlanetCarrierLoadCase)

    @property
    def point_load_load_case(self: "CastSelf") -> "_7088.PointLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7088,
        )

        return self.__parent__._cast(_7088.PointLoadLoadCase)

    @property
    def power_load_load_case(self: "CastSelf") -> "_7089.PowerLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7089,
        )

        return self.__parent__._cast(_7089.PowerLoadLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7090.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7090,
        )

        return self.__parent__._cast(_7090.PulleyLoadCase)

    @property
    def ring_pins_load_case(self: "CastSelf") -> "_7093.RingPinsLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7093,
        )

        return self.__parent__._cast(_7093.RingPinsLoadCase)

    @property
    def rolling_ring_assembly_load_case(
        self: "CastSelf",
    ) -> "_7095.RollingRingAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7095,
        )

        return self.__parent__._cast(_7095.RollingRingAssemblyLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7097.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7097,
        )

        return self.__parent__._cast(_7097.RollingRingLoadCase)

    @property
    def root_assembly_load_case(self: "CastSelf") -> "_7098.RootAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7098,
        )

        return self.__parent__._cast(_7098.RootAssemblyLoadCase)

    @property
    def shaft_hub_connection_load_case(
        self: "CastSelf",
    ) -> "_7099.ShaftHubConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7099,
        )

        return self.__parent__._cast(_7099.ShaftHubConnectionLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7100.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7100,
        )

        return self.__parent__._cast(_7100.ShaftLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7102.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7102,
        )

        return self.__parent__._cast(_7102.SpecialisedAssemblyLoadCase)

    @property
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7103.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7103,
        )

        return self.__parent__._cast(_7103.SpiralBevelGearLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7105.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7105,
        )

        return self.__parent__._cast(_7105.SpiralBevelGearSetLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7107.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7107,
        )

        return self.__parent__._cast(_7107.SpringDamperHalfLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7108.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7108,
        )

        return self.__parent__._cast(_7108.SpringDamperLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7109.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7109,
        )

        return self.__parent__._cast(_7109.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7111.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7111,
        )

        return self.__parent__._cast(_7111.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7112.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7112,
        )

        return self.__parent__._cast(_7112.StraightBevelGearLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7114.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7114,
        )

        return self.__parent__._cast(_7114.StraightBevelGearSetLoadCase)

    @property
    def straight_bevel_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7115.StraightBevelPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7115,
        )

        return self.__parent__._cast(_7115.StraightBevelPlanetGearLoadCase)

    @property
    def straight_bevel_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7116.StraightBevelSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7116,
        )

        return self.__parent__._cast(_7116.StraightBevelSunGearLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7117.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7117,
        )

        return self.__parent__._cast(_7117.SynchroniserHalfLoadCase)

    @property
    def synchroniser_load_case(self: "CastSelf") -> "_7118.SynchroniserLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7118,
        )

        return self.__parent__._cast(_7118.SynchroniserLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7119.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7119,
        )

        return self.__parent__._cast(_7119.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7120.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7120,
        )

        return self.__parent__._cast(_7120.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7123.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7123,
        )

        return self.__parent__._cast(_7123.TorqueConverterLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7124.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7124,
        )

        return self.__parent__._cast(_7124.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7125.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7125,
        )

        return self.__parent__._cast(_7125.TorqueConverterTurbineLoadCase)

    @property
    def unbalanced_mass_load_case(self: "CastSelf") -> "_7130.UnbalancedMassLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7130,
        )

        return self.__parent__._cast(_7130.UnbalancedMassLoadCase)

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7131.VirtualComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7131,
        )

        return self.__parent__._cast(_7131.VirtualComponentLoadCase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_7132.WormGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7132,
        )

        return self.__parent__._cast(_7132.WormGearLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7134.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7134,
        )

        return self.__parent__._cast(_7134.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7135.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7135,
        )

        return self.__parent__._cast(_7135.ZerolBevelGearLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7137.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7137,
        )

        return self.__parent__._cast(_7137.ZerolBevelGearSetLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "PartLoadCase":
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
class PartLoadCase(_2741.PartAnalysis):
    """PartLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def excitation_data_is_up_to_date(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationDataIsUpToDate")

        if temp is None:
            return False

        return temp

    @property
    def harmonic_excitation_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.HarmonicExcitationType]"""
        temp = pythonnet_property_get(self.wrapped, "HarmonicExcitationType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @harmonic_excitation_type.setter
    @enforce_parameter_types
    def harmonic_excitation_type(
        self: "Self", value: "_7045.HarmonicExcitationType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "HarmonicExcitationType", value)

    @property
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp",
        )

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up.setter
    @enforce_parameter_types
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: "Self", value: "_6952.StaticLoadCase"
    ) -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(
            self.wrapped,
            "LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp",
            value,
        )

    @property
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp",
        )

        if temp is None:
            return False

        return temp

    @use_this_load_case_for_advanced_system_deflection_current_load_case_set_up.setter
    @enforce_parameter_types
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp",
            bool(value) if value is not None else False,
        )

    @property
    def component_design(self: "Self") -> "_2525.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def static_load_case(self: "Self") -> "_6952.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def time_series_load_case(self: "Self") -> "_6953.TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def clear_user_specified_excitation_data_for_this_load_case(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ClearUserSpecifiedExcitationDataForThisLoadCase"
        )

    def get_harmonic_load_data_for_import(self: "Self") -> "_1428.HarmonicLoadDataBase":
        """mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataBase"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartLoadCase":
        """Cast to another type.

        Returns:
            _Cast_PartLoadCase
        """
        return _Cast_PartLoadCase(self)
