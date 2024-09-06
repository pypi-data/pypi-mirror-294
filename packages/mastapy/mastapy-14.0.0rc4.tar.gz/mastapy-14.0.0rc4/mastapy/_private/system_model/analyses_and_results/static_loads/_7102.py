"""SpecialisedAssemblyLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _6954

_SPECIALISED_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "SpecialisedAssemblyLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2735, _2737, _2741
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6963,
        _6969,
        _6972,
        _6977,
        _6978,
        _6982,
        _6988,
        _6991,
        _6996,
        _7001,
        _7003,
        _7005,
        _7013,
        _7034,
        _7036,
        _7043,
        _7055,
        _7062,
        _7065,
        _7068,
        _7072,
        _7078,
        _7081,
        _7083,
        _7095,
        _7105,
        _7108,
        _7111,
        _7114,
        _7118,
        _7123,
        _7134,
        _7137,
    )
    from mastapy._private.system_model.part_model import _2533

    Self = TypeVar("Self", bound="SpecialisedAssemblyLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyLoadCase._Cast_SpecialisedAssemblyLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyLoadCase:
    """Special nested class for casting SpecialisedAssemblyLoadCase to subclasses."""

    __parent__: "SpecialisedAssemblyLoadCase"

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6954.AbstractAssemblyLoadCase":
        return self.__parent__._cast(_6954.AbstractAssemblyLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7078.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7078,
        )

        return self.__parent__._cast(_7078.PartLoadCase)

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
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6963.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6963,
        )

        return self.__parent__._cast(_6963.AGMAGleasonConicalGearSetLoadCase)

    @property
    def belt_drive_load_case(self: "CastSelf") -> "_6969.BeltDriveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6969,
        )

        return self.__parent__._cast(_6969.BeltDriveLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6972.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6972,
        )

        return self.__parent__._cast(_6972.BevelDifferentialGearSetLoadCase)

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
    def clutch_load_case(self: "CastSelf") -> "_6982.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6982,
        )

        return self.__parent__._cast(_6982.ClutchLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_6988.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6988,
        )

        return self.__parent__._cast(_6988.ConceptCouplingLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_6991.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6991,
        )

        return self.__parent__._cast(_6991.ConceptGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_6996.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6996,
        )

        return self.__parent__._cast(_6996.ConicalGearSetLoadCase)

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
    def cycloidal_assembly_load_case(
        self: "CastSelf",
    ) -> "_7005.CycloidalAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7005,
        )

        return self.__parent__._cast(_7005.CycloidalAssemblyLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7013.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7013,
        )

        return self.__parent__._cast(_7013.CylindricalGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7034.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7034,
        )

        return self.__parent__._cast(_7034.FaceGearSetLoadCase)

    @property
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "_7036.FlexiblePinAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7036,
        )

        return self.__parent__._cast(_7036.FlexiblePinAssemblyLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7043.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7043,
        )

        return self.__parent__._cast(_7043.GearSetLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7055.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7055,
        )

        return self.__parent__._cast(_7055.HypoidGearSetLoadCase)

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
    def microphone_array_load_case(self: "CastSelf") -> "_7072.MicrophoneArrayLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7072,
        )

        return self.__parent__._cast(_7072.MicrophoneArrayLoadCase)

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
    def rolling_ring_assembly_load_case(
        self: "CastSelf",
    ) -> "_7095.RollingRingAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7095,
        )

        return self.__parent__._cast(_7095.RollingRingAssemblyLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7105.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7105,
        )

        return self.__parent__._cast(_7105.SpiralBevelGearSetLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7108.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7108,
        )

        return self.__parent__._cast(_7108.SpringDamperLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7111.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7111,
        )

        return self.__parent__._cast(_7111.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7114.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7114,
        )

        return self.__parent__._cast(_7114.StraightBevelGearSetLoadCase)

    @property
    def synchroniser_load_case(self: "CastSelf") -> "_7118.SynchroniserLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7118,
        )

        return self.__parent__._cast(_7118.SynchroniserLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7123.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7123,
        )

        return self.__parent__._cast(_7123.TorqueConverterLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7134.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7134,
        )

        return self.__parent__._cast(_7134.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7137.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7137,
        )

        return self.__parent__._cast(_7137.ZerolBevelGearSetLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyLoadCase":
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
class SpecialisedAssemblyLoadCase(_6954.AbstractAssemblyLoadCase):
    """SpecialisedAssemblyLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2533.SpecialisedAssembly":
        """mastapy.system_model.part_model.SpecialisedAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssemblyLoadCase":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyLoadCase
        """
        return _Cast_SpecialisedAssemblyLoadCase(self)
