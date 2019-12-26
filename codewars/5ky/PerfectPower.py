from math import sqrt, log


def isPP(n):
    for number in range(2, round(sqrt(n)) + 1):
        if abs(round(log(n, number)) - log(n, number)) < 10e-12:
            return [number, round(log(n, number))]
    return None


