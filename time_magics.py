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
    It is advisable to pass stmt as a raw string if it contains strings with
    newline characters. For example:


    This function, unlike time_magics.timeit(), doesn't use the statement in
    the first line as setup code when running multiple lines.
    >>> tm.time("'This \n will \n fail \n to \n run'")
    SyntaxError: EOL while scanning string literal (<unknown>, line 1

    >>> tm.time(r"'This \n will \n run \n as \n expected'")
    CPU times: user 2 µs, sys: 0 ns, total: 2 µs
    Wall time: 1.91 µs
    """
    magics = _setup_shell(ns)
    result = magics.time(cell=stmt)
    return result


def timeit_(func, repeat=7, number=None, precision=3, quiet=False):
    """A decorator version of time_magics.timeit().

    Use this as a decorator to time a function and print the output
    like the '%timeit' magic command in iPython

    Parameters
    ----------
    stmt : str
        The code you want to time.
    repeat : int, optional
        Number of repeats, each consisting of 'number' loops, and take the
        best result.
    number : int, optional
        How many times to execute stmt. If number is not provided, number is
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
        timeit_result = timeit('func(*args, **kwargs)', ns=locals(), repeat=repeat,
                               number=number, precision=precision, quiet=quiet)
        return timeit_result
    return timed


def timeit(stmt, ns={}, repeat=7, number=None, precision=3,
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
    repeat : int, optional
        Number of repeats, each consisting of 'number' loops, and take the
        best result.
    number : int, optional
        How many times to execute stmt. If number is not provided, number is
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
    It is advisable to pass stmt as a raw string if it contains strings with
    newline characters. For example:

    >>> tm.timeit("'This \n will \n fail \n to \n run'")
    SyntaxError: EOL while scanning string literal (<unknown>, line 1

    >>> tm.timeit(r"'This \n will \n run \n as \n expected'")
    3.68 ns ± 0.049 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
    """
    stmt = _parse_args(stmt, repeat, number, precision, quiet)
    magics = _setup_shell(ns)
    # stmt is cell code if it contains multiple lines (not
    # including \n found in strings)
    # TODO:len(stmt.splitlines()) > 1
    is_cell_code = stmt.count('\n') > stmt.count(r'\n')
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


def _parse_args(stmt, repeat, number, precision, quiet):
    """Parses function arguments into %timeit options"""
    args = f'-o -p {precision} -r {repeat}'
    if number:
        args = args + f' -n {number}'
    if quiet:
        args = args + f' -q'
    return f'{args} {stmt}'
