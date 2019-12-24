import string


def is_pangram(s):
    for letter in string.ascii_lowercase:
        if letter not in s.lower():
            return False
    return True


print(is_pangram('qwertyuiopasdfghjklzxcvbnm'))