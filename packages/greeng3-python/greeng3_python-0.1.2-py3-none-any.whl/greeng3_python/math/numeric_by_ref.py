"""
The idea is that a numeric object passed into a function can't be modified in place.  e.g. x += 1

Wouldn't it be nice to be able to pass around an object that behaves like a numeric quantity, but can be modified inside a function.

https://documentation.help/Python-PEP/numeric-types.html

https://stackoverflow.com/questions/60616802/how-to-type-hint-a-generic-numeric-type-in-python

Before 3.10:
from typing import SupportsFloat, Union

Numeric = Union[SupportsFloat, complex]
"""
from __future__ import annotations
from typing import Optional, SupportsFloat, TypeAlias, Union

BuiltinNumeric: TypeAlias = SupportsFloat | complex


class RefNumeric:
    """
    An object wrapping a numeric value, but which can be modified
    """

    def __init__(self, value: BuiltinNumeric = 0):
        self._value = value

    def __add__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__add__(other._value if isinstance(other, RefNumeric) else other)

    def __sub__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__sub__(other._value if isinstance(other, RefNumeric) else other)

    def __mul__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__mul__(other._value if isinstance(other, RefNumeric) else other)

    def __floordiv__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__floordiv__(other._value if isinstance(other, RefNumeric) else other)

    def __mod__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__mod__(other._value if isinstance(other, RefNumeric) else other)

    def __divmod__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__divmod__(other._value if isinstance(other, RefNumeric) else other)

    def __pow__(self, other: Union[BuiltinNumeric, RefNumeric], modulo: Optional[Union[BuiltinNumeric, RefNumeric]] = None) -> BuiltinNumeric:
        use_other = other._value if isinstance(other, RefNumeric) else other
        use_modulo = None if use_modulo is None else (
            modulo._value if isinstance(modulo, RefNumeric) else modulo)
        return self._value.__pow__(use_other) if use_modulo is None else self._value.__pow__(use_other, use_modulo)

    def __lshift__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__lshift__(other._value if isinstance(other, RefNumeric) else other)

    def __rshift__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rshift__(other._value if isinstance(other, RefNumeric) else other)

    def __and__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__and__(other._value if isinstance(other, RefNumeric) else other)

    def __xor__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__xor__(other._value if isinstance(other, RefNumeric) else other)

    def __or__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__or__(other._value if isinstance(other, RefNumeric) else other)

    def __div__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__div__(other._value if isinstance(other, RefNumeric) else other)

    def __truediv__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__truediv__(other._value if isinstance(other, RefNumeric) else other)

    def __radd__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__radd__(other._value if isinstance(other, RefNumeric) else other)

    def __rsub__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rsub__(other._value if isinstance(other, RefNumeric) else other)

    def __rmul__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rmul__(other._value if isinstance(other, RefNumeric) else other)

    def __rdiv__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rdiv__(other._value if isinstance(other, RefNumeric) else other)

    def __rtruediv__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rtruediv__(other._value if isinstance(other, RefNumeric) else other)

    def __rfloordiv__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rfloordiv__(other._value if isinstance(other, RefNumeric) else other)

    def __rmod__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rmod__(other._value if isinstance(other, RefNumeric) else other)

    def __rdivmod__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rdivmod__(other._value if isinstance(other, RefNumeric) else other)

    def __rpow__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rpow__(other._value if isinstance(other, RefNumeric) else other)

    def __rlshift__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rlshift__(other._value if isinstance(other, RefNumeric) else other)

    def __rrshift__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rlshift__(other._value if isinstance(other, RefNumeric) else other)

    def __rand__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rand__(other._value if isinstance(other, RefNumeric) else other)

    def __rxor__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__rxor__(other._value if isinstance(other, RefNumeric) else other)

    def __ror__(self, other: Union[BuiltinNumeric, RefNumeric]) -> BuiltinNumeric:
        return self._value.__ror__(other._value if isinstance(other, RefNumeric) else other)

    def __iadd__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value + \
            (other._value if isinstance(other, RefNumeric) else other)
        return self

    def __isub__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value - (other._value if isinstance(other,
                                                                RefNumeric) else other)
        return self

    def __imul__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value * (other._value if isinstance(other,
                                                                RefNumeric) else other)
        return self

    def __idiv__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value / (other._value if isinstance(other,
                                                                RefNumeric) else other)
        return self

    def __itruediv__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value / (other._value if isinstance(other,
                                                                RefNumeric) else other)
        return self

    def __ifloordiv__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value // (other._value if isinstance(other,
                                                                 RefNumeric) else other)
        return self

    def __imod__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value % (other._value if isinstance(
            other, RefNumeric) else other)
        return self

    def __ipow__(self, other: Union[BuiltinNumeric, RefNumeric], modulo: Optional[Union[BuiltinNumeric, RefNumeric]] = None) -> RefNumeric:
        use_other = other._value if isinstance(other, RefNumeric) else other
        use_modulo = None if use_modulo is None else (
            modulo._value if isinstance(modulo, RefNumeric) else modulo)
        self._value = self._value ** use_other
        if modulo is not None:
            self._value = self._value % use_modulo
        return self

    def __ilshift__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value << (other._value if isinstance(
            other, RefNumeric) else other)
        return self

    def __irshift__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value >> (other._value if isinstance(
            other, RefNumeric) else other)
        return self

    def __iand__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value & (other._value if isinstance(
            other, RefNumeric) else other)
        return self

    def __ixor__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value ^ (other._value if isinstance(
            other, RefNumeric) else other)
        return self

    def __ior__(self, other: Union[BuiltinNumeric, RefNumeric]) -> RefNumeric:
        self._value = self._value | (other._value if isinstance(
            other, RefNumeric) else other)
        return self

    def __neg__(self) -> RefNumeric:
        return self._value.__neg__()

    def __pos__(self) -> RefNumeric:
        return self._value.__pos__()

    def __abs__(self) -> RefNumeric:
        return self._value.__abs__()

    def __invert__(self) -> RefNumeric:
        return self._value.__invert__()

    def __complex__(self) -> complex:
        return self._value.__complex__()

    def __int__(self) -> int:
        return self._value.__int__()

    def __float__(self) -> float:
        return self._value.__float__()

    def __str__(self) -> str:
        return str(self._value)


Numeric: TypeAlias = BuiltinNumeric | RefNumeric


def test(x):
    x += 1
    print(x)


x = 1
test(x)
print(x)

y = RefNumeric(10)
test(y)
print(y)
