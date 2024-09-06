"""BearingConnectionComponent"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import

_BEARING_CONNECTION_COMPONENT = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "BearingConnectionComponent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.tolerances import (
        _1959,
        _1960,
        _1961,
        _1962,
        _1964,
        _1965,
        _1966,
        _1969,
        _1970,
        _1973,
        _1975,
    )

    Self = TypeVar("Self", bound="BearingConnectionComponent")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingConnectionComponent._Cast_BearingConnectionComponent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingConnectionComponent",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BearingConnectionComponent:
    """Special nested class for casting BearingConnectionComponent to subclasses."""

    __parent__: "BearingConnectionComponent"

    @property
    def inner_ring_tolerance(self: "CastSelf") -> "_1959.InnerRingTolerance":
        from mastapy._private.bearings.tolerances import _1959

        return self.__parent__._cast(_1959.InnerRingTolerance)

    @property
    def inner_support_tolerance(self: "CastSelf") -> "_1960.InnerSupportTolerance":
        from mastapy._private.bearings.tolerances import _1960

        return self.__parent__._cast(_1960.InnerSupportTolerance)

    @property
    def interference_detail(self: "CastSelf") -> "_1961.InterferenceDetail":
        from mastapy._private.bearings.tolerances import _1961

        return self.__parent__._cast(_1961.InterferenceDetail)

    @property
    def interference_tolerance(self: "CastSelf") -> "_1962.InterferenceTolerance":
        from mastapy._private.bearings.tolerances import _1962

        return self.__parent__._cast(_1962.InterferenceTolerance)

    @property
    def mounting_sleeve_diameter_detail(
        self: "CastSelf",
    ) -> "_1964.MountingSleeveDiameterDetail":
        from mastapy._private.bearings.tolerances import _1964

        return self.__parent__._cast(_1964.MountingSleeveDiameterDetail)

    @property
    def outer_ring_tolerance(self: "CastSelf") -> "_1965.OuterRingTolerance":
        from mastapy._private.bearings.tolerances import _1965

        return self.__parent__._cast(_1965.OuterRingTolerance)

    @property
    def outer_support_tolerance(self: "CastSelf") -> "_1966.OuterSupportTolerance":
        from mastapy._private.bearings.tolerances import _1966

        return self.__parent__._cast(_1966.OuterSupportTolerance)

    @property
    def ring_detail(self: "CastSelf") -> "_1969.RingDetail":
        from mastapy._private.bearings.tolerances import _1969

        return self.__parent__._cast(_1969.RingDetail)

    @property
    def ring_tolerance(self: "CastSelf") -> "_1970.RingTolerance":
        from mastapy._private.bearings.tolerances import _1970

        return self.__parent__._cast(_1970.RingTolerance)

    @property
    def support_detail(self: "CastSelf") -> "_1973.SupportDetail":
        from mastapy._private.bearings.tolerances import _1973

        return self.__parent__._cast(_1973.SupportDetail)

    @property
    def support_tolerance(self: "CastSelf") -> "_1975.SupportTolerance":
        from mastapy._private.bearings.tolerances import _1975

        return self.__parent__._cast(_1975.SupportTolerance)

    @property
    def bearing_connection_component(self: "CastSelf") -> "BearingConnectionComponent":
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
class BearingConnectionComponent(_0.APIBase):
    """BearingConnectionComponent

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEARING_CONNECTION_COMPONENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BearingConnectionComponent":
        """Cast to another type.

        Returns:
            _Cast_BearingConnectionComponent
        """
        return _Cast_BearingConnectionComponent(self)
