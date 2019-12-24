def disemvowel(string):
    vowels = {'a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y'}
    lst = [letter for letter in string if letter not in vowels]
    return ''.join(lst)


print(disemvowel('This website is for losers LOL!'))
