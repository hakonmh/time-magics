# Timeit-magic

iPython `%timeit` magic command in normal Python files.

```python
from timeit_magic import timeit

def foo(n):
    return sum(list(range(n)))

N = 10000
timeit("foo(10_000)", globals=globals())
timeit("foo(100_000_000)", number=10, repeat=1, globals=globals())

>> 98.8 µs ± 1.94 µs per loop (mean ± std. dev. of 7 runs, 5000 loops each)
2.2 s ± 0 ns per loop (mean ± std. dev. of 1 runs, 10 loops each)
```

Timeit-magic allows you to time code in a `.py` file with the same output and behavior as the [`%timeit`](https://docs.python.org/3/library/timeit.html) command in iPython and Jupyter Notebook.
It also provides another function, `time_it`, which allows you to time a function by decorating it:

```python
from timeit_magic import time_it

@time_it
def foo(n):
    return sum(list(range(n)))

N = 10000
# Both time_it and timeit returns the total runtime in seconds
total_time = foo(N)
print(total_time)

>> 97.6 µs ± 2.27 µs per loop (mean ± std. dev. of 7 runs, 5000 loops each)
3.4683985379997466
```

Both functions accepts the optional arguments `repeat` and `number`, which does the same as `-r` and `-n` in `%timeit`.
For more usage information, see the function docstrings and the `timeit` [documentation](https://docs.python.org/3/library/timeit).

## Installation

Timeit-magic can be installed by using `$ pip install timeit-magic`.
