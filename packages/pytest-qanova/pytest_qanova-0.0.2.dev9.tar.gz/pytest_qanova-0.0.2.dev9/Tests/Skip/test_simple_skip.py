"""Simple example skipped test."""

import pytest


@pytest.mark.skip(reason='no way of currently testing this')
def test_simple_skip():
    assert False
    