def longest_consec(strarr, k):
    strarr_sorted = sorted(strarr, reverse=False)
    length = len(strarr)
    for i in range(k, -1, -1):
        print(strarr_sorted[length], sep='')