import re
COMMON_NUM_PATTERN = re.compile(r"\d*\(\d+/\d+\)\d*|\d+\.\d+%?|\d+%?")


def is_math_num(number: str):
    pattern_str = r"\d*\(\d+/\d+\)\d*|\d+\.\d+%?|\d+%?"
    return re.match(pattern_str, number)


