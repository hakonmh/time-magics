# Timeit-magic

iPython `%timeit` magic command in normal Python files.

```python
from timeit_magic import timeit

def foo(n):
    return sum(list(range(n)))

timeit("foo(10_000)", globals=globals())
timeit("foo(10_000_000)", number=10, repeat=1, globals=globals())
timeit("foo(10_000_000)", max_time=20, globals=globals())

>> 99.9 µs ± 752 ns per loop (mean ± std. dev. of 7 runs, 20000 loops each)
229 ms ± 0 ns per loop (mean ± std. dev. of 1 runs, 10 loops each)
230 ms ± 2.33 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

Timeit-magic allows you to time code in a `.py` file with the same output and behavior as the [`%timeit`](https://docs.python.org/3/library/timeit.html) command in iPython and Jupyter Notebook.

It also provides another function, `time_it`, which allows you to time a function by decorating it:

```python
from timeit_magic import time_it

@time_it
def foo(n):
    return sum(list(range(n)))

# Both time_it and timeit returns the total runtime in seconds
total_time = foo(10_000)
print(total_time)

>> 101 µs ± 1.53 µs per loop (mean ± std. dev. of 7 runs, 20000 loops each)
14.110744676014292
```

Both functions accepts the optional arguments `repeat` and `number`, which does the same as `-r` and `-n` in `%timeit`.

For more usage information, see the function docstrings and the [`timeit` documentation](https://docs.python.org/3/library/timeit).

## Installation

Timeit-magic can be installed from [PyPI](https://pypi.org/project/timeit-magic/) by using `$ pip install timeit-magic`
