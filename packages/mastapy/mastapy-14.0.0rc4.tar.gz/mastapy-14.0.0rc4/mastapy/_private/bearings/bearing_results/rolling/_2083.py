"""LoadedRollerBearingResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2087

_LOADED_ROLLER_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedRollerBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1928
    from mastapy._private.bearings.bearing_results import _2003, _2008, _2011
    from mastapy._private.bearings.bearing_results.rolling import (
        _2043,
        _2048,
        _2051,
        _2059,
        _2063,
        _2075,
        _2078,
        _2094,
        _2097,
        _2102,
        _2111,
    )

    Self = TypeVar("Self", bound="LoadedRollerBearingResults")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedRollerBearingResults._Cast_LoadedRollerBearingResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollerBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedRollerBearingResults:
    """Special nested class for casting LoadedRollerBearingResults to subclasses."""

    __parent__: "LoadedRollerBearingResults"

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2087.LoadedRollingBearingResults":
        return self.__parent__._cast(_2087.LoadedRollingBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2008.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2008

        return self.__parent__._cast(_2008.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2011.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2011

        return self.__parent__._cast(_2011.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2003.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2003

        return self.__parent__._cast(_2003.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_1928.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _1928

        return self.__parent__._cast(_1928.BearingLoadCaseResultsLightweight)

    @property
    def loaded_asymmetric_spherical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2043.LoadedAsymmetricSphericalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2043

        return self.__parent__._cast(
            _2043.LoadedAsymmetricSphericalRollerBearingResults
        )

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2048.LoadedAxialThrustCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2048

        return self.__parent__._cast(
            _2048.LoadedAxialThrustCylindricalRollerBearingResults
        )

    @property
    def loaded_axial_thrust_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2051.LoadedAxialThrustNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2051

        return self.__parent__._cast(_2051.LoadedAxialThrustNeedleRollerBearingResults)

    @property
    def loaded_crossed_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2059.LoadedCrossedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2059

        return self.__parent__._cast(_2059.LoadedCrossedRollerBearingResults)

    @property
    def loaded_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2063.LoadedCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2063

        return self.__parent__._cast(_2063.LoadedCylindricalRollerBearingResults)

    @property
    def loaded_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2075.LoadedNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2075

        return self.__parent__._cast(_2075.LoadedNeedleRollerBearingResults)

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2078.LoadedNonBarrelRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2078

        return self.__parent__._cast(_2078.LoadedNonBarrelRollerBearingResults)

    @property
    def loaded_spherical_roller_radial_bearing_results(
        self: "CastSelf",
    ) -> "_2094.LoadedSphericalRollerRadialBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2094

        return self.__parent__._cast(_2094.LoadedSphericalRollerRadialBearingResults)

    @property
    def loaded_spherical_roller_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2097.LoadedSphericalRollerThrustBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2097

        return self.__parent__._cast(_2097.LoadedSphericalRollerThrustBearingResults)

    @property
    def loaded_taper_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2102.LoadedTaperRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2102

        return self.__parent__._cast(_2102.LoadedTaperRollerBearingResults)

    @property
    def loaded_toroidal_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2111.LoadedToroidalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2111

        return self.__parent__._cast(_2111.LoadedToroidalRollerBearingResults)

    @property
    def loaded_roller_bearing_results(self: "CastSelf") -> "LoadedRollerBearingResults":
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
class LoadedRollerBearingResults(_2087.LoadedRollingBearingResults):
    """LoadedRollerBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ROLLER_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def element_angular_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementAngularVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_centrifugal_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementCentrifugalForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_surface_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementSurfaceVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    def hertzian_contact_width_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianContactWidthInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def hertzian_contact_width_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianContactWidthOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_shear_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_shear_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedRollerBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedRollerBearingResults
        """
        return _Cast_LoadedRollerBearingResults(self)
