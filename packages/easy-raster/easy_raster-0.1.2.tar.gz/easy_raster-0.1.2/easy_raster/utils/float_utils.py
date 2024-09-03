from easy_kit.timing import time_func


@time_func
def clamp(x: float, low: float, high: float):
    if x is None:
        return x
    if low is None:
        low = x
    if high is None:
        high = x
    return max(low, min(x, high))


@time_func
def clamp_abs(x: float, low: float, high: float):
    if x is None:
        return x
    if low is None:
        low = abs(x)
    if high is None:
        high = abs(x)
    if abs(x) < low:
        return 0
    if x > high:
        return high
    if x < - high:
        return -high
    return x
