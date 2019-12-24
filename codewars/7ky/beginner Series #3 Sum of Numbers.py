def get_sum(a, b):
    if a == b:
        return a
    elif a > b:
        lst = list(range(b, a+1))
    else:
        lst = list(range(a, b+1))
    return sum(lst)


print(get_sum(0, 1))