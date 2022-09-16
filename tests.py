from IPython.terminal.embed import InteractiveShellEmbed
from timeit_magic import timeit, time_it


def _setup_ipython():
    ipshell = InteractiveShellEmbed()
    ipshell.dummy_mode = True
    return ipshell


def test_timeit():
    """Tests timeit_magic.timeit() against the %timeit magic command"""
    # Setup
    LENGTHS = [10, 1000, 1_000_000]
    ipshell = _setup_ipython()
    # Test
    for length in LENGTHS:
        statement = f"sum(range({length}))"
        ipshell.run_line_magic("timeit", statement)
        timeit(statement)
        print('')


@time_it
def _func(n):
    return sum(range(n))


def test_time_it():
    """Tests the time_it() decorator against the %timeit magic command"""
    # Setup Test
    N = 100
    ipshell = _setup_ipython()
    # Test
    ipshell.run_line_magic("timeit", f"sum(range({N}))")
    _func(N)


if __name__ == "__main__":
    test_timeit()
    test_time_it()
