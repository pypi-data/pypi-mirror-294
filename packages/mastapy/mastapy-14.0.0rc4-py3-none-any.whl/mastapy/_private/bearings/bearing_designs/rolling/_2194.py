"""BallBearing"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.rolling import _2219

_BALL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "BallBearing"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2184, _2185, _2188
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2189,
        _2190,
        _2195,
        _2204,
        _2208,
        _2213,
        _2220,
        _2226,
        _2227,
    )

    Self = TypeVar("Self", bound="BallBearing")
    CastSelf = TypeVar("CastSelf", bound="BallBearing._Cast_BallBearing")


__docformat__ = "restructuredtext en"
__all__ = ("BallBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BallBearing:
    """Special nested class for casting BallBearing to subclasses."""

    __parent__: "BallBearing"

    @property
    def rolling_bearing(self: "CastSelf") -> "_2219.RollingBearing":
        return self.__parent__._cast(_2219.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2185.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2185

        return self.__parent__._cast(_2185.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2188.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2188

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
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2220.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2220

        return self.__parent__._cast(_2220.SelfAligningBallBearing)

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
    def ball_bearing(self: "CastSelf") -> "BallBearing":
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
class BallBearing(_2219.RollingBearing):
    """BallBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BALL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def contact_radius_at_right_angle_to_rolling_direction_inner(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRadiusAtRightAngleToRollingDirectionInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def contact_radius_at_right_angle_to_rolling_direction_outer(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRadiusAtRightAngleToRollingDirectionOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def curvature_sum_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureSumInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def curvature_sum_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureSumOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def element_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_diameter.setter
    @enforce_parameter_types
    def element_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementDiameter", value)

    @property
    def inner_groove_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerGrooveRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_groove_radius.setter
    @enforce_parameter_types
    def inner_groove_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerGrooveRadius", value)

    @property
    def inner_groove_radius_as_percentage_of_element_diameter(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "InnerGrooveRadiusAsPercentageOfElementDiameter"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_groove_radius_as_percentage_of_element_diameter.setter
    @enforce_parameter_types
    def inner_groove_radius_as_percentage_of_element_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "InnerGrooveRadiusAsPercentageOfElementDiameter", value
        )

    @property
    def inner_left_shoulder_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerLeftShoulderDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_left_shoulder_diameter.setter
    @enforce_parameter_types
    def inner_left_shoulder_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerLeftShoulderDiameter", value)

    @property
    def inner_race_osculation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRaceOsculation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_race_osculation.setter
    @enforce_parameter_types
    def inner_race_osculation(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRaceOsculation", value)

    @property
    def inner_right_shoulder_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRightShoulderDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_right_shoulder_diameter.setter
    @enforce_parameter_types
    def inner_right_shoulder_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRightShoulderDiameter", value)

    @property
    def inner_ring_left_shoulder_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingLeftShoulderHeight")

        if temp is None:
            return 0.0

        return temp

    @inner_ring_left_shoulder_height.setter
    @enforce_parameter_types
    def inner_ring_left_shoulder_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerRingLeftShoulderHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_ring_right_shoulder_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingRightShoulderHeight")

        if temp is None:
            return 0.0

        return temp

    @inner_ring_right_shoulder_height.setter
    @enforce_parameter_types
    def inner_ring_right_shoulder_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerRingRightShoulderHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    def inner_ring_shoulder_chamfer(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingShoulderChamfer")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_shoulder_chamfer.setter
    @enforce_parameter_types
    def inner_ring_shoulder_chamfer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingShoulderChamfer", value)

    @property
    def outer_groove_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterGrooveRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_groove_radius.setter
    @enforce_parameter_types
    def outer_groove_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterGrooveRadius", value)

    @property
    def outer_groove_radius_as_percentage_of_element_diameter(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "OuterGrooveRadiusAsPercentageOfElementDiameter"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_groove_radius_as_percentage_of_element_diameter.setter
    @enforce_parameter_types
    def outer_groove_radius_as_percentage_of_element_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "OuterGrooveRadiusAsPercentageOfElementDiameter", value
        )

    @property
    def outer_left_shoulder_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterLeftShoulderDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_left_shoulder_diameter.setter
    @enforce_parameter_types
    def outer_left_shoulder_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterLeftShoulderDiameter", value)

    @property
    def outer_race_osculation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRaceOsculation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_race_osculation.setter
    @enforce_parameter_types
    def outer_race_osculation(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRaceOsculation", value)

    @property
    def outer_right_shoulder_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRightShoulderDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_right_shoulder_diameter.setter
    @enforce_parameter_types
    def outer_right_shoulder_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRightShoulderDiameter", value)

    @property
    def outer_ring_left_shoulder_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingLeftShoulderHeight")

        if temp is None:
            return 0.0

        return temp

    @outer_ring_left_shoulder_height.setter
    @enforce_parameter_types
    def outer_ring_left_shoulder_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterRingLeftShoulderHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_ring_right_shoulder_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingRightShoulderHeight")

        if temp is None:
            return 0.0

        return temp

    @outer_ring_right_shoulder_height.setter
    @enforce_parameter_types
    def outer_ring_right_shoulder_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterRingRightShoulderHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    def outer_ring_shoulder_chamfer(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingShoulderChamfer")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_shoulder_chamfer.setter
    @enforce_parameter_types
    def outer_ring_shoulder_chamfer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingShoulderChamfer", value)

    @property
    def relative_curvature_difference_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeCurvatureDifferenceInner")

        if temp is None:
            return 0.0

        return temp

    @property
    def relative_curvature_difference_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeCurvatureDifferenceOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    def shoulders(self: "Self") -> "List[_2195.BallBearingShoulderDefinition]":
        """List[mastapy.bearings.bearing_designs.rolling.BallBearingShoulderDefinition]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shoulders")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BallBearing":
        """Cast to another type.

        Returns:
            _Cast_BallBearing
        """
        return _Cast_BallBearing(self)
