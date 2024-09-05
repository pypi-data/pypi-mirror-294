from __future__ import annotations

import random
from types import MethodType
from typing import Any, Callable, TypeVar, cast, get_type_hints


class SingleDispatch:
    def __init__(self, func_name: str):
        self._func_name = func_name
        self._impls: dict[type, Callable] = {}
        self._dispatch_cache: dict[type, type] = {}
        self._inst = None
        self._owner = None

        self._inst_type_checking_count: int = 0
        self._inst_type_checking_cycle: int = int(1e5)
        self._random_inst_type_checking_target: int = random.randint(0, self._inst_type_checking_cycle)

    def register_impl(self, func: Callable):
        first_arg_type = list(get_type_hints(func).values())[0]
        self._impls[first_arg_type] = func
        self._dispatch_cache[first_arg_type] = first_arg_type  # dummy value

    def __get__(self, inst, owner):
        self._inst = inst
        self._owner = owner
        return self

    def __call__(self, *args: Any, **kwarg: Any) -> Any:
        if len(args) > 0:
            first_arg = args[0]
        elif len(kwarg) > 0:
            first_arg = list(kwarg.values())[0]
        else:
            first_arg = None
        first_arg_type = type(first_arg)
        try:
            impl = self._impls[self._dispatch_cache[first_arg_type]]
        except KeyError:
            found_impl = False
            for typ in self._impls:
                if isinstance(first_arg, typ):
                    impl = self._impls[typ]
                    self._dispatch_cache[first_arg_type] = typ
                    found_impl = True
                    break
            if not found_impl:
                raise TypeError(f"No implementation found for {self._func_name} with type {first_arg_type}")

        # runtime type checking
        if self._inst_type_checking_count < self._random_inst_type_checking_target:
            self._inst_type_checking_count += 1
        else:
            if not isinstance(first_arg, self._dispatch_cache[first_arg_type]):
                raise TypeError(
                    f"Type mismatch: {first_arg_type} != {self._dispatch_cache[first_arg_type]}, "
                    "usually due to the shape mismatch."
                )
            self._inst_type_checking_count = 0
            self._random_inst_type_checking_target = random.randint(0, self._inst_type_checking_cycle)

        # add `self` to the method
        if self._inst is not None:
            impl = MethodType(impl, self._inst)
        elif self._owner is not None:
            impl = MethodType(impl, self._owner)

        return impl(*args, **kwarg)


_DISPATCH_REGISTRY: dict[str, SingleDispatch] = {}

T = TypeVar("T", bound=Callable)


def singledispatch(is_impl: bool = True) -> Callable[[T], T]:
    """A decorator for single dispatch, will dispatch based on the type of the first argument.
    A lightweight runtime type checking is also implemented.

    Args:
        is_impl (bool, optional): Whether the function is an implementation. Defaults to True.
    """

    def _inner(func: T) -> T:
        func_name = func.__qualname__
        if func_name not in _DISPATCH_REGISTRY:
            _DISPATCH_REGISTRY[func_name] = SingleDispatch(func_name)
        if is_impl:
            _DISPATCH_REGISTRY[func_name].register_impl(func)
        return cast(T, _DISPATCH_REGISTRY[func_name])

    return _inner


__all__ = ["singledispatch"]
