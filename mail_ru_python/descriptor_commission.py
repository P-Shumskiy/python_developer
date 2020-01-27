class Value:
    def __set__(self, instance, value):
        self.value = value - value * instance.commission

    def __get__(self, instance, owner):
        return self.value

    def __delete__(self, instance):
        del self.value


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


def test():
    new_account = Account(0.2)
    amount = 100
    new_account.amount = 100
    if new_account.amount == 80:
        print("#Test 1 OK")
    else:
        print(f"#Test 1 FAILED, amount is {new_account.amount}, "
              f"but must be {amount - amount * new_account.commission}")
    new_account = Account(0)
    new_account.amount = 100
    if new_account.amount == 100:
        print("#Test 2 OK")
    else:
        print("#Test 2 Failed")


if __name__ == '__main__':
    test()
