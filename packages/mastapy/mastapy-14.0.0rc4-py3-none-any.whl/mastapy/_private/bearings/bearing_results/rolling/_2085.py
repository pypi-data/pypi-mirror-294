"""LoadedRollerStripLoadResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_LOADED_ROLLER_STRIP_LOAD_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedRollerStripLoadResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import (
        _2035,
        _2045,
        _2080,
        _2096,
        _2113,
    )

    Self = TypeVar("Self", bound="LoadedRollerStripLoadResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedRollerStripLoadResults._Cast_LoadedRollerStripLoadResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollerStripLoadResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedRollerStripLoadResults:
    """Special nested class for casting LoadedRollerStripLoadResults to subclasses."""

    __parent__: "LoadedRollerStripLoadResults"

    @property
    def loaded_abstract_spherical_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2035.LoadedAbstractSphericalRollerBearingStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2035

        return self.__parent__._cast(
            _2035.LoadedAbstractSphericalRollerBearingStripLoadResults
        )

    @property
    def loaded_asymmetric_spherical_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2045.LoadedAsymmetricSphericalRollerBearingStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2045

        return self.__parent__._cast(
            _2045.LoadedAsymmetricSphericalRollerBearingStripLoadResults
        )

    @property
    def loaded_non_barrel_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2080.LoadedNonBarrelRollerBearingStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2080

        return self.__parent__._cast(_2080.LoadedNonBarrelRollerBearingStripLoadResults)

    @property
    def loaded_spherical_roller_radial_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2096.LoadedSphericalRollerRadialBearingStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2096

        return self.__parent__._cast(
            _2096.LoadedSphericalRollerRadialBearingStripLoadResults
        )

    @property
    def loaded_toroidal_roller_bearing_strip_load_results(
        self: "CastSelf",
    ) -> "_2113.LoadedToroidalRollerBearingStripLoadResults":
        from mastapy._private.bearings.bearing_results.rolling import _2113

        return self.__parent__._cast(_2113.LoadedToroidalRollerBearingStripLoadResults)

    @property
    def loaded_roller_strip_load_results(
        self: "CastSelf",
    ) -> "LoadedRollerStripLoadResults":
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
class LoadedRollerStripLoadResults(_0.APIBase):
    """LoadedRollerStripLoadResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ROLLER_STRIP_LOAD_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedRollerStripLoadResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedRollerStripLoadResults
        """
        return _Cast_LoadedRollerStripLoadResults(self)
