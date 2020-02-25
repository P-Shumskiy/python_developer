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
#
# test_tuple = (1, "1", [1])
#
# for element in test_tuple:
#     print(f"{element}, type is  {type(element)}")

# class MyContainer:
#     def __init__(self, *values):
#         self.values = dict()
#         for value in values:
#             self.values[value] = value**3
#
#     def __getitem__(self, item):
#         return self.values[item-1: item+2]
#
#     def __setitem__(self, key, value):
#         self.values[key] = value**3
#
#     def __repr__(self):
#         return f"{self.values}"
#
#
# test = MyContainer(1, 2, 3, 4, 5)
# test[6] = 6
# print(test)

                                                                # Дескрипторы


# class MyDescriptor:
#     def __get__(self, instance, owner):
#         print('get')
#
#     def __set__(self, instance, value):
#         print('set')
#
#     def __delete__(self, instance):
#         print('del')
#
#
# class MyClass:
#     attr = MyDescriptor()
#
#
# if __name__ == "__main__":
#     my_instance = MyClass()
#     print(my_instance.attr)
#     my_instance.attr = 10
#     del my_instance.attr


# class Value:
#     def __init__(self):
#         self.value = None
#
#     @staticmethod
#     def _prepare_value(value):
#         return value * 10
#
#     def __get__(self, instance, owner):
#         return self.value
#
#     def __set__(self, instance, value):
#         self.value = self._prepare_value(value)
#
#
# class Class:
#     attr = Value()
#
#
# if __name__ == '__main__':
#     inst = Class()
#     inst.attr = 10
#     print(inst.attr)


# class ImportantValue:
#     def __init__(self, amount):
#         self.amount = amount
#
#     def __get__(self, instance, owner):
#         return self.amount
#
#     def __set__(self, instance, value):
#         with open('log.txt', 'a') as f:
#             f.write(str(value) + '\n')
#
#         self.amount = value ** 2
#
#
# class Account:
#     def __init__(self, amount):
#         self.amount = ImportantValue(amount)
#
#
# if __name__ == '__main__':
#     bob = Account(100)
#     print(bob.amount)
#     bob.amount = 200
#     bob.amount = 250


                                                        #  Property


# class Robot:
#     def __init__(self, power):
#         self._power = power
#
#     power = property()
#
#     @power.setter
#     def power(self, value):
#         if value < 0:
#             self._power = 0
#         else:
#             self._power = value
#
#     @power.getter
#     def power(self):
#         return self._power
#
#     @power.deleter
#     def power(self):
#         del self._power
#
#
# robot = Robot(100)
# print(robot.power)
# robot.power = -100
# print(robot.power)


# class Class:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#     @property
#     def square(self):
#         return self.a * self.b
#
#
# test = Class(2, 5)
# print(test.square)
#
# a = type('MyClass', (), {})
# print(a)


def test_coroutine():
    while True:
        line = yield  # type: str
        if 'python' in line:
            print("I think so too! Give five!")
        else:
            print("Hmm..I don't think so!")


def func_wrapper_for_test_coroutine():
    c = test_coroutine()
    yield from c
    # next(c)
    # c.send("python the best language")
    # c.send("ruby the best language")
    # c.close()


print(type(func_wrapper_for_test_coroutine))
# func_wrapper_for_test_coroutine()
a = func_wrapper_for_test_coroutine()

print(type(a))
print(next(a))
a.send("python the best language")
a.send("ruby the best language")