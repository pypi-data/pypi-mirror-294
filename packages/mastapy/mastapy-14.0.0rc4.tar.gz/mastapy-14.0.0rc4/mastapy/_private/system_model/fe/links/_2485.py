"""RollingRingConnectionFELink"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.fe.links import _2478

_ROLLING_RING_CONNECTION_FE_LINK = python_net_import(
    "SMT.MastaAPI.SystemModel.FE.Links", "RollingRingConnectionFELink"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.fe.links import _2473, _2480

    Self = TypeVar("Self", bound="RollingRingConnectionFELink")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollingRingConnectionFELink._Cast_RollingRingConnectionFELink",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingRingConnectionFELink",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingRingConnectionFELink:
    """Special nested class for casting RollingRingConnectionFELink to subclasses."""

    __parent__: "RollingRingConnectionFELink"

    @property
    def multi_angle_connection_fe_link(
        self: "CastSelf",
    ) -> "_2478.MultiAngleConnectionFELink":
        return self.__parent__._cast(_2478.MultiAngleConnectionFELink)

    @property
    def multi_node_fe_link(self: "CastSelf") -> "_2480.MultiNodeFELink":
        from mastapy._private.system_model.fe.links import _2480

        return self.__parent__._cast(_2480.MultiNodeFELink)

    @property
    def fe_link(self: "CastSelf") -> "_2473.FELink":
        from mastapy._private.system_model.fe.links import _2473

        return self.__parent__._cast(_2473.FELink)

    @property
    def rolling_ring_connection_fe_link(
        self: "CastSelf",
    ) -> "RollingRingConnectionFELink":
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
class RollingRingConnectionFELink(_2478.MultiAngleConnectionFELink):
    """RollingRingConnectionFELink

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_RING_CONNECTION_FE_LINK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RollingRingConnectionFELink":
        """Cast to another type.

        Returns:
            _Cast_RollingRingConnectionFELink
        """
        return _Cast_RollingRingConnectionFELink(self)
