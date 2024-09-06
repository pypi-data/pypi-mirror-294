"""OptimizationStrategy"""

from __future__ import annotations

from typing import ClassVar, Generic, TYPE_CHECKING, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.optimization import _2289

_OPTIMIZATION_STRATEGY = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization", "OptimizationStrategy"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.system_model.optimization import _2280, _2283, _2287
    from mastapy._private.utility.databases import _1882

    Self = TypeVar("Self", bound="OptimizationStrategy")
    CastSelf = TypeVar(
        "CastSelf", bound="OptimizationStrategy._Cast_OptimizationStrategy"
    )

TStep = TypeVar("TStep", bound="_2287.OptimizationStep")

__docformat__ = "restructuredtext en"
__all__ = ("OptimizationStrategy",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimizationStrategy:
    """Special nested class for casting OptimizationStrategy to subclasses."""

    __parent__: "OptimizationStrategy"

    @property
    def optimization_strategy_base(
        self: "CastSelf",
    ) -> "_2289.OptimizationStrategyBase":
        return self.__parent__._cast(_2289.OptimizationStrategyBase)

    @property
    def named_database_item(self: "CastSelf") -> "_1882.NamedDatabaseItem":
        from mastapy._private.utility.databases import _1882

        return self.__parent__._cast(_1882.NamedDatabaseItem)

    @property
    def conical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2280.ConicalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2280

        return self.__parent__._cast(_2280.ConicalGearOptimisationStrategy)

    @property
    def cylindrical_gear_optimisation_strategy(
        self: "CastSelf",
    ) -> "_2283.CylindricalGearOptimisationStrategy":
        from mastapy._private.system_model.optimization import _2283

        return self.__parent__._cast(_2283.CylindricalGearOptimisationStrategy)

    @property
    def optimization_strategy(self: "CastSelf") -> "OptimizationStrategy":
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
class OptimizationStrategy(_2289.OptimizationStrategyBase, Generic[TStep]):
    """OptimizationStrategy

    This is a mastapy class.

    Generic Types:
        TStep
    """

    TYPE: ClassVar["Type"] = _OPTIMIZATION_STRATEGY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_OptimizationStrategy":
        """Cast to another type.

        Returns:
            _Cast_OptimizationStrategy
        """
        return _Cast_OptimizationStrategy(self)
