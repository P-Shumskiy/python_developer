def create_phone_number(n: list):
    return '({0}{1}{2}) {3}{4}{5}-{6}{7}{8}{9}'.format(*n)


print(create_phone_number([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]))
