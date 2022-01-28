from itertools import chain
from typing import Any, Callable, Dict, Tuple
import pytest
from owith import owith, owith_all, dcwith

from .context_managers import (
    SimpleContextManager,
)


@pytest.mark.parametrize(
    "func,cm_args,cm_kwargs,args,kwargs,expected",
    [
        (
            # case 1:
            # context managers as args,
            # no other args and kwargs.
            lambda cm1, cm2: 1,
            (
                SimpleContextManager(),
                SimpleContextManager(),
            ),
            {},
            (),
            {},
            1,
        ),
        (
            # case 2:
            # context managers as kwargs,
            # no other args and kwargs.
            lambda cm1, cm2: 100,
            (),
            {
                "cm1": SimpleContextManager(),
                "cm2": SimpleContextManager(),
            },
            (),
            {},
            100,
        ),
        (
            # case 3:
            # context managers as args and kwargs,
            # no other args and kwargs
            lambda cm1, cm2: 10,
            (
                SimpleContextManager(),
            ),
            {
                "cm2": SimpleContextManager(),
            },
            (),
            {},
            10,
        ),
        (
            # case 4-1: no context managers
            lambda: -1,
            (),
            {},
            (),
            {},
            -1,
        ),
        (
            # case 4-2: no context managers
            lambda x, y: (x, y),
            (),
            {},
            (1, 2),
            {},
            (1, 2),
        ),
        (
            # case 5-1:
            # context managers as args,
            # other kwargs given.
            lambda cm1, cm2, kwd1="hoge", kwd2="fuga": kwd1 + kwd2,
            (
                SimpleContextManager(),
                SimpleContextManager(),
            ),
            {},
            (),
            {
                "kwd1": "HOGE",
                "kwd2": "FUGA",
            },
            "HOGEFUGA",
        ),
        (
            # case 5-2:
            # context managers as kwargs,
            # other kwargs given.
            lambda cm1=None, cm2=None, kwd1="hoge", kwd2="fuga": kwd1 + kwd2,
            (),
            {
                "cm1": SimpleContextManager(),
                "cm2": SimpleContextManager(),
            },
            (),
            {
                "kwd1": "HOGE",
                "kwd2": "FUGA",
            },
            "HOGEFUGA",
        ),
        (
            # case 5-3:
            # context managers as args and kwargs,
            # other kwargs given.
            lambda cm1=None, cm2=None, kwd1="hoge", kwd2="fuga": kwd1 + kwd2,
            (SimpleContextManager(),),
            {
                "cm2": SimpleContextManager(),
            },
            (),
            {
                "kwd1": "HOGE",
                "kwd2": "FUGA",
            },
            "HOGEFUGA",
        ),
        (
            # case 6-1:
            # cotnext managers as kwargs
            # other args given.
            lambda arg0, arg1, cm1, cm2: arg0 + arg1,
            (),
            {
                "cm1": SimpleContextManager(),
                "cm2": SimpleContextManager(),
            },
            (10, 20),
            {},
            30,
        ),
        (
            # case 6-2:
            # cotnext managers as args
            # other args given.
            lambda cm1, cm2, arg0, arg1: arg0 + arg1,
            (
                SimpleContextManager(),
                SimpleContextManager(),
            ),
            {},
            (10, 20),
            {},
            30,
        ),
        (
            # case 6-3:
            # cotnext managers as args and kwargs, other args given.
            lambda cm1, arg0, arg1, cm2: arg0 + arg1,
            (SimpleContextManager(),),
            {
                "cm2": SimpleContextManager(),
            },
            (10, 20),
            {},
            30,
        ),
        (
            # case 7-1:
            # context managers as args,
            # other args and kwargs given.
            lambda cm1, cm2, x, kwd=False: (x, kwd),
            (
                SimpleContextManager(),
                SimpleContextManager(),
            ),
            {},
            (False,),
            {"kwd": True},
            (False, True),
        ),
        (
            # case 7-2: context managers as kwargs
            # other args and kwargs given.
            lambda x, cm1, cm2, kwd=False: (x, kwd),
            (),
            {
                "cm1": SimpleContextManager(),
                "cm2": SimpleContextManager(),
            },
            (False,),
            {"kwd": True},
            (False, True),
        ),
        (
            # case 7-3:
            # context managers as args and kwargs,
            # other args and kwargs given.
            lambda cm1, x, cm2, kwd=False: (x, kwd),
            (
                SimpleContextManager(),
            ),
            {
                "cm2": SimpleContextManager(),
            },
            (False,),
            {"kwd": True},
            (False, True),
        ),
    ]
)
def test_owith(
    func: Callable,
    cm_args: Tuple,
    cm_kwargs: Dict,
    args: Tuple,
    kwargs: Dict,
    expected: Any,
):
    # preparation
    func.__name__ = "func"
    func.__doc__ = "This is a test"
    wrapped = owith(func, *cm_args, **cm_kwargs)

    # pre-assert
    # assert whether all contextmanagers have not been used.
    for cm in chain(cm_args, cm_kwargs.values()):
        assert not cm.entered
        assert not cm.exited

    # execute
    actual = wrapped(*args, **kwargs)

    # assert
    # assert whether all contextmanagers have been used in with statement.
    for cm in chain(cm_args, cm_kwargs.values()):
        assert cm.entered
        assert cm.exited
    # assert whether wrapped wraps func.
    assert wrapped.__name__ == func.__name__
    assert wrapped.__doc__ == func.__doc__
    # assert the output is equal with the expected output.
    assert actual == expected


