

def map_recursive(condition, function, sequence, types=(str, unicode)):
    """Walks recursively through a sequence and calls for each keys
    and values matching `types` (defautls to `(str, unicode)`) the
    passed `condition`.
    If the return value of the `condition` is positive it calls `function`
    and replaces the return value of the call in the structure.

    Example:

        >>> data = [{'foo': ['upper::bar', 'upper::baz']}]
        >>> result = map_recursive(
        ...     lambda item: item.startswith('upper::'),
        ...     lambda item: item.lstrip('upper::').upper(),
        ...     data)
        >>> data == result
        True
        >>> result
        [{'foo': ['BAR', 'BAZ']}]
    """

    if isinstance(sequence, types) and condition(sequence):
        return function(sequence)

    elif isinstance(sequence, list):
        for i, item in enumerate(sequence[:]):
            sequence[i:i + 1] = [map_recursive(
                    condition, function, item, types=types)]

    elif isinstance(sequence, tuple):
        return tuple(map_recursive(condition, function,
                                         list(sequence), types=types))

    elif isinstance(sequence, dict):
        for key, value in sequence.items():
            value = map_recursive(
                condition, function, value, types=types)

            new_key = map_recursive(
                condition, function, key, types=types)

            if new_key != key:
                del sequence[key]

            sequence[new_key] = value

    return sequence
