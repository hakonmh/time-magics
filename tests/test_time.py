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


def test_time_does_not_leak_namespace_between_calls():
    """Assignments must not persist in a shared default namespace."""
    tm.time("_tm_leaked_name = 123")
    with pytest.raises(NameError):
        tm.time("_tm_leaked_name")


def test_time_empty_or_comment_only_statement_returns_none():
    """Empty and comment-only statements should not crash."""
    assert tm.time("") is None
    assert tm.time("# comment only") is None


def test_time_prints_timings_when_statement_raises(capsys):
    """%time still reports timings if the statement raises."""
    with pytest.raises(ZeroDivisionError):
        tm.time("1/0")
    captured = capsys.readouterr()
    assert "CPU times:" in captured.out
    assert "Wall time:" in captured.out


def test_time_decorator_preserves_function_name():
    @tm.time_
    def add(a, b):
        return a + b

    assert add.__name__ == "add"
    assert add(2, 3) == 5
