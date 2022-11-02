# Time-magics

iPython `%time` and `%timeit` magic command in normal Python files.

```python
import time
import time_magics as tm

def foo(n):
    time.sleep(0.1)
    return sum(list(range(n)))

tm.time("foo(1_000_000)", ns={"foo": foo})
tm.timeit("foo(1_000_000)", ns={"foo": foo})

>> CPU times: user 18.9 ms, sys: 23.8 ms, total: 42.7 ms
Wall time: 143 ms
138 ms ± 1.46 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

Time-magics allows you to time code in a `.py` file with the same output and behavior as the
[`%timeit`](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-timeit)
and [`%time`](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-time)
command in iPython and Jupyter Notebook.

It also provides the functions `time_` and `timeit_`, which allows you to time a function by
decorating it:

```python
import time
import time_magics as tm

@tm.timeit_
def foo(n):
    return sum(list(range(n)))

@tm.time_
def bar(n):
    time.sleep(0.5)
    return sum(list(range(n)))

# Both timeit_ and timeit returns a TimeitResult object
result = foo(10_000)
print("timeit_ output:", type(result), result.best)

# While time_ and time returns the timed statement return value (if any)
value = bar(10_000)
print("time_ output:", value)

>> 97.6 µs ± 825 ns per loop (mean ± std. dev. of 7 runs, 10000 loops each)
timeit_ output: <TimeitResult> 9.643386240350083e-05

CPU times: user 668 µs, sys: 2 µs, total: 670 µs
Wall time: 501 ms
time_ output: 49995000
```

It should be noted that `timeit()` and `timeit_()` returns a `TimeitResult` object, while
`time()` and `time_()` returns the statement return value.

For more usage information, consult the function docstrings.

## Installation

Time-magics is available on [PyPI](https://pypi.org/project/time-magics/):

```console
python -m pip install time-magics
```

## Usage

The `ns` parameter specifies a namespace in which to execute the code:

```python
>>> import time
>>> import time_magics as tm

>>> tm.timeit("time.sleep(0.5)")
NameError: name 'time' is not defined

>>> tm.timeit("time.sleep(0.5)", ns={'time': time})
501 ms ± 24.9 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

`timeit()` and `timeit_()` has the two optional parameters `n` and `r` which does the same
as in `%timeit`:

- `n` - How many times to execute `stmt`. If `n` is not provided, it will determined so as
 to get sufficient accuracy.
- `r` - Number of repeats, each consisting of `n` loops, and take the best result.

```python
import time_magics as tm

tm.timeit('sum(list(range(100)))')
tm.timeit('sum(list(range(100)))', r=3, n=1000)

>> 1.83 µs ± 17 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
1.84 µs ± 14 ns per loop (mean ± std. dev. of 3 runs, 1,000 loops each)
```

### Pitfalls

For multi-line statements `time()` and `timeit()` will run in cell mode (i.e. `%%time[it]`
instead of `%time[it]`). There is a subtle, but crucial difference in behavior between the
 two functions in cell mode:

- `timeit()` will run the first line in the statement string as setup code and is executed, but not
timed. All lines after the setup line are considered the body of the cell and are timed.
- `time()`, on the other hand, doesn't use the first line as setup code when running multiple
lines. The first line will therefore be timed as normal.

Both functions behavior reflects their magic command equivalents.

```python
import time
import time_magics as tm

stmt = """time.sleep(1)
time.sleep(1)
"""

tm.timeit(stmt, ns={'time': time})
tm.time(stmt, ns={'time': time})

>> 1 s ± 233 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)
# Only the last time.sleep is timed, the first line is used as setup
CPU times: user 216 µs, sys: 15 µs, total: 231 µs
Wall time: 2 s  # Both time.sleeps is timed
```

You should pass `stmt` as a raw string if it contains strings with newline (`\n`) characters.
If not, `stmt` may be incorrectly parsed. For example:

```python
>>> import time_magics as tm

>>> tm.time("a = 'This \n will \n fail \n to \n run'")
SyntaxError: EOL while scanning string literal (<unknown>, line 1

>>> tm.time(r"a = 'This \n will \n run \n as \n expected'")
CPU times: user 2 µs, sys: 0 ns, total: 2 µs
Wall time: 1.91 µs

>>> tm.time("a = 'This \\n will \\n also \\n run \\n as \\n expected'")
CPU times: user 1 µs, sys: 0 ns, total: 1 µs
Wall time: 2.15 µs
```
