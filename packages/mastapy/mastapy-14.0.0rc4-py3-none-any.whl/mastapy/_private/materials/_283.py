"""MaterialDatabase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.databases import _1881

_MATERIAL_DATABASE = python_net_import("SMT.MastaAPI.Materials", "MaterialDatabase")

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.cycloidal import _1505, _1512
    from mastapy._private.electric_machines import _1331, _1349, _1362
    from mastapy._private.gears.materials import _598, _600, _604, _605, _607, _608
    from mastapy._private.materials import _282
    from mastapy._private.shafts import _25
    from mastapy._private.utility.databases import _1877, _1884

    Self = TypeVar("Self", bound="MaterialDatabase")
    CastSelf = TypeVar("CastSelf", bound="MaterialDatabase._Cast_MaterialDatabase")

T = TypeVar("T", bound="_282.Material")

__docformat__ = "restructuredtext en"
__all__ = ("MaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MaterialDatabase:
    """Special nested class for casting MaterialDatabase to subclasses."""

    __parent__: "MaterialDatabase"

    @property
    def named_database(self: "CastSelf") -> "_1881.NamedDatabase":
        return self.__parent__._cast(_1881.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_1884.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _1884

        return self.__parent__._cast(_1884.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_1877.Database":
        pass

        from mastapy._private.utility.databases import _1877

        return self.__parent__._cast(_1877.Database)

    @property
    def shaft_material_database(self: "CastSelf") -> "_25.ShaftMaterialDatabase":
        from mastapy._private.shafts import _25

        return self.__parent__._cast(_25.ShaftMaterialDatabase)

    @property
    def bevel_gear_abstract_material_database(
        self: "CastSelf",
    ) -> "_598.BevelGearAbstractMaterialDatabase":
        from mastapy._private.gears.materials import _598

        return self.__parent__._cast(_598.BevelGearAbstractMaterialDatabase)

    @property
    def bevel_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_600.BevelGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _600

        return self.__parent__._cast(_600.BevelGearISOMaterialDatabase)

    @property
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_604.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _604

        return self.__parent__._cast(_604.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_605.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _605

        return self.__parent__._cast(_605.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "_607.CylindricalGearMaterialDatabase":
        from mastapy._private.gears.materials import _607

        return self.__parent__._cast(_607.CylindricalGearMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_608.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _608

        return self.__parent__._cast(_608.CylindricalGearPlasticMaterialDatabase)

    @property
    def magnet_material_database(self: "CastSelf") -> "_1331.MagnetMaterialDatabase":
        from mastapy._private.electric_machines import _1331

        return self.__parent__._cast(_1331.MagnetMaterialDatabase)

    @property
    def stator_rotor_material_database(
        self: "CastSelf",
    ) -> "_1349.StatorRotorMaterialDatabase":
        from mastapy._private.electric_machines import _1349

        return self.__parent__._cast(_1349.StatorRotorMaterialDatabase)

    @property
    def winding_material_database(self: "CastSelf") -> "_1362.WindingMaterialDatabase":
        from mastapy._private.electric_machines import _1362

        return self.__parent__._cast(_1362.WindingMaterialDatabase)

    @property
    def cycloidal_disc_material_database(
        self: "CastSelf",
    ) -> "_1505.CycloidalDiscMaterialDatabase":
        from mastapy._private.cycloidal import _1505

        return self.__parent__._cast(_1505.CycloidalDiscMaterialDatabase)

    @property
    def ring_pins_material_database(
        self: "CastSelf",
    ) -> "_1512.RingPinsMaterialDatabase":
        from mastapy._private.cycloidal import _1512

        return self.__parent__._cast(_1512.RingPinsMaterialDatabase)

    @property
    def material_database(self: "CastSelf") -> "MaterialDatabase":
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
class MaterialDatabase(_1881.NamedDatabase[T]):
    """MaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_MaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_MaterialDatabase
        """
        return _Cast_MaterialDatabase(self)
