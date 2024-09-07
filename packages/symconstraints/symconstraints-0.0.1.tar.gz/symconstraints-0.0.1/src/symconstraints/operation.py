"""Operations module."""

from __future__ import annotations

from sympy import Symbol
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sympy.logic.boolalg import Boolean
    from sympy import Expr


@dataclass(eq=True, frozen=True)
class Operation:
    """Generic operation.

    Attributes
    ----------
    keys : frozenset[Symbol]
        Set of keys that this operation needs to check if its not missing before executing.
    inferred_by : frozenset[Boolean]
        Set of constraints which generated this operation.
    """

    keys: frozenset[Symbol]
    inferred_by: frozenset[Boolean] = field(kw_only=True, default_factory=frozenset)


@dataclass(eq=True, frozen=True)
class Validation(Operation):
    """Validation operation.

    Attributes
    ----------
    operations : frozenset[Boolean]
        A set of SymPy Boolean expressions that are used to validate the keys.
    """

    operations: frozenset[Boolean]

    def __str__(self):
        return (
            f'Validation: ({", ".join(str(k) for k in self.keys)}) => [{", ".join(str(op) for op in self.operations)}]'
            f' inferred by ({", ".join(str(op) for op in self.inferred_by)})'
        )

    def __repr__(self):
        return str(self)


@dataclass(eq=True, frozen=True)
class Imputation(Operation):
    """Imputation operation.

    Attributes
    ----------
    target_key : Symbol
        Key that will be imputed by this operation

    operation : Expr
        SymPy expression used to impute the target key
    """

    target_key: Symbol
    operation: Expr

    def __str__(self):
        return (
            f'Imputation: ({", ".join(str(k) for k in self.keys)}) => {str(self.target_key)} = {self.operation}'
            f' inferred by ({", ".join(str(op) for op in self.inferred_by)})'
        )

    def __repr__(self):
        return str(self)
