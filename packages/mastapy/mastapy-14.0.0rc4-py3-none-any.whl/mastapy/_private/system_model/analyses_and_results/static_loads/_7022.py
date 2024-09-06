"""ElectricMachineHarmonicLoadDataFromJMAG"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.static_loads import _7025, _7029

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_JMAG = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ElectricMachineHarmonicLoadDataFromJMAG",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import (
        _1426,
        _1428,
        _1431,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7019

    Self = TypeVar("Self", bound="ElectricMachineHarmonicLoadDataFromJMAG")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineHarmonicLoadDataFromJMAG._Cast_ElectricMachineHarmonicLoadDataFromJMAG",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineHarmonicLoadDataFromJMAG",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineHarmonicLoadDataFromJMAG:
    """Special nested class for casting ElectricMachineHarmonicLoadDataFromJMAG to subclasses."""

    __parent__: "ElectricMachineHarmonicLoadDataFromJMAG"

    @property
    def electric_machine_harmonic_load_data_from_motor_packages(
        self: "CastSelf",
    ) -> "_7025.ElectricMachineHarmonicLoadDataFromMotorPackages":
        return self.__parent__._cast(
            _7025.ElectricMachineHarmonicLoadDataFromMotorPackages
        )

    @property
    def electric_machine_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7019.ElectricMachineHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7019,
        )

        return self.__parent__._cast(_7019.ElectricMachineHarmonicLoadData)

    @property
    def electric_machine_harmonic_load_data_base(
        self: "CastSelf",
    ) -> "_1426.ElectricMachineHarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1426

        return self.__parent__._cast(_1426.ElectricMachineHarmonicLoadDataBase)

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "_1431.SpeedDependentHarmonicLoadData":
        from mastapy._private.electric_machines.harmonic_load_data import _1431

        return self.__parent__._cast(_1431.SpeedDependentHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1428.HarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1428

        return self.__parent__._cast(_1428.HarmonicLoadDataBase)

    @property
    def electric_machine_harmonic_load_data_from_jmag(
        self: "CastSelf",
    ) -> "ElectricMachineHarmonicLoadDataFromJMAG":
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
class ElectricMachineHarmonicLoadDataFromJMAG(
    _7025.ElectricMachineHarmonicLoadDataFromMotorPackages[
        _7029.ElectricMachineHarmonicLoadJMAGImportOptions
    ]
):
    """ElectricMachineHarmonicLoadDataFromJMAG

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA_FROM_JMAG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineHarmonicLoadDataFromJMAG":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineHarmonicLoadDataFromJMAG
        """
        return _Cast_ElectricMachineHarmonicLoadDataFromJMAG(self)
