import pytest
from .fixtures import *
import time_magics as tm

ARGS = [(STMT1, 'line'), (STMT2, 'cell'), (STMT3, 'cell'), (STMT4, 'cell')]
KWARGS = [(3, 3, 4, False), (1, 1, 3, True)]


@pytest.mark.parametrize(
    ['stmt', 'mode'], ARGS, ids=["STMT1", "STMT2", "STMT3", "STMT4"])
@pytest.mark.parametrize(
    ['r', 'n', 'precision', 'quiet'], KWARGS)
def test_timeit(stmt, mode, r, n, precision, quiet):
    """Tests tm.timeit() against the %timeit magic command"""
    # Setup
    ipython = setup_ipython()
    ns = {**locals(), **globals()}
    ipython.shell.user_ns.update(ns)

    ipython_stmt = _parse_args(stmt, r, n, precision, quiet)
    if mode == 'line':
        expected = ipython.timeit(line=ipython_stmt)
    else:
        setup = ipython_stmt.splitlines()[0]
        ipython_stmt = ipython_stmt.replace(setup + '\n', '')
        expected = ipython.timeit(line=setup, cell=ipython_stmt)
    # Test
    result = tm.timeit(stmt, ns=ns, r=r, n=n,
                       precision=precision, quiet=quiet)
    # Assert
    assert type(result) == type(expected)
    assert len(result.timings) == r
    assert result.loops == n
    assert result._precision == precision


def _parse_args(stmt, r, n, precision, quiet):
    """Parses function arguments into %timeit options"""
    args = f'-o -p {precision} -r {r}'
    if n:
        args = args + f' -n {n}'
    if quiet:
        args = args + ' -q'
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


def test_format_timeit_stmt_only_strips_first_line():
    """Cell-mode setup must be the first line only, not every matching line."""
    setup, stmt = tm._format_timeit_stmt(
        "print('hello')\nprint('hello')\nprint('world')\n")
    assert setup == "print('hello')"
    assert stmt == "print('hello')\nprint('world')\n"


def test_format_timeit_stmt_handles_crlf_line_endings():
    setup, stmt = tm._format_timeit_stmt("import time\r\ntime.sleep(1)\r\n")
    assert setup == "import time"
    assert stmt == "time.sleep(1)\r\n"


def test_format_timeit_stmt_single_line_has_no_setup():
    setup, stmt = tm._format_timeit_stmt("1 + 1")
    assert setup == ""
    assert stmt == "1 + 1"


def test_format_timeit_stmt_blank_first_line_is_not_setup():
    source = "\npass\n"
    setup, stmt = tm._format_timeit_stmt(source)
    assert setup == ""
    assert stmt == source


def test_timeit_cell_mode_keeps_duplicate_of_setup_line():
    ns = {"log": []}
    tm.timeit(
        "log.append(1)\nlog.append(1)\nlog.append(2)",
        ns=ns, r=1, n=1, quiet=True)
    assert ns["log"] == [1, 1, 2]


def test_timeit_does_not_time_setup_line():
    ns = {"time": __import__("time")}
    result = tm.timeit(
        "time.sleep(0.2)\npass", ns=ns, r=1, n=1, quiet=True)
    assert result.best < 0.05


def test_timeit_decorator_accepts_keyword_arguments():
    @tm.timeit_(r=1, n=1, quiet=True)
    def add(a, b):
        return a + b

    result = add(1, 2)
    assert result.loops == 1
    assert result.repeat == 1
    assert add.__name__ == "add"


def test_print_timeit_result_warning_has_space(capsys):
    from IPython.core.magics.execution import TimeitResult

    all_runs = [1.0, 5.0]
    result = TimeitResult(1, 2, 1.0, 5.0, all_runs, compile_time=0, precision=3)
    tm._print_timeit_result(result)
    captured = capsys.readouterr()
    assert "This could mean" in captured.out
    assert "Thiscould" not in captured.out
