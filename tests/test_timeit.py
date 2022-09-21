import pytest
from .fixtures import *
import time_magics as tm

ARGS = [(STMT1, 'line'), (STMT2, 'cell'), (STMT3, 'cell'), (STMT4, 'cell')]
KWARGS = [(3, 3, 4, False), (1, 1, 3, True)]


@pytest.mark.parametrize(
    ['stmt', 'mode'], ARGS)
@pytest.mark.parametrize(
    ['repeat', 'number', 'precision', 'quiet'], KWARGS)
def test_timeit(stmt, mode, repeat, number, precision, quiet):
    """Tests tm.timeit() against the %timeit magic command"""
    # Setup
    ipython = setup_ipython()
    ns = {**locals(), **globals()}
    ipython.shell.user_ns.update(ns)

    ipython_stmt = _parse_args(stmt, repeat, number, precision, quiet)
    if mode == 'line':
        expected = ipython.timeit(line=ipython_stmt)
    else:
        setup = ipython_stmt.splitlines()[0]
        ipython_stmt = ipython_stmt.replace(setup + '\n', '')
        expected = ipython.timeit(line=setup, cell=ipython_stmt)
    # Test
    result = tm.timeit(stmt, ns=ns, repeat=repeat, number=number,
                       precision=precision, quiet=quiet)
    # Assert
    assert type(result) == type(expected)
    assert len(result.timings) == repeat
    assert result.loops == number
    assert result._precision == precision


def _parse_args(stmt, repeat, number, precision, quiet):
    """Parses function arguments into %timeit options"""
    args = f'-o -p {precision} -r {repeat}'
    if number:
        args = args + f' -n {number}'
    if quiet:
        args = args + f' -q'
    return f'{args} {stmt}'


def test_timeit_():
    """Tests the timeit_() decorator against the %timeit magic command"""
    # Setup Test
    DIFFICULTY = 12
    ipython = setup_ipython()
    ipython.timeit(f"foo({DIFFICULTY})", local_ns={**locals(), **globals()})
    # Test
    _foo = tm.timeit_(foo)
    result = _foo(DIFFICULTY)
    # Assert
    assert hasattr(result, 'timings')
