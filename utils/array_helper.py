def expand_array(array, to, value=[]):
    for _ in range(to - len(array) + 1):
        array.append(value)
    return array[to]