"""LoadedRollingBearingResults"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_results import _2008

_LOADED_ROLLING_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedRollingBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings import _1928, _1937
    from mastapy._private.bearings.bearing_results import _2003, _2011
    from mastapy._private.bearings.bearing_results.rolling import (
        _2023,
        _2027,
        _2032,
        _2034,
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
        _2088,
        _2090,
        _2094,
        _2097,
        _2102,
        _2105,
        _2108,
        _2111,
        _2114,
    )
    from mastapy._private.bearings.bearing_results.rolling.abma import _2171
    from mastapy._private.bearings.bearing_results.rolling.fitting import (
        _2164,
        _2166,
        _2167,
    )
    from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import (
        _2157,
        _2158,
        _2160,
    )
    from mastapy._private.bearings.bearing_results.rolling.skf_module import _2152

    Self = TypeVar("Self", bound="LoadedRollingBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedRollingBearingResults._Cast_LoadedRollingBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedRollingBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedRollingBearingResults:
    """Special nested class for casting LoadedRollingBearingResults to subclasses."""

    __parent__: "LoadedRollingBearingResults"

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2008.LoadedDetailedBearingResults":
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
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "LoadedRollingBearingResults":
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
class LoadedRollingBearingResults(_2008.LoadedDetailedBearingResults):
    """LoadedRollingBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ROLLING_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def axial_to_radial_load_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialToRadialLoadRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    def cage_angular_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CageAngularVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    def change_in_element_diameter_due_to_thermal_expansion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ChangeInElementDiameterDueToThermalExpansion"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def change_in_operating_radial_internal_clearance_due_to_element_thermal_expansion(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ChangeInOperatingRadialInternalClearanceDueToElementThermalExpansion",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def drag_loss_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DragLossFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def dynamic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ElementTemperature")

        if temp is None:
            return 0.0

        return temp

    @element_temperature.setter
    @enforce_parameter_types
    def element_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ElementTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def fluid_film_density(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FluidFilmDensity")

        if temp is None:
            return 0.0

        return temp

    @property
    def fluid_film_temperature_source(
        self: "Self",
    ) -> "_1937.FluidFilmTemperatureOptions":
        """mastapy.bearings.FluidFilmTemperatureOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FluidFilmTemperatureSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.FluidFilmTemperatureOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._1937", "FluidFilmTemperatureOptions"
        )(value)

    @property
    def frequency_of_over_rolling_on_inner_ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOfOverRollingOnInnerRing")

        if temp is None:
            return 0.0

        return temp

    @property
    def frequency_of_over_rolling_on_outer_ring(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOfOverRollingOnOuterRing")

        if temp is None:
            return 0.0

        return temp

    @property
    def frequency_of_over_rolling_on_rolling_element(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FrequencyOfOverRollingOnRollingElement"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def frictional_moment_of_drag_losses(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionalMomentOfDragLosses")

        if temp is None:
            return 0.0

        return temp

    @property
    def frictional_moment_of_seals(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionalMomentOfSeals")

        if temp is None:
            return 0.0

        return temp

    @property
    def include_centrifugal_effects(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeCentrifugalEffects")

        if temp is None:
            return False

        return temp

    @property
    def include_centrifugal_ring_expansion(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeCentrifugalRingExpansion")

        if temp is None:
            return False

        return temp

    @property
    def include_fitting_effects(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeFittingEffects")

        if temp is None:
            return False

        return temp

    @property
    def include_gear_blank_elastic_distortion(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeGearBlankElasticDistortion")

        if temp is None:
            return False

        return temp

    @property
    def include_inner_race_deflections(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeInnerRaceDeflections")

        if temp is None:
            return False

        return temp

    @property
    def include_thermal_expansion_effects(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IncludeThermalExpansionEffects")

        if temp is None:
            return False

        return temp

    @property
    def is_inner_ring_rotating_relative_to_load(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsInnerRingRotatingRelativeToLoad")

        if temp is None:
            return False

        return temp

    @property
    def is_outer_ring_rotating_relative_to_load(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsOuterRingRotatingRelativeToLoad")

        if temp is None:
            return False

        return temp

    @property
    def kinematic_viscosity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KinematicViscosity")

        if temp is None:
            return 0.0

        return temp

    @property
    def kinematic_viscosity_of_oil_for_efficiency_calculations(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KinematicViscosityOfOilForEfficiencyCalculations"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def lambda_ratio_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LambdaRatioInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def lambda_ratio_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LambdaRatioOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def lubricant_film_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LubricantFilmTemperature")

        if temp is None:
            return 0.0

        return temp

    @lubricant_film_temperature.setter
    @enforce_parameter_types
    def lubricant_film_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LubricantFilmTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def lubricant_windage_and_churning_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LubricantWindageAndChurningTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @lubricant_windage_and_churning_temperature.setter
    @enforce_parameter_types
    def lubricant_windage_and_churning_temperature(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LubricantWindageAndChurningTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def maximum_normal_load_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalLoadInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_normal_load_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalLoadOuter")

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
    def maximum_normal_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def maximum_normal_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressOuter")

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
    def number_of_elements_in_contact(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfElementsInContact")

        if temp is None:
            return 0

        return temp

    @property
    def oil_dip_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilDipCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    def ratio_of_operating_element_diameter_to_element_pcd(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RatioOfOperatingElementDiameterToElementPCD"
        )

        if temp is None:
            return 0.0

        return temp

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
    def rolling_frictional_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingFrictionalMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    def sliding_friction_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingFrictionCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    def sliding_frictional_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingFrictionalMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    def speed_factor_dmn(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedFactorDmn")

        if temp is None:
            return 0.0

        return temp

    @property
    def speed_factor_dn(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedFactorDn")

        if temp is None:
            return 0.0

        return temp

    @property
    def static_equivalent_load_capacity_ratio_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StaticEquivalentLoadCapacityRatioLimit"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def surrounding_lubricant_density(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurroundingLubricantDensity")

        if temp is None:
            return 0.0

        return temp

    @property
    def total_element_raceway_contact_area_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalElementRacewayContactAreaInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def total_element_raceway_contact_area_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalElementRacewayContactAreaLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def total_element_raceway_contact_area_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalElementRacewayContactAreaOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def total_element_raceway_contact_area_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalElementRacewayContactAreaRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def total_frictional_moment_from_skf_loss_method(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalFrictionalMomentFromSKFLossMethod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def ansiabma(self: "Self") -> "_2171.ANSIABMAResults":
        """mastapy.bearings.bearing_results.rolling.abma.ANSIABMAResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ANSIABMA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def din7322010(self: "Self") -> "_2023.DIN7322010Results":
        """mastapy.bearings.bearing_results.rolling.DIN7322010Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DIN7322010")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso2812007(self: "Self") -> "_2157.ISO2812007Results":
        """mastapy.bearings.bearing_results.rolling.iso_rating_results.ISO2812007Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO2812007")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def iso762006(self: "Self") -> "_2158.ISO762006Results":
        """mastapy.bearings.bearing_results.rolling.iso_rating_results.ISO762006Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO762006")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def isotr1417912001(self: "Self") -> "_2032.ISOTR1417912001Results":
        """mastapy.bearings.bearing_results.rolling.ISOTR1417912001Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISOTR1417912001")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def isotr1417922001(self: "Self") -> "_2034.ISOTR1417922001Results":
        """mastapy.bearings.bearing_results.rolling.ISOTR1417922001Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISOTR1417922001")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def isots162812008(self: "Self") -> "_2160.ISOTS162812008Results":
        """mastapy.bearings.bearing_results.rolling.iso_rating_results.ISOTS162812008Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISOTS162812008")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_ring_fitting_at_assembly(
        self: "Self",
    ) -> "_2164.InnerRingFittingThermalResults":
        """mastapy.bearings.bearing_results.rolling.fitting.InnerRingFittingThermalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRingFittingAtAssembly")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def inner_ring_fitting_at_operating_conditions(
        self: "Self",
    ) -> "_2164.InnerRingFittingThermalResults":
        """mastapy.bearings.bearing_results.rolling.fitting.InnerRingFittingThermalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InnerRingFittingAtOperatingConditions"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def maximum_operating_internal_clearance(self: "Self") -> "_2027.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumOperatingInternalClearance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def maximum_static_contact_stress(
        self: "Self",
    ) -> "_2114.MaximumStaticContactStress":
        """mastapy.bearings.bearing_results.rolling.MaximumStaticContactStress

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumStaticContactStress")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def minimum_operating_internal_clearance(self: "Self") -> "_2027.InternalClearance":
        """mastapy.bearings.bearing_results.rolling.InternalClearance

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumOperatingInternalClearance")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def outer_ring_fitting_at_assembly(
        self: "Self",
    ) -> "_2166.OuterRingFittingThermalResults":
        """mastapy.bearings.bearing_results.rolling.fitting.OuterRingFittingThermalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRingFittingAtAssembly")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def outer_ring_fitting_at_operating_conditions(
        self: "Self",
    ) -> "_2166.OuterRingFittingThermalResults":
        """mastapy.bearings.bearing_results.rolling.fitting.OuterRingFittingThermalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterRingFittingAtOperatingConditions"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def skf_module_results(self: "Self") -> "_2152.SKFModuleResults":
        """mastapy.bearings.bearing_results.rolling.skf_module.SKFModuleResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFModuleResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def all_mounting_results(self: "Self") -> "List[_2167.RingFittingThermalResults]":
        """List[mastapy.bearings.bearing_results.rolling.fitting.RingFittingThermalResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllMountingResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def rows(self: "Self") -> "List[_2088.LoadedRollingBearingRow]":
        """List[mastapy.bearings.bearing_results.rolling.LoadedRollingBearingRow]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rows")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedRollingBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedRollingBearingResults
        """
        return _Cast_LoadedRollingBearingResults(self)