@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        (
            # args case
            lambda x: 1,
            (1,),
            {},
        ),
        (
            # kwargs case
            lambda x: 1,
            (),
            {"x": 1},
        ),
    ]

)
def test_owith_with_not_contextmanager(func, args, kwargs):

    with pytest.raises(TypeError):
        owith(func, *args, **kwargs)


def test_owith_with_first_arg_not_callable():
    with pytest.raises(TypeError):
        owith(1)


@pytest.mark.parametrize(
    "func,cm_args,cm_kwargs,expected",
    [
        (
            # args case
            lambda x, y: 1,
            (
                SimpleContextManager(),
                SimpleContextManager(),
            ),
            {},
            1,
        ),
        (
            # kwargs case
            lambda x, y: 2,
            (),
            {
                "x": SimpleContextManager(),
                "y": SimpleContextManager(),
            },
            2,
        ),
        (
            # args and kwargs case
            lambda x, y: 3,
            (
                SimpleContextManager(),
            ),
            {
                "y": SimpleContextManager(),
            },
            3
        )
    ]
)
def test_owith_all(func, cm_args, cm_kwargs, expected):

    # preparation
    func.__name__ = "name"
    func.__doc__ = "this is a test"
    func_ = owith_all(func)

    # pre-assert
    # assert whether all contextmanagers have not been used.
    for cm in chain(cm_args, cm_kwargs.values()):
        assert not cm.entered
        assert not cm.exited

    # execute
    actual = func_(*cm_args, **cm_kwargs)

    # assert
    # assert whether all contextmanagers have been used in with statement.
    for cm in chain(cm_args, cm_kwargs.values()):
        assert cm.entered
        assert cm.exited
    # assert whether func_ wraps func.
    assert func_.__name__ == func.__name__
    assert func_.__doc__ == func.__doc__
    # assert the output is equal with the expected output.
    assert actual == expected


@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        (
            lambda x: 1,
            (1,),
            {},
        ),
        (
            lambda x: 1,
            (),
            {"x": 1},
        ),
    ]
)
def test_owith_all_with_not_context_manager(func, args, kwargs):

    with pytest.raises(TypeError):
        owith_all(func)(*args, **kwargs)


def test_owith_all_for_non_callable():
    with pytest.raises(TypeError):
        owith_all(1)


def test_dcwith():
    # preparation
    cm = SimpleContextManager()
    assert not cm.entered
    assert not cm.exited
    # execute
    assert dcwith(cm)(lambda x: 1)(x=100) == 1
    # assert
    assert cm.entered
    assert cm.exited


def test_dcwith_with_not_context_manager():
    with pytest.raises(TypeError):
        dcwith(1)
