from typing import Any, ContextManager


def cm_validate(obj: Any):
    """Check whether the object has __enter__ and __exit__.

    Args:
        obj (Any): target object

    Raises:
        TypeError: occurred when obj is not an instance of ContextManager.
    """

    if not isinstance(obj, ContextManager):
        raise TypeError(f"{obj} is not a context manager.")
