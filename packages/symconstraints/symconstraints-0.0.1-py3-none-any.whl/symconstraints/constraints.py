"""Tools to create constraints."""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations
from typing import TYPE_CHECKING
from warnings import warn
from dataclasses import dataclass
from functools import reduce

import sympy
from sympy import (
    And,
    Dummy,
    Eq,
    Basic,
    Ge,
    Gt,
    Interval,
    Le,
    Lt,
    Or,
    S,
    Symbol,
    oo,
    simplify_logic,
    solveset,
    FiniteSet,
    Expr,
    Intersection,
    Union,
    ConditionSet,
    roots,
    reduce_inequalities,
    Q,
    ask,
    Pow,
    Poly,
)
from sympy.polys.polyerrors import UnsolvableFactorError
from sympy.logic.boolalg import Boolean

if TYPE_CHECKING:
    from typing import Iterable, Literal

from symconstraints.operation import Imputation, Validation

_assumption_domain = {
    "real": S.Reals,
    "complex": S.Complexes,
    "integer": S.Integers,
    "negative": Interval(-oo, 0),
    "positive": Interval(0, oo),
}


def _get_symbol_domain(symbol):
    result = S.Complexes
    for assumption, is_assumption_true in symbol.assumptions0.items():
        domain = _assumption_domain.get(assumption)
        if domain is not None:
            result = (
                result.intersect(domain)
                if is_assumption_true
                else domain.complement(result)
            )
    return result


class _DummyRelation:
    rel: Literal["<", ">", "=", "!"]
    expr: Basic
    strict: bool

    def __init__(self, relation: Basic, dummy: Dummy):
        relation = reduce_inequalities(relation, dummy)
        self.strict = isinstance(relation, (Lt, Gt))
        if isinstance(relation, Eq):
            self.rel = "="
            self.expr = relation.rhs if relation.lhs == dummy else relation.lhs
        elif isinstance(relation, Ge | Gt | Le | Lt):
            if relation.gts == dummy:
                self.rel = ">"
                self.expr = relation.lts
            else:
                self.rel = "<"
                self.expr = relation.gts

        if self.rel is None:
            raise ValueError(f"Could not analyze relation {relation}")


def _is_even_root(expr: _DummyRelation):
    return isinstance(expr.expr, Pow) and ask(Q.even(1 / expr.expr.args[1]))


def _and_dummy_to_constraints(and_relation: And, dummy: Dummy) -> set[Boolean]:
    constraints: set[Boolean] = set()
    useful_relations = []
    for rel in and_relation.args:
        try:
            useful_relations.append(_DummyRelation(rel, dummy))
        except ValueError as e:
            warn(str(e))

    for relation1, relation2 in combinations(useful_relations, 2):
        strict = relation1.strict or relation2.strict
        match (relation1.rel, relation2.rel):
            case ("=", "="):
                constraints.add(Eq(relation1.expr, relation2.expr))
            case (">" | "=", "<" | "="):
                if ask(Eq(relation1.expr, -relation2.expr)) and (
                    _is_even_root(relation1) or _is_even_root(relation2)
                ):
                    # This is a workaround to a bug where SymPy doesn't recognize the square roots are always nonnegative
                    # in the real domain
                    continue

                constraints.add((Lt if strict else Le)(relation1.expr, relation2.expr))
            case ("<" | "=", ">" | "="):
                if ask(Eq(relation1.expr, -relation2.expr)) and (
                    _is_even_root(relation1) or _is_even_root(relation2)
                ):
                    # This is a workaround to a bug where SymPy doesn't recognize the square roots are always nonnegative
                    # in the real domain
                    continue

                constraints.add((Gt if strict else Ge)(relation1.expr, relation2.expr))

    return constraints


def _get_basic_symbols(basic: Basic):
    return frozenset(
        symbol for symbol in basic.free_symbols if isinstance(symbol, Symbol)
    )


@dataclass(frozen=True)
class _InferredSet:
    inferred_set: sympy.Set
    inferred_by: Boolean


@dataclass(frozen=True)
class _InferredConstraint:
    constraint: Boolean
    inferred_by: frozenset[Boolean]


def symbols(symbols_str: str | Iterable[str], *, real=True, **kwargs):
    """Define SymPy symbols.

    This is equivalent to the sympy.symbols function, but symbols are defined in the real domain by default.

    Parameters
    ----------
    symbols_str : str | Iterable[str]
        Space seperated set of symbols or an array of symbols
    real : bool, optional
        Assume symbols are real numbers, by default True
    **kwargs
        Other keyword arguments are passed to the sympy.symbols functions
    """
    return sympy.symbols(symbols_str, real=real, **kwargs)


