"""LoadedElement"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_LOADED_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedElement"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _1998
    from mastapy._private.bearings.bearing_results.rolling import (
        _2027,
        _2036,
        _2039,
        _2042,
        _2047,
        _2050,
        _2054,
        _2058,
        _2062,
        _2065,
        _2069,
        _2073,
        _2074,
        _2081,
        _2082,
        _2089,
        _2092,
        _2093,
        _2099,
        _2101,
        _2104,
        _2107,
        _2110,
        _2127,
    )

    Self = TypeVar("Self", bound="LoadedElement")
    CastSelf = TypeVar("CastSelf", bound="LoadedElement._Cast_LoadedElement")


__docformat__ = "restructuredtext en"
__all__ = ("LoadedElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedElement:
    """Special nested class for casting LoadedElement to subclasses."""

    __parent__: "LoadedElement"

    @property
    def loaded_angular_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2036.LoadedAngularContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2036

        return self.__parent__._cast(_2036.LoadedAngularContactBallBearingElement)

    @property
    def loaded_angular_contact_thrust_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2039.LoadedAngularContactThrustBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2039

        return self.__parent__._cast(_2039.LoadedAngularContactThrustBallBearingElement)

    @property
    def loaded_asymmetric_spherical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2042.LoadedAsymmetricSphericalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2042

        return self.__parent__._cast(
            _2042.LoadedAsymmetricSphericalRollerBearingElement
        )

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2047.LoadedAxialThrustCylindricalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2047

        return self.__parent__._cast(
            _2047.LoadedAxialThrustCylindricalRollerBearingElement
        )

    @property
    def loaded_axial_thrust_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2050.LoadedAxialThrustNeedleRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2050

        return self.__parent__._cast(_2050.LoadedAxialThrustNeedleRollerBearingElement)

    @property
    def loaded_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2054.LoadedBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2054

        return self.__parent__._cast(_2054.LoadedBallBearingElement)

    @property
    def loaded_crossed_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2058.LoadedCrossedRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2058

        return self.__parent__._cast(_2058.LoadedCrossedRollerBearingElement)

    @property
    def loaded_cylindrical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2062.LoadedCylindricalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2062

        return self.__parent__._cast(_2062.LoadedCylindricalRollerBearingElement)

    @property
    def loaded_deep_groove_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2065.LoadedDeepGrooveBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2065

        return self.__parent__._cast(_2065.LoadedDeepGrooveBallBearingElement)

    @property
    def loaded_four_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2069.LoadedFourPointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2069

        return self.__parent__._cast(_2069.LoadedFourPointContactBallBearingElement)

    @property
    def loaded_multi_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2073.LoadedMultiPointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2073

        return self.__parent__._cast(_2073.LoadedMultiPointContactBallBearingElement)

    @property
    def loaded_needle_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2074.LoadedNeedleRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2074

        return self.__parent__._cast(_2074.LoadedNeedleRollerBearingElement)

    @property
    def loaded_non_barrel_roller_element(
        self: "CastSelf",
    ) -> "_2081.LoadedNonBarrelRollerElement":
        from mastapy._private.bearings.bearing_results.rolling import _2081

        return self.__parent__._cast(_2081.LoadedNonBarrelRollerElement)

    @property
    def loaded_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2082.LoadedRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2082

        return self.__parent__._cast(_2082.LoadedRollerBearingElement)

    @property
    def loaded_self_aligning_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2089.LoadedSelfAligningBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2089

        return self.__parent__._cast(_2089.LoadedSelfAligningBallBearingElement)

    @property
    def loaded_spherical_radial_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2092.LoadedSphericalRadialRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2092

        return self.__parent__._cast(_2092.LoadedSphericalRadialRollerBearingElement)

    @property
    def loaded_spherical_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2093.LoadedSphericalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2093

        return self.__parent__._cast(_2093.LoadedSphericalRollerBearingElement)

    @property
    def loaded_spherical_thrust_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2099.LoadedSphericalThrustRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2099

        return self.__parent__._cast(_2099.LoadedSphericalThrustRollerBearingElement)

    @property
    def loaded_taper_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2101.LoadedTaperRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2101

        return self.__parent__._cast(_2101.LoadedTaperRollerBearingElement)

    @property
    def loaded_three_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2104.LoadedThreePointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2104

        return self.__parent__._cast(_2104.LoadedThreePointContactBallBearingElement)

    @property
    def loaded_thrust_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2107.LoadedThrustBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2107

        return self.__parent__._cast(_2107.LoadedThrustBallBearingElement)

    @property
    def loaded_toroidal_roller_bearing_element(
        self: "CastSelf",
    ) -> "_2110.LoadedToroidalRollerBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2110

        return self.__parent__._cast(_2110.LoadedToroidalRollerBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "LoadedElement":
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
class LoadedElement(_0.APIBase):
    """LoadedElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return temp

    @property
    def axial_loading(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialLoading")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementId")

        if temp is None:
            return ""

        return temp

    @property
    def element_raceway_contact_area_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRacewayContactAreaInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_raceway_contact_area_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRacewayContactAreaLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_raceway_contact_area_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRacewayContactAreaOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_raceway_contact_area_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRacewayContactAreaRight")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_lubricating_film_thickness_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_lubricating_film_thickness_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def normal_load_inner(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalLoadInner")

        if temp is None:
            return 0.0

        return temp

    @normal_load_inner.setter
    @enforce_parameter_types
    def normal_load_inner(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NormalLoadInner", float(value) if value is not None else 0.0
        )

    @property
    def normal_load_outer(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalLoadOuter")

        if temp is None:
            return 0.0

        return temp

    @normal_load_outer.setter
    @enforce_parameter_types
    def normal_load_outer(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NormalLoadOuter", float(value) if value is not None else 0.0
        )

    @property
    def race_deflection_inner(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RaceDeflectionInner")

        if temp is None:
            return 0.0

        return temp

    @race_deflection_inner.setter
    @enforce_parameter_types
    def race_deflection_inner(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RaceDeflectionInner",
            float(value) if value is not None else 0.0,
        )

    @property
    def race_deflection_outer(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RaceDeflectionOuter")

        if temp is None:
            return 0.0

        return temp

    @race_deflection_outer.setter
    @enforce_parameter_types
    def race_deflection_outer(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RaceDeflectionOuter",
            float(value) if value is not None else 0.0,
        )

    @property
    def race_deflection_total(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RaceDeflectionTotal")

        if temp is None:
            return 0.0

        return temp

    @race_deflection_total.setter
    @enforce_parameter_types
    def race_deflection_total(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RaceDeflectionTotal",
            float(value) if value is not None else 0.0,
        )

    @property
    def race_separation_at_element_axial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceSeparationAtElementAxial")

        if temp is None:
            return 0.0

        return temp

    @property
    def race_separation_at_element_radial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceSeparationAtElementRadial")

        if temp is None:
            return 0.0

        return temp

    @property
    def force_from_inner_race(self: "Self") -> "_1998.ElementForce":
        """mastapy.bearings.bearing_results.ElementForce

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceFromInnerRace")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def operating_internal_clearance(self: "Self") -> "_2027.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingInternalClearance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def subsurface_shear_stress_distribution_inner(
        self: "Self",
    ) -> "List[_2127.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceShearStressDistributionInner"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def subsurface_shear_stress_distribution_outer(
        self: "Self",
    ) -> "List[_2127.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceShearStressDistributionOuter"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def subsurface_von_mises_stress_distribution_inner(
        self: "Self",
    ) -> "List[_2127.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceVonMisesStressDistributionInner"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def subsurface_von_mises_stress_distribution_outer(
        self: "Self",
    ) -> "List[_2127.StressAtPosition]":
        """List[mastapy.bearings.bearing_results.rolling.StressAtPosition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SubsurfaceVonMisesStressDistributionOuter"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: "Self") -> "_Cast_LoadedElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedElement
        """
        return _Cast_LoadedElement(self)
