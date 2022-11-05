from enum import Enum

f_var = "x_0"
f_add = "add_2"
f_times = "times_2"
f_cos = "cos_1"
f_sin = "sin_1"
f_minus = "minus_1"
f_relation = "relation_2"
f_norm = "norm_1"
f_sum = "sum_1"
f_square = "square_1"
f_defi_integral = "defi_integral_4"

def ft(x):
    if type(x) == tuple:
        f, n = x[0], int(x[1])
    else:
        f = x
        n = int(x.split("_")[-1])

    return tuple([f, n])