class Constraints:
    """Creates a set of validation and imputation operations from mathematical SymPy expressions.

    Examples
    --------
    Get all possible validations and imputations, including inferred ones

    >>> from sympy import Eq
    >>> from symconstraints import Constraints, symbols
    >>> a, b, c = symbols('a b c')
    >>> # a=b+c, c<b+3
    >>> constraints = Constraints([Eq(a, 2 * b), c < b + 3])
    >>> for validation in constraints.validations:
    ...     print(validation)
    ...
    Validation: (b, a) => [Eq(a, 2*b)] inferred by (Eq(a, 2*b))
    Validation: (c, b) => [b - c > -3] inferred by (c < b + 3)
    Validation: (c, a) => [a/2 > c - 3] inferred by (c < b + 3, Eq(a, 2*b))
    >>> for imputation in constraints.imputations:
    ...     print(imputation)
    ...
    Imputation: (b) => a = 2*b inferred by (Eq(a, 2*b))
    Imputation: (a) => b = a/2 inferred by (Eq(a, 2*b))
    """

    _validations: list[Validation]
    _imputations: list[Imputation]

    def __init__(self, constraints: Iterable[Boolean]):
        """Create constraints.

        Parameters
        ----------
        constraints : Iterable[Boolean]
            List of SymPy Boolean expressions
        """
        self._symbol_to_sets: defaultdict[Symbol, set[_InferredSet]] = defaultdict(set)
        self._symbols_to_constraints: defaultdict[
            frozenset[Symbol], set[_InferredConstraint]
        ] = defaultdict(set)
        self._imputations = []

        for constraint in constraints:
            simplified_constraint = simplify_logic(constraint, form="cnf", force=True)
            if isinstance(simplified_constraint, And):
                for arg in simplified_constraint.args:
                    if isinstance(arg, Boolean):
                        self._add_constraint(arg, constraint)
            else:
                self._add_constraint(simplified_constraint, constraint)

        for symbol, symbol_sets in self._symbol_to_sets.items():
            for inferred_set1, inferred_set2 in combinations(symbol_sets, 2):
                set1, inferred_by1 = (
                    inferred_set1.inferred_set,
                    inferred_set1.inferred_by,
                )
                set2, inferred_by2 = (
                    inferred_set2.inferred_set,
                    inferred_set2.inferred_by,
                )
                inferred_by = frozenset([inferred_by1, inferred_by2])
                dummy = Dummy(**symbol.assumptions0)
                dummy_relation = simplify_logic(
                    set1.intersect(set2).as_relational(dummy), form="dnf"
                )
                if isinstance(dummy_relation, Or):
                    and_operations: list[Boolean] = []
                    for arg in dummy_relation.args:
                        if isinstance(arg, And):
                            and_operations.append(
                                And(*_and_dummy_to_constraints(arg, dummy))
                            )
                        else:
                            and_operations = []
                            break
                    if len(and_operations) > 0:
                        simplified_constraint = Or(*and_operations)
                        self._symbols_to_constraints[
                            _get_basic_symbols(simplified_constraint)
                        ].add(_InferredConstraint(simplified_constraint, inferred_by))
                elif isinstance(dummy_relation, And):
                    for simplified_constraint in _and_dummy_to_constraints(
                        dummy_relation, dummy
                    ):
                        constraint_symbols = _get_basic_symbols(simplified_constraint)
                        self._symbols_to_constraints[constraint_symbols].add(
                            _InferredConstraint(simplified_constraint, inferred_by)
                        )
                        for constraint_symbol in constraint_symbols:
                            constraint_symbol_set = solveset(
                                simplified_constraint,
                                constraint_symbol,
                                domain=_get_symbol_domain(constraint_symbol),
                            )
                            self._add_possible_imputation_from_set(
                                constraint_symbol_set, constraint_symbol, inferred_by
                            )

        self._validations = [
            Validation(
                frozenset(symbols),
                frozenset(
                    inferred_constraint.constraint
                    for inferred_constraint in inferred_constraints
                ),
                inferred_by=reduce(
                    lambda a, b: a | b.inferred_by, inferred_constraints, frozenset()
                ),
            )
            for symbols, inferred_constraints in self._symbols_to_constraints.items()
            if len(symbols) > 0
        ]

    def _add_constraint(self, constraint: Boolean, inferred_by: Boolean):
        inferred_by_set = frozenset([inferred_by])
        symbols = _get_basic_symbols(constraint)
        self._symbols_to_constraints[symbols].add(
            _InferredConstraint(constraint, inferred_by_set)
        )
        for symbol in symbols:
            symbol_set = solveset(constraint, symbol, domain=_get_symbol_domain(symbol))
            if isinstance(symbol_set, Intersection):
                for subset in symbol_set.args:
                    if isinstance(subset, sympy.Set):
                        self._symbol_to_sets[symbol].add(
                            _InferredSet(subset, inferred_by)
                        )
                        self._add_possible_imputation_from_set(
                            subset, symbol, inferred_by_set
                        )
            elif isinstance(symbol_set, ConditionSet):
                # solveset couldn't return a simple set. Attempt to solve manually.
                # Is it a polynomial inequality?
                if (
                    isinstance(symbol_set.condition, Le | Ge | Gt | Lt)
                    and isinstance(symbol_set.condition.lts, Expr)
                    and isinstance(symbol_set.condition.gts, Expr)
                ):
                    expr = (
                        symbol_set.condition.lts - symbol_set.condition.gts
                        if (symbol in symbol_set.condition.lts.free_symbols)
                        ^ (symbol in symbol_set.condition.gts.free_symbols)
                        else None
                    )

                    if expr is not None and expr.is_polynomial(symbol):
                        # It is a polynomial inequality, solve it as such.
                        expr_poly = Poly(expr, symbol)
                        strict = isinstance(symbol_set.condition, Gt | Lt)
                        GreaterThan = (
                            (lambda x: Interval.Lopen(x, oo))
                            if strict
                            else (lambda x: Interval(x, oo))
                        )
                        LessThan = (
                            (lambda x: Interval.Ropen(-oo, x))
                            if strict
                            else (lambda x: Interval(-oo, x))
                        )
                        try:
                            expr_roots = roots(expr_poly, strict=True, multiple=True)
                            union_args = []
                            # The inequality is in the form of F > 0 if polynomial is negative, i.e., F is negative iff an even
                            # number of factors are negative. F < 0 if polynomial is postive, i.e. F is positive iff an odd
                            # number of factors are odd.
                            for number_of_negatives in range(
                                0 if expr_poly.LC() < 0 else 1,
                                len(expr_roots) + 1,
                                2,
                            ):
                                for negative_indexes in combinations(
                                    range(len(expr_roots)), number_of_negatives
                                ):
                                    intervals = {}
                                    for index, root in enumerate(expr_roots):
                                        for key in intervals.keys():
                                            quotient = key / root
                                            if (
                                                len(quotient.free_symbols) == 0
                                                and quotient.is_real
                                            ):
                                                intervals[key] = Intersection(
                                                    intervals[key],
                                                    LessThan(quotient)
                                                    if index in negative_indexes
                                                    else GreaterThan(quotient),
                                                )
                                                break
                                        else:
                                            intervals[root] = (
                                                LessThan(1)
                                                if index in negative_indexes
                                                else GreaterThan(1)
                                            )
                                    if all(
                                        isinstance(interval, Interval)
                                        for interval in intervals.values()
                                    ):
                                        union_args.append(
                                            Intersection(
                                                *(
                                                    Interval(
                                                        -oo
                                                        if interval.start == -oo
                                                        else root * interval.start,
                                                        oo
                                                        if interval.end == oo
                                                        else root * interval.end,
                                                        left_open=interval.left_open,
                                                        right_open=interval.right_open,
                                                    )
                                                    for root, interval in intervals.items()
                                                )
                                            )
                                        )
                            self._symbol_to_sets[symbol].add(
                                _InferredSet(Union(*union_args), inferred_by)
                            )
                        except UnsolvableFactorError:
                            pass
            else:
                self._symbol_to_sets[symbol].add(_InferredSet(symbol_set, inferred_by))
                self._add_possible_imputation_from_set(
                    symbol_set, symbol, inferred_by_set
                )

    def _add_possible_imputation_from_set(
        self, set_expr: sympy.Set, target_expr: Symbol, inferred_by: frozenset[Boolean]
    ):
        if isinstance(set_expr, FiniteSet) and len(set_expr) == 1:
            expr = set_expr.args[0]
            if isinstance(expr, Expr):
                self._imputations.append(
                    Imputation(
                        _get_basic_symbols(expr),
                        target_expr,
                        expr,
                        inferred_by=inferred_by,
                    )
                )

    @property
    def validations(self) -> list[Validation]:
        """Get all validation operations from the constraints.

        Returns
        -------
        list[Validation]
            Validation operations
        """
        return self._validations

    @property
    def imputations(self) -> list[Imputation]:
        """Get all imputation operations from the constraints.

        Returns
        -------
        list[Imputation]
            Imputation operations
        """
        return self._imputations
