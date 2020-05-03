# x = int(input("Enter positive number, please: "))
# assert x > 0, "Value must be postivie"
from contracts import contract


@contract(x='float', returns='float,>0')
def foo(x):
    pass


@contract
def foo2(x):
    """Function with contract
        :type x: float
        :rtype: float,>=0
    """


@contract
def foo3(x: 'float') -> 'float, >=0':
    pass


# foo(1)
# foo2(1)
# foo3(1)
#
def gcd(a, b):
    assert (isinstance(a, int) and
            isinstance(b, int) and
            a > 0 and
            b > 0)
    while b != 0:
        r = a % b
        b = a
        a = r
    return a


# @contract
# def foo(z: 'dict(int:)|dict(float:)'):
#     return z
#
# foo({1.1: 2, 1.1: 3})

gcd('3', 2)

list.sort()