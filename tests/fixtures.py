import time
import bcrypt
import random

from IPython.terminal.embed import InteractiveShellEmbed
from IPython.core.magics.execution import ExecutionMagics

random = random  # Remove flake8 warning
STMT1 = "sum(sorted(random.sample(list(range(100000)), 100000)))"
STMT2 = r"""pystring = 'hello\nworld'
pystring.splitlines()
time.sleep(0.1)
"""
STMT3 = """time.sleep(0.1)
random.seed(100)
pylist = [random.randint(-1000, 1000) for _ in range(1_000_000)]
sum(pylist)
"""
STMT4 = """
time.sleep(0.1)
random.seed(100)
pylist = [random.randint(-1000, 1000) for _ in range(1_000_000)]
sum(pylist)
"""


def setup_ipython():
    ipshell = InteractiveShellEmbed()
    ipshell.dummy_mode = True
    magics = ExecutionMagics(ipshell)
    return magics


def foo(difficulty):
    time.sleep(0.1)
    passwd = "abcdefgh".encode("utf8")
    salt = bcrypt.gensalt(difficulty)
    result = bcrypt.hashpw(passwd, salt)
    return result.decode("utf8")
