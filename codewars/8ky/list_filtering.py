def filter_list(l):
    """ Function takes list of non-negative integers and strings and return a new list with the string
        filtered out
    """
    return [number for number in l if isinstance(number, int)]
