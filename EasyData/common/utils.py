import time
from contextlib import contextmanager
from ast import literal_eval

@contextmanager
def divider():
    print("*"*100)
    yield
    print("*"*100)

def print_with_divider(*args):
    with divider():
        print(*args)

def getTime():
    rq = time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time()))
    return rq
