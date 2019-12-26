def maxSequence(array: list):
    if not array:
        return 0
    list_of_sums = []
    for x in range(len(array)):
        for y in range(x, len(array)):
            list_of_sums.append(sum(array[x:y+1]))
    return max(list_of_sums)


print(maxSequence([-2, 1, -3, 4, -1, 2, 1, -5, 4]))
