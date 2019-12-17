def longest_consec(strarr: list, k: int):
    n = len(strarr)
    if n == 0 or k > n or k <= 0:
        return ''

    lst = []
    for i in range(len(strarr)-k+1):
        word = ''
        for j in range(k):
            word += strarr[i+j]
        lst.append(word)
    longest_word = lst[0]
    for word in lst:
        if len(word) > len(longest_word):
            longest_word = word
    return longest_word
