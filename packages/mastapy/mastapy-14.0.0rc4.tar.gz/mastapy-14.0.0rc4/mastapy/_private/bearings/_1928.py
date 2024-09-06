"""BearingLoadCaseResultsLightweight"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_BEARING_LOAD_CASE_RESULTS_LIGHTWEIGHT = python_net_import(
    "SMT.MastaAPI.Bearings", "BearingLoadCaseResultsLightweight"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings import _1927
    from mastapy._private.bearings.bearing_results import (
        _2003,
        _2005,
        _2006,
        _2007,
        _2008,
        _2009,
        _2011,
    )
    from mastapy._private.bearings.bearing_results.fluid_film import (
        _2173,
        _2174,
        _2175,
        _2176,
        _2178,
        _2181,
        _2182,
    )
    from mastapy._private.bearings.bearing_results.rolling import (
        _2037,
        _2040,
        _2043,
        _2048,
        _2051,
        _2056,
        _2059,
        _2063,
        _2066,
        _2071,
        _2075,
        _2078,
        _2083,
        _2087,
        _2090,
        _2094,
        _2097,
        _2102,
        _2105,
        _2108,
        _2111,
    )

    Self = TypeVar("Self", bound="BearingLoadCaseResultsLightweight")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingLoadCaseResultsLightweight._Cast_BearingLoadCaseResultsLightweight",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingLoadCaseResultsLightweight",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingLoadCaseResultsLightweight:
    """Special nested class for casting BearingLoadCaseResultsLightweight to subclasses."""

    __parent__: "BearingLoadCaseResultsLightweight"

    @property
    def bearing_load_case_results_for_pst(
        self: "CastSelf",
    ) -> "_1927.BearingLoadCaseResultsForPST":
        from mastapy._private.bearings import _1927

        return self.__parent__._cast(_1927.BearingLoadCaseResultsForPST)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2003.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2003

        return self.__parent__._cast(_2003.LoadedBearingResults)

    @property
    def loaded_concept_axial_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2005.LoadedConceptAxialClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2005

        return self.__parent__._cast(_2005.LoadedConceptAxialClearanceBearingResults)

    @property
    def loaded_concept_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2006.LoadedConceptClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2006

        return self.__parent__._cast(_2006.LoadedConceptClearanceBearingResults)

    @property
    def loaded_concept_radial_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2007.LoadedConceptRadialClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2007

        return self.__parent__._cast(_2007.LoadedConceptRadialClearanceBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2008.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2008

        return self.__parent__._cast(_2008.LoadedDetailedBearingResults)

    @property
    def loaded_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2009.LoadedLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2009

        return self.__parent__._cast(_2009.LoadedLinearBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2011.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2011

        return self.__parent__._cast(_2011.LoadedNonLinearBearingResults)

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
    def loaded_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2056.LoadedBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2056

        return self.__parent__._cast(_2056.LoadedBallBearingResults)

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
    def loaded_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2083.LoadedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2083

        return self.__parent__._cast(_2083.LoadedRollerBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2087.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2087

        return self.__parent__._cast(_2087.LoadedRollingBearingResults)

    @property
    def loaded_self_aligning_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2090.LoadedSelfAligningBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2090

        return self.__parent__._cast(_2090.LoadedSelfAligningBallBearingResults)

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
    def loaded_toroidal_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2111.LoadedToroidalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2111

        return self.__parent__._cast(_2111.LoadedToroidalRollerBearingResults)

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2173.LoadedFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2173

        return self.__parent__._cast(_2173.LoadedFluidFilmBearingResults)

    @property
    def loaded_grease_filled_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2174.LoadedGreaseFilledJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2174

        return self.__parent__._cast(_2174.LoadedGreaseFilledJournalBearingResults)

    @property
    def loaded_pad_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2175.LoadedPadFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2175

        return self.__parent__._cast(_2175.LoadedPadFluidFilmBearingResults)

    @property
    def loaded_plain_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2176.LoadedPlainJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2176

        return self.__parent__._cast(_2176.LoadedPlainJournalBearingResults)

    @property
    def loaded_plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2178.LoadedPlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_results.fluid_film import _2178

        return self.__parent__._cast(_2178.LoadedPlainOilFedJournalBearing)

    @property
    def loaded_tilting_pad_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2181.LoadedTiltingPadJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2181

        return self.__parent__._cast(_2181.LoadedTiltingPadJournalBearingResults)

    @property
    def loaded_tilting_pad_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2182.LoadedTiltingPadThrustBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2182

        return self.__parent__._cast(_2182.LoadedTiltingPadThrustBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "BearingLoadCaseResultsLightweight":
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
class BearingLoadCaseResultsLightweight(_0.APIBase):
    """BearingLoadCaseResultsLightweight

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_LOAD_CASE_RESULTS_LIGHTWEIGHT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def relative_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_BearingLoadCaseResultsLightweight":
        """Cast to another type.

        Returns:
            _Cast_BearingLoadCaseResultsLightweight
        """
        return _Cast_BearingLoadCaseResultsLightweight(self)
