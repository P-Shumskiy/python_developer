"""In this kata we will only consider finite series and you are required to return a code according to the type of
sequence"""


def sequence_classifier(arr):
    if len(set(arr)) == 1:
        return 5

    if len(set(arr)) == len(arr):
        strictly = True
    else:
        strictly = False

    if sorted(arr) == arr:
        increasing = True
    elif sorted(arr, reverse=True) == arr:
        increasing = False
    else:
        return 0

    if strictly:
        if increasing:
            return 1
        else:
            return 3
    else:
        if increasing:
            return 2
        else:
            return 4


print(sequence_classifier([3, 5, 8, 1, 14, 3]))
