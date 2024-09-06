"""DetailedBearing"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs import _2188

_DETAILED_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns", "DetailedBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2184
    from mastapy._private.bearings.bearing_designs.fluid_film import (
        _2241,
        _2243,
        _2245,
        _2247,
        _2248,
        _2249,
    )
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2189,
        _2190,
        _2191,
        _2192,
        _2193,
        _2194,
        _2196,
        _2202,
        _2203,
        _2204,
        _2208,
        _2213,
        _2214,
        _2215,
        _2216,
        _2219,
        _2220,
        _2223,
        _2224,
        _2225,
        _2226,
        _2227,
        _2228,
    )

    Self = TypeVar("Self", bound="DetailedBearing")
    CastSelf = TypeVar("CastSelf", bound="DetailedBearing._Cast_DetailedBearing")


__docformat__ = "restructuredtext en"
__all__ = ("DetailedBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DetailedBearing:
    """Special nested class for casting DetailedBearing to subclasses."""

    __parent__: "DetailedBearing"

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2188.NonLinearBearing":
        return self.__parent__._cast(_2188.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2184.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2184

        return self.__parent__._cast(_2184.BearingDesign)

    @property
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2189.AngularContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2189

        return self.__parent__._cast(_2189.AngularContactBallBearing)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2190.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2190

        return self.__parent__._cast(_2190.AngularContactThrustBallBearing)

    @property
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2191.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2191

        return self.__parent__._cast(_2191.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2192.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2192

        return self.__parent__._cast(_2192.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2193.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2193

        return self.__parent__._cast(_2193.AxialThrustNeedleRollerBearing)

    @property
    def ball_bearing(self: "CastSelf") -> "_2194.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2194

        return self.__parent__._cast(_2194.BallBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2196.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2196

        return self.__parent__._cast(_2196.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2202.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2202

        return self.__parent__._cast(_2202.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2203.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2203

        return self.__parent__._cast(_2203.CylindricalRollerBearing)

    @property
    def deep_groove_ball_bearing(self: "CastSelf") -> "_2204.DeepGrooveBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2204

        return self.__parent__._cast(_2204.DeepGrooveBallBearing)

    @property
    def four_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2208.FourPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2208

        return self.__parent__._cast(_2208.FourPointContactBallBearing)

    @property
    def multi_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2213.MultiPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2213

        return self.__parent__._cast(_2213.MultiPointContactBallBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2214.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2214

        return self.__parent__._cast(_2214.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2215.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2215

        return self.__parent__._cast(_2215.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2216.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2216

        return self.__parent__._cast(_2216.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2219.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2219

        return self.__parent__._cast(_2219.RollingBearing)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2220.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2220

        return self.__parent__._cast(_2220.SelfAligningBallBearing)

    @property
    def spherical_roller_bearing(self: "CastSelf") -> "_2223.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2223

        return self.__parent__._cast(_2223.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2224.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2224

        return self.__parent__._cast(_2224.SphericalRollerThrustBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2225.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2225

        return self.__parent__._cast(_2225.TaperRollerBearing)

    @property
    def three_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2226.ThreePointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2226

        return self.__parent__._cast(_2226.ThreePointContactBallBearing)

    @property
    def thrust_ball_bearing(self: "CastSelf") -> "_2227.ThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2227

        return self.__parent__._cast(_2227.ThrustBallBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2228.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2228

        return self.__parent__._cast(_2228.ToroidalRollerBearing)

    @property
    def pad_fluid_film_bearing(self: "CastSelf") -> "_2241.PadFluidFilmBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2241

        return self.__parent__._cast(_2241.PadFluidFilmBearing)

    @property
    def plain_grease_filled_journal_bearing(
        self: "CastSelf",
    ) -> "_2243.PlainGreaseFilledJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2243

        return self.__parent__._cast(_2243.PlainGreaseFilledJournalBearing)

    @property
    def plain_journal_bearing(self: "CastSelf") -> "_2245.PlainJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2245

        return self.__parent__._cast(_2245.PlainJournalBearing)

    @property
    def plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2247.PlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2247

        return self.__parent__._cast(_2247.PlainOilFedJournalBearing)

    @property
    def tilting_pad_journal_bearing(
        self: "CastSelf",
    ) -> "_2248.TiltingPadJournalBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2248

        return self.__parent__._cast(_2248.TiltingPadJournalBearing)

    @property
    def tilting_pad_thrust_bearing(self: "CastSelf") -> "_2249.TiltingPadThrustBearing":
        from mastapy._private.bearings.bearing_designs.fluid_film import _2249

        return self.__parent__._cast(_2249.TiltingPadThrustBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "DetailedBearing":
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
class DetailedBearing(_2188.NonLinearBearing):
    """DetailedBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DETAILED_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_DetailedBearing":
        """Cast to another type.

        Returns:
            _Cast_DetailedBearing
        """
        return _Cast_DetailedBearing(self)
