def print_l(info, pad="=", length=50):
    print(info.ljust(length, pad))

def print_r(info, pad="=", length=50):
    print(info.rjust(length, pad))

def print_c(info, pad="=", length=50):
    print(info.center(length, pad))