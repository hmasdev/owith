from functools import wraps
from typing import Any, Callable

from .validation import cm_validate

__all__ = [
    "owith",
    "owith_all",
    "dcwith",
]


def owith(func: Callable[..., Any], *args, **kwargs) -> Callable[..., Any]:
    """Incremental application of 'with' to the arguments of a function.

    Args:
        func (Callable[..., Any]): target function.

    Raises:
        TypeError: occurred when func is not callable.
        TypeError: occurred when there is a non-context manager in args or kwargs.

    Returns:
        Callable[..., Any]: wrapped function.

    NOTE:
        owith(func, arg0, ..., argN, kw0=kw0, ..., kwM=kwM) behaves the same as the following funciton: 

        def func_(*args, **kwargs):
            with arg0 as arg0_:
                ...
                with argsN as argN_:
                    with kwM as kwM_:
                        ...
                        with kw0 as kw0_:
                            return func(args0_, ..., argsN_, *args, kw0=kw0_, ..., kwM=kwM_)
    """  # noqa

    if not callable(func):
        raise TypeError("The first argument must be callable.")

    if args:
        # validate
        cm_validate(args[0])

        # wrap
        @wraps(func)
        def wrapped(*args_, **kwargs_):
            with args[0] as args0:
                return func(args0, *args_, **kwargs_)

        return owith(wrapped, *args[1:], **kwargs)

    if kwargs:
        # extract
        key, val = kwargs.popitem()
        # validate
        cm_validate(val)

        # wrap
        @wraps(func)
        def wrapped(*args_, **kwargs_):
            with val as val_:
                kwargs_[key] = val_
                return func(*args_, **kwargs_)

        return owith(wrapped, *args, **kwargs)

    return func


def owith_all(func: Callable[..., Any]) -> Callable[..., Any]:
    """Application of 'with' to all arguments of the function.

    Args:
        func (Callable[..., Any]): target function.

    Raises:
        TypeError: occurred when func is not callable.

    Returns:
        Callable[..., Any]: wrapped function.

    NOTE:
        owith_all(func) behaves the same as the following function

        def func_(*args, **kwargs):
            return owith(func_, *args, **kwargs)

    NOTE:
        If there is a non-context manager in the arguments of owith_all(func), TypeError will be raised.

    """  # noqa

    if not callable(func):
        raise TypeError("The first argument must be callable.")

    @wraps(func)
    def wrapped(*args, **kwargs):
        return owith(func, *args, **kwargs)()

    return wrapped


def dcwith(*args) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Incremental application of 'with'

    Raises:
        TypeError: occurred when there is a non-context manager in args.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]: function decorator.

    NOTE:
        dcwith(arg0, ..., argN)(func) behaves the same as

        def func_(*args, **kwargs):
            with argN, ..., arg0:
                return func(*args, **kwargs)
    """

    # validation
    for arg in args:
        cm_validate(arg)
    # args to kwargs
    kwargs = {f"_arg{i}": v for i, v in enumerate(args)}

    # define decorator
    def deco(func: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(func)
        def wrapped(*args_, **kwargs_):
            kwargs_ = {k: v for k, v in kwargs_.items() if k not in kwargs}
            return func(*args_, **kwargs_)

        return owith(wrapped, **kwargs)

    return deco
