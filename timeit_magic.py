import statistics
from math import log10, floor, ceil
from timeit import Timer


def time_it(func, repeat=7, number=None, max_time=20):
    """A decorator version of timeit_magic.timeit().

    Use this as a decorator to time a function and print the output
    like the '%timeit' magic command in iPython

    Parameters
    ----------
    repeat : int, optional
        How many times to repeat the timer, by default 7
    number : int, optional
        How many times to execute func, by default None
    max_time : int, optional
        Calls timeit with the number of loops so that total time >= max_time,
        by default 20 seconds. Will not be used if 'number' is provided
    Returns
    -------
    float
        Total time taken in seconds.
    """
    def timed(*args, **kwargs):
        nonlocal func
        runtime = timeit('func(*args, **kwargs)',
                         repeat, number, max_time,
                         globals={**globals(), **locals()},
                         )
        return runtime
    return timed


def timeit(stmt="pass", repeat=7, number=None, max_time=20, **kwargs):
    """Times a function and prints the output like '%timeit' in iPython.

    Parameters
    ----------
    stmt : str
        The code you want to time.
    repeat : int, optional
        How many times to repeat the timer, by default 7
    number : int, optional
        How many times to execute stmt, by default None
    max_time : int, optional
        Calls timeit with the number of loops so that total time >= max_time,
        by default 20 seconds. Will not be used if 'number' is provided
    **kwargs : optional
        Keyword arguments passed to timeit.Timer, for example 'setup' and
        'globals'
    Returns
    -------
    float
        Total time taken in seconds.
    """
    time_taken, number = _timeit(stmt, repeat, number, max_time, **kwargs)
    avg, std = _get_time_stats(time_taken, number)

    avg, avg_unit = _format_unit(avg)
    avg = _format_number(avg)
    std, std_unit = _format_unit(std)
    std = _format_number(std)

    output = f"{avg} {avg_unit} ± {std} {std_unit} per loop " \
             f"(mean ± std. dev. of {repeat} runs, {number} loops each)"
    print(output)
    return sum(time_taken)


def _timeit(stmt, repeat, number, max_time, **kwargs):
    """Measures the running time of a function using timeit.repeat()."""
    timer = Timer(stmt, **kwargs)
    if number:
        time_taken = timer.repeat(repeat, number)
    else:
        time_taken, number = _autorange(timer, max_time, repeat)
    return time_taken, number


def _autorange(timer, max_time, repeat):
    """Return the number of loops and time taken so that total time >= max_time.

    'number' is the number of loops in the seq 1, 2, 5, 10, 20, 50 ... which
    is closest to having a total time taken >= max_time when running in
    timer.repeat().

    Returns
    -------
    tuple
        (time_taken, number)
    """
    estimate = timer.repeat(repeat, 1)
    number = max(round(max_time / sum(estimate)), 1)
    if number > 1:
        number = _find_number(number)
        time_taken = timer.repeat(repeat, number)
        return time_taken, number
    else:
        return estimate, number


def _find_number(number):
    """Finds the number of loops in the seq 1, 2, 5, 10, 20, 50 ... closest
    to having a total time taken >= max_time when running in timer.repeat()
    """
    last_i = 1
    for i in _sequence_generator():
        if number < i:
            return last_i
        last_i = i


def _sequence_generator():
    """Generator yielding a sequence of 1, 2, 5, 10, 20, 50 ..."""
    i = 1
    while True:
        for j in 1, 2, 5:
            yield i * j
        i *= 10


def _get_time_stats(time_taken, number):
    """Calculates the mean and st. deviation of the _timeit runs"""
    avg = sum(time_taken) / (len(time_taken) * number)
    try:
        std = statistics.stdev(time_taken) / number
    except statistics.StatisticsError:
        std = 0
    return avg, std


def _format_unit(number):
    """Decides time unit (either h, min, s, ms, µs or ns) and converts
    'number' to that unit.
    """
    try:
        num_zeros_after_decimal = -floor(log10(number))
    except ValueError:
        num_zeros_after_decimal = 0

    if number > 3600:
        unit = 'h'
        number = number / 3600
    elif number > 60:
        unit = 'min'
        number = number / 60
    elif num_zeros_after_decimal <= 0 and number != 0:
        unit = 's'
    elif 0 < num_zeros_after_decimal <= 3:
        number = number * 10**3
        unit = 'ms'
    elif 3 < num_zeros_after_decimal <= 6:
        number = number * 10**6
        unit = 'µs'
    else:
        number = number * 10**9
        unit = 'ns'

    return number, unit


def _format_number(number):
    try:
        round_to = 3 - ceil(log10(number))
    except ValueError:
        round_to = 3

    if round_to == 0:
        number = round(number)
    else:
        number = round(number, round_to)
    return number
