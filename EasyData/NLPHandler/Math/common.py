import re
COMMON_NUM_PATTERN = r"(\d+\.\d+%?|\d+%?)"

TEXT_NUM_PATTERN = r"(\d+(,\d\d\d)+|\d*\(\d+/\d+\)\d*|\d+\.\d+%?|\d+%?)"
"""
    Patten1: 1,222,333
    Pattte2: 2(1/3)4
    Patten3: 1.2 或 1.2%
    Patten4: 12 或 12%
"""

def is_math_num(number: str, pattern_str=COMMON_NUM_PATTERN):
    # pattern_str = r"\d*\(\d+/\d+\)\d*|\d+\.\d+%?|\d+%?"

    return re.match(pattern_str, number)


