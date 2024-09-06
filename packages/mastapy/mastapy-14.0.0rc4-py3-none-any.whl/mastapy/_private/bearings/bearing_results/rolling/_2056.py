"""LoadedBallBearingResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2087

_LOADED_BALL_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedBallBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _1928
    from mastapy._private.bearings.bearing_results import _2003, _2008, _2011
    from mastapy._private.bearings.bearing_results.rolling import (
        _2026,
        _2037,
        _2040,
        _2066,
        _2071,
        _2090,
        _2105,
        _2108,
        _2129,
    )

    Self = TypeVar("Self", bound="LoadedBallBearingResults")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedBallBearingResults._Cast_LoadedBallBearingResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBallBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBallBearingResults:
    """Special nested class for casting LoadedBallBearingResults to subclasses."""

    __parent__: "LoadedBallBearingResults"

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
    def loaded_angular_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2037.LoadedAngularContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2037

        return self.__parent__._cast(_2037.LoadedAngularContactBallBearingResults)

    @property
    def loaded_angular_contact_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2040.LoadedAngularContactThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2040

        return self.__parent__._cast(_2040.LoadedAngularContactThrustBallBearingResults)

    @property
    def loaded_deep_groove_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2066.LoadedDeepGrooveBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2066

        return self.__parent__._cast(_2066.LoadedDeepGrooveBallBearingResults)

    @property
    def loaded_four_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2071.LoadedFourPointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2071

        return self.__parent__._cast(_2071.LoadedFourPointContactBallBearingResults)

    @property
    def loaded_self_aligning_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2090.LoadedSelfAligningBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2090

        return self.__parent__._cast(_2090.LoadedSelfAligningBallBearingResults)

    @property
    def loaded_three_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2105.LoadedThreePointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2105

        return self.__parent__._cast(_2105.LoadedThreePointContactBallBearingResults)

    @property
    def loaded_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2108.LoadedThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2108

        return self.__parent__._cast(_2108.LoadedThrustBallBearingResults)

    @property
    def loaded_ball_bearing_results(self: "CastSelf") -> "LoadedBallBearingResults":
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
class LoadedBallBearingResults(_2087.LoadedRollingBearingResults):
    """LoadedBallBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BALL_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def friction_model_for_gyroscopic_moment(
        self: "Self",
    ) -> "_2026.FrictionModelForGyroscopicMoment":
        """mastapy.bearings.bearing_results.rolling.FrictionModelForGyroscopicMoment

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionModelForGyroscopicMoment")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingResults.Rolling.FrictionModelForGyroscopicMoment",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results.rolling._2026",
            "FrictionModelForGyroscopicMoment",
        )(value)

    @property
    def smearing_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmearingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def use_element_contact_angles_for_angular_velocities(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UseElementContactAnglesForAngularVelocities"
        )

        if temp is None:
            return False

        return temp

    @property
    def track_truncation(self: "Self") -> "_2129.TrackTruncationSafetyFactorResults":
        """mastapy.bearings.bearing_results.rolling.TrackTruncationSafetyFactorResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TrackTruncation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedBallBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedBallBearingResults
        """
        return _Cast_LoadedBallBearingResults(self)
