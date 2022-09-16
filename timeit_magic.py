import statistics
from math import log10, floor, ceil
from timeit import Timer


def time_it(func, repeat=7, number=None):
    """A decorator version of timeit_magic.timeit().

    Use this as a decorator to time a function and print the output
    like the '%timeit' magic command in iPython

    Parameters
    ----------
    repeat : int, optional
        How many times to repeat the timer, by default 7
    number : int, optional
        How many times to execute func, by default None
    Returns
    -------
    float
        Total time taken in seconds.
    """
    def timed(*args, **kwargs):
        nonlocal func
        runtime = timeit('func(*args, **kwargs)',
                         repeat, number,
                         globals={**globals(), **locals()},
                         )
        return runtime
    return timed


def timeit(stmt="pass", repeat=7, number=None, **kwargs):
    """Times a function and prints the output like '%timeit' in iPython.

    Parameters
    ----------
    stmt : str
        The code you want to time.
    repeat : int, optional
        How many times to repeat the timer, by default 7
    number : int, optional
        How many times to execute stmt, by default None
    **kwargs : optional
        Keyword arguments passed to timeit.Timer, for example 'setup' and 'globals'
    Returns
    -------
    float
        Total time taken in seconds.
    """
    time_taken, number = _timeit(stmt, repeat, number, **kwargs)
    avg, std = _get_time_stats(time_taken, number)

    avg, avg_unit = _format_unit(avg)
    avg = _format_number(avg)
    std, std_unit = _format_unit(std)
    std = _format_number(std)

    output = f"{avg} {avg_unit} ± {std} {std_unit} per loop " \
             f"(mean ± std. dev. of {repeat} runs, {number} loops each)"
    print(output)
    return sum(time_taken)


def _timeit(stmt, repeat, number, **kwargs):
    timer = Timer(stmt, **kwargs)
    if number:
        time_taken = timer.repeat(repeat, number)
    else:
        time_taken, number = __autorange(timer, repeat)
    return time_taken, number


def __autorange(timer, repeat):
    MAX_TIME = ceil(20 / repeat)
    i = 1
    while True:
        for j in 1, 2, 5:
            number = i * j
            time_taken = timer.repeat(repeat, number)
            if sum(time_taken) >= MAX_TIME:
                return time_taken, number
        i *= 10


def _get_time_stats(time_taken, number):
    avg = sum(time_taken) / (len(time_taken) * number)
    try:
        std = statistics.stdev(time_taken) / number
    except statistics.StatisticsError:
        std = 0
    return avg, std


def _format_unit(num):
    try:
        num_zeros = -floor(log10(num))
    except ValueError:
        num_zeros = 0

    if num_zeros <= 0 and num != 0:
        unit = 's'
    elif 0 < num_zeros <= 3:
        num = num * 10**3
        unit = 'ms'
    elif 3 < num_zeros <= 6:
        num = num * 10**6
        unit = 'µs'
    else:
        num = num * 10**9
        unit = 'ns'

    return num, unit


def _format_number(num):
    try:
        round_to = 3 - ceil(log10(num))
    except ValueError:
        round_to = 3

    if round_to == 0:
        num = round(num)
    else:
        num = round(num, round_to)
    return num
