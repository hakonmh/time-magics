import pytest
from .fixtures import *
import time_magics as tm

ARGS = [(STMT1, 'line'), (STMT2, 'cell'), (STMT3, 'cell')]


@pytest.mark.parametrize(
    ['stmt', 'mode'], ARGS, ids=["STMT1", "STMT2", "STMT3"])
def test_time(stmt, mode):
    """Tests tm.time() against the %time magic command"""
    # Setup
    ipython = setup_ipython()
    ns = {**locals(), **globals()}
    ipython.shell.user_ns.update(ns)
    if mode == 'line':
        expected = ipython.time(line=stmt)
    else:
        expected = ipython.time(cell=stmt)
    # Test
    result = tm.time(stmt, ns=ns)
    # Assert
    assert result == expected


def test_time_():
    """Tests the time_() decorator against the %time magic command"""
    # Setup Test
    DIFFICULTY = 12
    ipython = setup_ipython()
    expected = ipython.time(f"foo({DIFFICULTY})",
                            local_ns={**locals(), **globals()})
    # Test
    _foo = tm.time_(foo)
    result = _foo(DIFFICULTY)
    # Assert
    assert len(result) == len(expected)
