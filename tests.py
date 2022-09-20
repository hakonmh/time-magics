import random
from IPython.terminal.embed import InteractiveShellEmbed
import time_magics as tm


def foo(n):
    pylist = list(range(n))
    random.shuffle(pylist)
    return sorted(pylist)


def _setup_ipython():
    ipshell = InteractiveShellEmbed()
    ipshell.dummy_mode = True
    ipshell.run_cell("""
    import random

    def foo(n):
        pylist = list(range(n))
        random.shuffle(pylist)
        return sorted(pylist)
    """)
    return ipshell


def test_time():
    """Tests tm.time() against the %time magic command"""
    # Setup
    LENGTHS = [10, 1000, 1_000_000]
    ipshell = _setup_ipython()
    # Test
    for length in LENGTHS:
        statement = f"foo({length})"
        ipshell.run_line_magic("time", statement)
        result = tm.time(statement, globals={'foo': foo})
        print(result[-5:])
        print('------')


def test_time_():
    """Tests the time_() decorator against the %time magic command"""
    # Setup Test
    N = 100
    ipshell = _setup_ipython()
    # Test
    ipshell.run_line_magic("time", f"foo({N})")
    _foo = tm.time_(foo)
    result = _foo(N)
    print(result[-5:])


def test_timeit():
    """Tests tm.timeit() against the %timeit magic command"""
    # Setup
    LENGTHS = [10, 1000, 1_000_000]
    ipshell = _setup_ipython()
    # Test
    for length in LENGTHS:
        statement = f"foo({length})"
        ipshell.run_line_magic("timeit", statement)
        tm.timeit(statement, max_time=5, globals={'foo': foo})
        print('------')


def test_timeit_():
    """Tests the timeit_() decorator against the %timeit magic command"""
    # Setup Test
    N = 100
    ipshell = _setup_ipython()
    # Test
    ipshell.run_line_magic("timeit", f"foo({N})")
    _foo = tm.timeit_(foo, max_time=5)
    _foo(N)


if __name__ == "__main__":
    test_time()
    print()
    test_time_()
    print()
    test_timeit()
    print()
    test_timeit_()
