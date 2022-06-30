import re

def is_math_num(number):
    pattern_str = r"\d*\(\d+/\d+\)\d*|\d+\.\d+%?|\d+%?"
    return re.match(pattern_str, number)
