import statistics
from math import log10, floor, ceil
from timeit import Timer
from time import perf_counter
try:
    import resource
except ImportError:
    resource = None


def time_(func):
    """A decorator version of time_magics.time().

    Use this as a decorator to time a function and print the output
    like the '%time' magic command in iPython

    Returns
    -------
    Returns the 'func' return value.
    """
    def timed(*args, **kwargs):
        nonlocal func
        runtime = time('func(*args, **kwargs)',
                       globals=locals()
                       )
        return runtime

    return timed


def time(stmt="pass", globals={}):
    """Times a function and prints the output like '%time' in iPython.

    time() also returns the 'stmt' return value.

    Parameters
    ----------
    stmt : str
        The code you want to time.
    globals : dict, optional
        Specifies a namespace in which to execute the code.
    """
    result, timings = _time(stmt, globals)
    ts = []
    for timing in timings:
        timing, unit = _format_unit(timing)
        timing = _round_number(timing)
        ts.append((timing, unit))

    print(f"CPU times: user {ts[0][0]} {ts[0][1]}, sys: {ts[1][0]} {ts[1][1]},"
          f" total: {ts[2][0]} {ts[2][1]} \nWall time: {ts[3][0]} {ts[3][1]}")

    return result


def timeit_(func, repeat=7, number=None, max_time=5):
    """A decorator version of time_magics.timeit().

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
        by default 5 seconds. max_time does nothing when number is provided

    Returns
    -------
    float
        Total time taken in seconds.
    """
    def timed(*args, **kwargs):
        nonlocal func
        runtime = timeit('func(*args, **kwargs)',
                         repeat, number, max_time,
                         globals=locals(),
                         )
        return runtime
    return timed


def timeit(stmt="pass", repeat=7, number=None, max_time=5, **kwargs):
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
        by default 5 seconds. max_time does nothing when number is provided
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
    avg = _round_number(avg)
    std, std_unit = _format_unit(std)
    std = _round_number(std)

    output = f"{avg} {avg_unit} ± {std} {std_unit} per loop " \
             f"(mean ± std. dev. of {repeat} runs, {number} loops each)"
    print(output)
    return sum(time_taken)


def _time(stmt, globals):
    """Measures the cpu and wall time of a function.

    Returns
    -------
    tuple
        ('stmt' result, (cpu_user, cpu_sys, cpu_total, wall_time))
    """
    start_wall_time = perf_counter()
    start_cpu_time = _clock()

    result = eval(stmt, globals)

    end_cpu_time = _clock()
    end_wall_time = perf_counter()

    cpu_user = (end_cpu_time[0] - start_cpu_time[0])
    cpu_sys = (end_cpu_time[1] - start_cpu_time[1])
    cpu_total = (cpu_sys + cpu_user)
    wall_time = end_wall_time - start_wall_time

    timings = (cpu_user, cpu_sys, cpu_total, wall_time)
    return result, timings


def _clock():
    """Fetches CPU times in the format (time_user, time_sys)"""
    if resource is not None and hasattr(resource, "getrusage"):
        # Some systems (like windows) don't have getrusage
        return resource.getrusage(resource.RUSAGE_SELF)[:2]
    else:
        # Under windows, system CPU time can't be measured.
        # This just returns perf_counter() and zero.
        return (perf_counter(), 0.0)


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


def _round_number(number):
    """Rounds the number so its of proper length"""
    try:
        round_to = 3 - ceil(log10(number))
    except ValueError:
        round_to = 3

    if round_to == 0:
        number = round(number)
    else:
        number = round(number, round_to)
    return number
