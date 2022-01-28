from contextlib import contextmanager
import pytest

from owith.validation import cm_validate
from .context_managers import SimpleContextManager


@pytest.mark.parametrize(
    "obj,typeerror_raised",
    [
        (
            1,
            True,
        ),
        (
            SimpleContextManager(),
            False,
        ),
        (
            # contextlib._GeneratorContextManager
            contextmanager(lambda: (1 for _ in range(1)))(),
            False,
        )
    ]
)
def test_cm_validate(obj, typeerror_raised):

    if not typeerror_raised:
        assert cm_validate(obj) is None
    else:
        with pytest.raises(TypeError):
            cm_validate(obj)
