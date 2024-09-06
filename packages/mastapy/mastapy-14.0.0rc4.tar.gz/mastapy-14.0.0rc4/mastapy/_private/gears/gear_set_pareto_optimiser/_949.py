"""ParetoConicalRatingOptimisationStrategyDatabase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.math_utility.optimisation import _1600

_PARETO_CONICAL_RATING_OPTIMISATION_STRATEGY_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser",
    "ParetoConicalRatingOptimisationStrategyDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _956,
        _957,
        _959,
        _960,
        _961,
        _962,
    )
    from mastapy._private.math_utility.optimisation import _1588
    from mastapy._private.utility.databases import _1877, _1881, _1884

    Self = TypeVar("Self", bound="ParetoConicalRatingOptimisationStrategyDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ParetoConicalRatingOptimisationStrategyDatabase._Cast_ParetoConicalRatingOptimisationStrategyDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParetoConicalRatingOptimisationStrategyDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParetoConicalRatingOptimisationStrategyDatabase:
    """Special nested class for casting ParetoConicalRatingOptimisationStrategyDatabase to subclasses."""

    __parent__: "ParetoConicalRatingOptimisationStrategyDatabase"

    @property
    def pareto_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_1600.ParetoOptimisationStrategyDatabase":
        return self.__parent__._cast(_1600.ParetoOptimisationStrategyDatabase)

    @property
    def design_space_search_strategy_database(
        self: "CastSelf",
    ) -> "_1588.DesignSpaceSearchStrategyDatabase":
        from mastapy._private.math_utility.optimisation import _1588

        return self.__parent__._cast(_1588.DesignSpaceSearchStrategyDatabase)

    @property
    def named_database(self: "CastSelf") -> "_1881.NamedDatabase":
        pass

        from mastapy._private.utility.databases import _1881

        return self.__parent__._cast(_1881.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_1884.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _1884

        return self.__parent__._cast(_1884.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_1877.Database":
        pass

        from mastapy._private.utility.databases import _1877

        return self.__parent__._cast(_1877.Database)

    @property
    def pareto_hypoid_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_956.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _956

        return self.__parent__._cast(
            _956.ParetoHypoidGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_hypoid_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_957.ParetoHypoidGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _957

        return self.__parent__._cast(
            _957.ParetoHypoidGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_959.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _959

        return self.__parent__._cast(
            _959.ParetoSpiralBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_spiral_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_960.ParetoSpiralBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _960

        return self.__parent__._cast(
            _960.ParetoSpiralBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_duty_cycle_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_961.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _961

        return self.__parent__._cast(
            _961.ParetoStraightBevelGearSetDutyCycleOptimisationStrategyDatabase
        )

    @property
    def pareto_straight_bevel_gear_set_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "_962.ParetoStraightBevelGearSetOptimisationStrategyDatabase":
        from mastapy._private.gears.gear_set_pareto_optimiser import _962

        return self.__parent__._cast(
            _962.ParetoStraightBevelGearSetOptimisationStrategyDatabase
        )

    @property
    def pareto_conical_rating_optimisation_strategy_database(
        self: "CastSelf",
    ) -> "ParetoConicalRatingOptimisationStrategyDatabase":
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
class ParetoConicalRatingOptimisationStrategyDatabase(
    _1600.ParetoOptimisationStrategyDatabase
):
    """ParetoConicalRatingOptimisationStrategyDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARETO_CONICAL_RATING_OPTIMISATION_STRATEGY_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ParetoConicalRatingOptimisationStrategyDatabase":
        """Cast to another type.

        Returns:
            _Cast_ParetoConicalRatingOptimisationStrategyDatabase
        """
        return _Cast_ParetoConicalRatingOptimisationStrategyDatabase(self)
