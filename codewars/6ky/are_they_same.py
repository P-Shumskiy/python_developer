def comp(array1, array2):
    if not isinstance(array1, list) or not isinstance(array2, list):
        return False
    if sorted([i**2 for i in array1]) == sorted(array2):
        return True
    return False
