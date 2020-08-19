from pkg_resources import resource_filename
import warnings

import dockside
from .util import requires

try:
    import pytest
except ImportError:
    pytest = None


@requires(pytest, "pytest")
def test(*args):
    options = [resource_filename("dockside", "")]
    options.extend(list(args))
    return pytest.main(options)


@requires(pytest, "pytest")
def teststrict(*args):
    options = ["--doctest-modules", *list(args)]
    return test(*list(set(options)))


@requires(pytest, "pytest")
def test_nowarnings(*args):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        return teststrict(*args)
