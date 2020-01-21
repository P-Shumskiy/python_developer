# def add(a: int, b: int) -> int:
#     return a + b
#
#
# answer1 = add(1, 3)
# answer2 = add("Hello ", "World")
#
# print(answer1, answer2, sep="\n")


# def extender(source_list: list, extend_list: list) -> list:
#     source_list.extend(extend_list)
#
#
# values = [1, 2, 3]
# extender(values, [1, 5, 10])
# print(values)

# def foo(*a, **b):
#     for i in a:
#         print(i)
#     for key, item in b.items():
#         print(f'{key}: {item}')
#
#
# foo(1, 2, 3, c='Vasya')

# import random
#
#
# def int_to_str(lst: list):
#     return list(map(lambda x: str(x), lst))
#
#
# print(int_to_str([random.randint(1, 100) for i in range(100)]))

test_tuple = (1, "1", [1])

for element in test_tuple:
    print(f"{element}, type is  {type(element)}")
