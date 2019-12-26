import itertools


def permutations(string):
    return list(''.join(permutation) for permutation in set(itertools.permutations(string)))


print(type(permutations('abadgGfade')))
