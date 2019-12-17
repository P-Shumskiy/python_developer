def high_and_low(numbers: str):
    numbers = list(map(int, numbers.split()))
    return '{} {}'.format(max(numbers), min(numbers))


def test_high_and_low():
    if high_and_low("1 2 3 4 5") == "5 1":
        print('test 1 is OK')
    else:
        print('test 1 is Failed')
    if high_and_low("1 2 -3 4 5") == "5 -3":
        print('test 2 is OK')
    else:
        print('test 2 is Failed')
    if high_and_low("1 9 3 4 -5") == "9 -5":
        print('test 3 is OK')
    else:
        print('test 3 is Failed')


test_high_and_low()
