"""CustomReportItemContainer"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1814

_CUSTOM_REPORT_ITEM_CONTAINER = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportItemContainer"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1805, _1809, _1818, _1826

    Self = TypeVar("Self", bound="CustomReportItemContainer")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportItemContainer._Cast_CustomReportItemContainer"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportItemContainer",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportItemContainer:
    """Special nested class for casting CustomReportItemContainer to subclasses."""

    __parent__: "CustomReportItemContainer"

    @property
    def custom_report_item(self: "CastSelf") -> "_1814.CustomReportItem":
        return self.__parent__._cast(_1814.CustomReportItem)

    @property
    def custom_report(self: "CastSelf") -> "_1805.CustomReport":
        from mastapy._private.utility.report import _1805

        return self.__parent__._cast(_1805.CustomReport)

    @property
    def custom_report_column(self: "CastSelf") -> "_1809.CustomReportColumn":
        from mastapy._private.utility.report import _1809

        return self.__parent__._cast(_1809.CustomReportColumn)

    @property
    def custom_report_item_container_collection_item(
        self: "CastSelf",
    ) -> "_1818.CustomReportItemContainerCollectionItem":
        from mastapy._private.utility.report import _1818

        return self.__parent__._cast(_1818.CustomReportItemContainerCollectionItem)

    @property
    def custom_report_tab(self: "CastSelf") -> "_1826.CustomReportTab":
        from mastapy._private.utility.report import _1826

        return self.__parent__._cast(_1826.CustomReportTab)

    @property
    def custom_report_item_container(self: "CastSelf") -> "CustomReportItemContainer":
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
class CustomReportItemContainer(_1814.CustomReportItem):
    """CustomReportItemContainer

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_ITEM_CONTAINER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportItemContainer":
        """Cast to another type.

        Returns:
            _Cast_CustomReportItemContainer
        """
        return _Cast_CustomReportItemContainer(self)
