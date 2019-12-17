""" Given an array of integers, return a new array with each value doubled
"""


def maps(a):
    return list(map(lambda x: x * 2, a))


def maps2(a):
    return [i * 2 for i in a]

