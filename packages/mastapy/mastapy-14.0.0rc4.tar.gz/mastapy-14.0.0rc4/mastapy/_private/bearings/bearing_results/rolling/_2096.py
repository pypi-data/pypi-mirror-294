"""LoadedSphericalRollerRadialBearingStripLoadResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2035

_LOADED_SPHERICAL_ROLLER_RADIAL_BEARING_STRIP_LOAD_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedSphericalRollerRadialBearingStripLoadResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2085, _2113

    Self = TypeVar("Self", bound="LoadedSphericalRollerRadialBearingStripLoadResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedSphericalRollerRadialBearingStripLoadResults._Cast_LoadedSphericalRollerRadialBearingStripLoadResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedSphericalRollerRadialBearingStripLoadResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedSphericalRollerRadialBearingStripLoadResults:
    """Special nested class for casting LoadedSphericalRollerRadialBearingStripLoadResults to subclasses."""

    __parent__: "LoadedSphericalRollerRadialBearingStripLoadResults"

    @property
    def loaded_abstract_spherical_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2035.LoadedAbstractSphericalRollerBearingStripLoadResults":
        return self.__parent__._cast(
            _2035.LoadedAbstractSphericalRollerBearingStripLoadResults
        )

    @property
    def loaded_roller_strip_load_results(
        self: "CastSelf",
    ) -> "_2085.LoadedRollerStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2085

        return self.__parent__._cast(_2085.LoadedRollerStripLoadResults)

    @property
    def loaded_toroidal_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2113.LoadedToroidalRollerBearingStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2113

        return self.__parent__._cast(_2113.LoadedToroidalRollerBearingStripLoadResults)

    @property
    def loaded_spherical_roller_radial_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "LoadedSphericalRollerRadialBearingStripLoadResults":
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
class LoadedSphericalRollerRadialBearingStripLoadResults(
    _2035.LoadedAbstractSphericalRollerBearingStripLoadResults
):
    """LoadedSphericalRollerRadialBearingStripLoadResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_SPHERICAL_ROLLER_RADIAL_BEARING_STRIP_LOAD_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_LoadedSphericalRollerRadialBearingStripLoadResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedSphericalRollerRadialBearingStripLoadResults
        """
        return _Cast_LoadedSphericalRollerRadialBearingStripLoadResults(self)
