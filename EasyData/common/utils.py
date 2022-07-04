import time
from contextlib import contextmanager
from ast import literal_eval
from datetime import datetime
import logging

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

@contextmanager
def compute_time():
    start_time = datetime
    yield
    end_time = datetime
    print(f"[]")

# -------------------------------------------------------------- #
# 装饰器
# -------------------------------------------------------------- #
def log_func_info(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args, **kwargs)
        return wrapper

    return decorator

"""
Example:

@use_logging(level="warn")
def foo(name='foo'):
    print("i am %s" % name)

foo()
"""

def log_compute_time(func):
    def wrapper(*args, **kwargs):
        with compute_time():
            return func(*args, **kwargs)
    return wrapper
