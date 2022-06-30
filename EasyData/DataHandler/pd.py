from ast import literal_eval
from ..common import print_with_divider

__all__ = ["literal_wise_eval", "check_nan", "check_unique"]

def literal_wise_eval(data):
    if isinstance(data, str):
        if data[0] in ("[", "(", "{") and data[-1] in ("]", ")", "}"):
            return literal_eval(data)
        else:
            return data
    else:
        return data

def check_nan(df):
    tmp_series = df.isna().sum()  # nan
    print_with_divider(f"{'column':10} \t {'NaN':10}")
    for k, v in tmp_series.items():
        print(f"{k:10} \t {v:10}")


def check_unique(df, columns=None):
    columns = df.columns if columns is None else columns
    print_with_divider(f"{'column':10} \t {'NaN':10}")
    for col in columns:
        try:
            uniuqe_num = len(df[col].unique())
            print(f"{col:10} \t {uniuqe_num:10}")
        except Exception:
            continue
