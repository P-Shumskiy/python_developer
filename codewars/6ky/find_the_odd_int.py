from collections import Counter


def find_it(seq: list):
    """ function searches integer value in given list that in list are odd times and return this integer value """
    dct = Counter(seq)
    for key, value in dct.items():
        if value % 2 == 1:
            return key
    return None


print(find_it([1, 2, 2, 1, 1]))  # return 1 because it 3 times in list
