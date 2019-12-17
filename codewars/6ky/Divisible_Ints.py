import itertools


def get_count(n: str):
    ans = [n[x:y] for x, y in itertools.combinations(range(len(n) + 1),  r=2)]
    ans = list(map(int, ans))
    counter = 0
    for number in ans:
        try:
            if int(n) % number == 0:
                counter += 1
        except ZeroDivisionError:
            continue
    print(ans)
    return counter-1


print(get_count('123032452346'))
