"""PerMachineSettings"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private.utility import _1644

_PER_MACHINE_SETTINGS = python_net_import("SMT.MastaAPI.Utility", "PerMachineSettings")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1952
    from mastapy._private.gears.gear_designs.cylindrical import _1043
    from mastapy._private.gears.ltca.cylindrical import _880
    from mastapy._private.gears.materials import _612
    from mastapy._private.nodal_analysis import _68
    from mastapy._private.nodal_analysis.geometry_modeller_link import _168
    from mastapy._private.system_model.part_model import _2527
    from mastapy._private.utility import _1645, _1646
    from mastapy._private.utility.cad_export import _1885
    from mastapy._private.utility.databases import _1880
    from mastapy._private.utility.scripting import _1790
    from mastapy._private.utility.units_and_measurements import _1656

    Self = TypeVar("Self", bound="PerMachineSettings")
    CastSelf = TypeVar("CastSelf", bound="PerMachineSettings._Cast_PerMachineSettings")


__docformat__ = "restructuredtext en"
__all__ = ("PerMachineSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PerMachineSettings:
    """Special nested class for casting PerMachineSettings to subclasses."""

    __parent__: "PerMachineSettings"

    @property
    def persistent_singleton(self: "CastSelf") -> "_1644.PersistentSingleton":
        return self.__parent__._cast(_1644.PersistentSingleton)

    @property
    def fe_user_settings(self: "CastSelf") -> "_68.FEUserSettings":
        from mastapy._private.nodal_analysis import _68

        return self.__parent__._cast(_68.FEUserSettings)

    @property
    def geometry_modeller_settings(self: "CastSelf") -> "_168.GeometryModellerSettings":
        from mastapy._private.nodal_analysis.geometry_modeller_link import _168

        return self.__parent__._cast(_168.GeometryModellerSettings)

    @property
    def gear_material_expert_system_factor_settings(
        self: "CastSelf",
    ) -> "_612.GearMaterialExpertSystemFactorSettings":
        from mastapy._private.gears.materials import _612

        return self.__parent__._cast(_612.GearMaterialExpertSystemFactorSettings)

    @property
    def cylindrical_gear_fe_settings(
        self: "CastSelf",
    ) -> "_880.CylindricalGearFESettings":
        from mastapy._private.gears.ltca.cylindrical import _880

        return self.__parent__._cast(_880.CylindricalGearFESettings)

    @property
    def cylindrical_gear_defaults(self: "CastSelf") -> "_1043.CylindricalGearDefaults":
        from mastapy._private.gears.gear_designs.cylindrical import _1043

        return self.__parent__._cast(_1043.CylindricalGearDefaults)

    @property
    def program_settings(self: "CastSelf") -> "_1645.ProgramSettings":
        from mastapy._private.utility import _1645

        return self.__parent__._cast(_1645.ProgramSettings)

    @property
    def pushbullet_settings(self: "CastSelf") -> "_1646.PushbulletSettings":
        from mastapy._private.utility import _1646

        return self.__parent__._cast(_1646.PushbulletSettings)

    @property
    def measurement_settings(self: "CastSelf") -> "_1656.MeasurementSettings":
        from mastapy._private.utility.units_and_measurements import _1656

        return self.__parent__._cast(_1656.MeasurementSettings)

    @property
    def scripting_setup(self: "CastSelf") -> "_1790.ScriptingSetup":
        from mastapy._private.utility.scripting import _1790

        return self.__parent__._cast(_1790.ScriptingSetup)

    @property
    def database_settings(self: "CastSelf") -> "_1880.DatabaseSettings":
        from mastapy._private.utility.databases import _1880

        return self.__parent__._cast(_1880.DatabaseSettings)

    @property
    def cad_export_settings(self: "CastSelf") -> "_1885.CADExportSettings":
        from mastapy._private.utility.cad_export import _1885

        return self.__parent__._cast(_1885.CADExportSettings)

    @property
    def skf_settings(self: "CastSelf") -> "_1952.SKFSettings":
        from mastapy._private.bearings import _1952

        return self.__parent__._cast(_1952.SKFSettings)

    @property
    def planet_carrier_settings(self: "CastSelf") -> "_2527.PlanetCarrierSettings":
        from mastapy._private.system_model.part_model import _2527

        return self.__parent__._cast(_2527.PlanetCarrierSettings)

    @property
    def per_machine_settings(self: "CastSelf") -> "PerMachineSettings":
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
class PerMachineSettings(_1644.PersistentSingleton):
    """PerMachineSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PER_MACHINE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    def reset_to_defaults(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ResetToDefaults")

    @property
    def cast_to(self: "Self") -> "_Cast_PerMachineSettings":
        """Cast to another type.

        Returns:
            _Cast_PerMachineSettings
        """
        return _Cast_PerMachineSettings(self)
