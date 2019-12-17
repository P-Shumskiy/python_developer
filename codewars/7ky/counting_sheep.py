def count_sheeps(ArrayOfSheeps):
    count = 0
    for i in range(len(ArrayOfSheeps)):
        if ArrayOfSheeps[i]:
            count += 1
    return count


def test_cound_sheeps():
    print('test 1 is {}'.format(count_sheeps(array_1) == 17))
    print('test 2 is {}'.format(count_sheeps(array_2) == 0))
    print('test 3 is {}'.format(count_sheeps(array_2) == 0))


array_1 = [True, True, True, False, True, True, True, True,
           True, False, True, False, True, False, False, True,
           True, True, True, True, False, False, True, True]
array_2 = [False, False, False]
array_3 = []

test_cound_sheeps()
