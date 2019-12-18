import itertools


def get_count(n: int):
    ans = [str(n)[x:y] for x, y in itertools.combinations(range(len(str(n)) + 1),  r=2)]
    ans = list(map(int, ans))
    counter = 0
    for number in ans:
        if number == 0 or n == number:
            continue
        elif n % number == 0:
            counter += 1
    return counter


print(get_count(1))
