from ast import literal_eval

def literal_wise_eval(data):
    if isinstance(data, str):
        if data[0] in ("[","(","{") and data[0] in ("]",")","}"):
            return literal_eval(data)
        else:
            return data
    else:
        return data