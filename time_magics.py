from IPython.terminal.embed import InteractiveShellEmbed
from IPython.core.magics.execution import ExecutionMagics


def time_(func):
    """A decorator version of time_magics.time().

    Use this as a decorator to time a function and print the output
    like the '%time' magic command in iPython

    Returns
    -------
    obj
        Returns the func return value.
    """
    def timed(*args, **kwargs):
        nonlocal func
        result = time('func(*args, **kwargs)', ns=locals())
        return result

    return timed


def time(stmt, ns={}):
    """Times a function and prints the output like '%time' in iPython.

    Parameters
    ----------
    stmt : str
        The code you want to time.
    ns : dict, optional
        Specifies a namespace in which to execute the code.
    Returns
    -------
    obj
        The stmt return value. Note that multi-line statements will not return
        anything.
    Notes
    -----
    This function, unlike time_magics.timeit(), doesn't use the statement in
    the first line as setup code when running multiple lines.

    It is advisable to pass stmt as a raw string if it contains strings with
    newline characters. For example:

    >>> tm.time("'This \n will \n fail \n to \n run'")
    SyntaxError: EOL while scanning string literal (<unknown>, line 1

    >>> tm.time(r"'This \n will \n run \n as \n expected'")
    CPU times: user 2 µs, sys: 0 ns, total: 2 µs
    Wall time: 1.91 µs
    """
    magics = _setup_shell(ns)
    result = magics.time(cell=stmt)
    return result


def timeit_(func, r=7, n=None, precision=3, quiet=False):
    """A decorator version of time_magics.timeit().

    Use this as a decorator to time a function and print the output
    like the '%timeit' magic command in iPython

    Parameters
    ----------
    stmt : str
        The code you want to time.
    r : int, optional
        Number of repeats, each consisting of 'n' loops, and take the
        best result.
    n : int, optional
        How many times to execute stmt. If n is not provided, it will
        determined so as to get sufficient accuracy.
    precision : int, optional
        use a precision of <P> digits to display the timing result, by
        default 3.
    quiet : bool, optional
        Do not print result if True, by default False.
    Returns
    -------
    TimeitResult
        Returns a TimeitResult that can be stored in a variable to inspect the
        result in more details.
    """
    def timed(*args, **kwargs):
        nonlocal func
        timeit_result = timeit('func(*args, **kwargs)', ns=locals(), r=r,
                               n=n, precision=precision, quiet=quiet)
        return timeit_result
    return timed


def timeit(stmt, ns={}, r=7, n=None, precision=3,
           quiet=False):
    """Times a function and prints the output like '%timeit' in iPython.

    Time execution of a Python statement or expression using the %timeit
    or %%timeit magic command. This function can be used both as a single
    line and multi line timer:

    - In single line mode you can time a single-line statement (though
    multiple ones can be chained with using semicolons).

    - In multi line mode, the statement in the first line is used as setup
    code (executed but not timed) and the body of the cell is timed. The
    cell body has access to any variables created in the setup code.

    Parameters
    ----------
    stmt : str
        The code you want to time.
    ns : dict, optional
        Specifies a namespace in which to execute the code.
    r : int, optional
        Number of repeats, each consisting of 'n' loops, and take the
        best result.
    n : int, optional
        How many times to execute stmt. If n is not provided, it will
        determined so as to get sufficient accuracy.
    precision : int, optional
        use a precision of <P> digits to display the timing result, by
        default 3.
    quiet : bool, optional
        Do not print result if True, by default False.
    Returns
    -------
    TimeitResult
        Returns a TimeitResult that can be stored in a variable to inspect the
        result in more details.

    Notes
    -----
    In multi line mode, the statement in the first line is used as setup
    code (executed but not timed) and the body of the cell is timed. For example:

    >>> tm.timeit('''time.sleep(1)
    >>> pass''', ns={'time': time})
    3.9 ns ± 0.0672 ns per loop (mean ± std. dev. of 7 runs, 100000000 loops each)

    >>> tm.timeit('''
    >>> time.sleep(1)
    >>> pass''', ns={'time': time})
    1 s ± 363 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)

    It is advisable to pass stmt as a raw string if it contains strings with
    newline characters. For example:

    >>> tm.timeit("'This \n will \n fail \n to \n run'")
    SyntaxError: EOL while scanning string literal (<unknown>, line 1

    >>> tm.timeit(r"'This \n will \n run \n as \n expected'")
    3.68 ns ± 0.049 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    """
    stmt = _parse_args(stmt, r, n, precision, quiet)
    magics = _setup_shell(ns)
    is_cell_code = len(stmt.splitlines()) > 1
    if is_cell_code:
        # In cell mode, the statement in the first line is used as setup code
        # executed but not timed.
        setup = stmt.splitlines()[0]
        stmt = stmt.replace(setup + '\n', '')
        result = magics.timeit(line=setup, cell=stmt)
    else:
        result = magics.timeit(line=stmt)
    return result


def _setup_shell(ns):
    ipshell = InteractiveShellEmbed()
    ipshell.user_ns.update(ns)
    magics = ExecutionMagics(ipshell)
    return magics


def _parse_args(stmt, r, n, precision, quiet):
    """Parses function arguments into %timeit options"""
    args = f'-o -p {precision} -r {r}'
    if n:
        args = args + f' -n {n}'
    if quiet:
        args = args + f' -q'
    return f'{args} {stmt}'
