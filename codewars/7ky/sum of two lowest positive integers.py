def sum_of_two_lowest_positive_integers(numbers):
    numbers.sort(reverse=False)
    return numbers[0] + numbers[1]


def test():
    if sum_of_two_lowest_positive_integers([5, 8, 12, 18, 22]) == 13:
        print('test is OK')
    else:
        print('test is False')
