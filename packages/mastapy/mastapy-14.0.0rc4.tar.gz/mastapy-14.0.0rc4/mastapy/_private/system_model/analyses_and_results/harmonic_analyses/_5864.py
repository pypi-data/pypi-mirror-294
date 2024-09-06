"""ElectricMachinePeriodicExcitationDetail"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5925

_ELECTRIC_MACHINE_PERIODIC_EXCITATION_DETAIL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "ElectricMachinePeriodicExcitationDetail",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5810,
        _5865,
        _5866,
        _5867,
        _5868,
        _5869,
        _5870,
        _5871,
        _5872,
        _5873,
        _5874,
        _5875,
    )

    Self = TypeVar("Self", bound="ElectricMachinePeriodicExcitationDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachinePeriodicExcitationDetail._Cast_ElectricMachinePeriodicExcitationDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachinePeriodicExcitationDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachinePeriodicExcitationDetail:
    """Special nested class for casting ElectricMachinePeriodicExcitationDetail to subclasses."""

    __parent__: "ElectricMachinePeriodicExcitationDetail"

    @property
    def periodic_excitation_with_reference_shaft(
        self: "CastSelf",
    ) -> "_5925.PeriodicExcitationWithReferenceShaft":
        return self.__parent__._cast(_5925.PeriodicExcitationWithReferenceShaft)

    @property
    def abstract_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5810.AbstractPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5810,
        )

        return self.__parent__._cast(_5810.AbstractPeriodicExcitationDetail)

    @property
    def electric_machine_rotor_x_force_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5865.ElectricMachineRotorXForcePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5865,
        )

        return self.__parent__._cast(
            _5865.ElectricMachineRotorXForcePeriodicExcitationDetail
        )

    @property
    def electric_machine_rotor_x_moment_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5866.ElectricMachineRotorXMomentPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5866,
        )

        return self.__parent__._cast(
            _5866.ElectricMachineRotorXMomentPeriodicExcitationDetail
        )

    @property
    def electric_machine_rotor_y_force_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5867.ElectricMachineRotorYForcePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5867,
        )

        return self.__parent__._cast(
            _5867.ElectricMachineRotorYForcePeriodicExcitationDetail
        )

    @property
    def electric_machine_rotor_y_moment_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5868.ElectricMachineRotorYMomentPeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5868,
        )

        return self.__parent__._cast(
            _5868.ElectricMachineRotorYMomentPeriodicExcitationDetail
        )

    @property
    def electric_machine_rotor_z_force_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5869.ElectricMachineRotorZForcePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5869,
        )

        return self.__parent__._cast(
            _5869.ElectricMachineRotorZForcePeriodicExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_axial_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_5870.ElectricMachineStatorToothAxialLoadsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5870,
        )

        return self.__parent__._cast(
            _5870.ElectricMachineStatorToothAxialLoadsExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_5871.ElectricMachineStatorToothLoadsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5871,
        )

        return self.__parent__._cast(
            _5871.ElectricMachineStatorToothLoadsExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_moments_excitation_detail(
        self: "CastSelf",
    ) -> "_5872.ElectricMachineStatorToothMomentsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5872,
        )

        return self.__parent__._cast(
            _5872.ElectricMachineStatorToothMomentsExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_radial_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_5873.ElectricMachineStatorToothRadialLoadsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5873,
        )

        return self.__parent__._cast(
            _5873.ElectricMachineStatorToothRadialLoadsExcitationDetail
        )

    @property
    def electric_machine_stator_tooth_tangential_loads_excitation_detail(
        self: "CastSelf",
    ) -> "_5874.ElectricMachineStatorToothTangentialLoadsExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5874,
        )

        return self.__parent__._cast(
            _5874.ElectricMachineStatorToothTangentialLoadsExcitationDetail
        )

    @property
    def electric_machine_torque_ripple_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "_5875.ElectricMachineTorqueRipplePeriodicExcitationDetail":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5875,
        )

        return self.__parent__._cast(
            _5875.ElectricMachineTorqueRipplePeriodicExcitationDetail
        )

    @property
    def electric_machine_periodic_excitation_detail(
        self: "CastSelf",
    ) -> "ElectricMachinePeriodicExcitationDetail":
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
class ElectricMachinePeriodicExcitationDetail(
    _5925.PeriodicExcitationWithReferenceShaft
):
    """ElectricMachinePeriodicExcitationDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_PERIODIC_EXCITATION_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachinePeriodicExcitationDetail":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachinePeriodicExcitationDetail
        """
        return _Cast_ElectricMachinePeriodicExcitationDetail(self)
