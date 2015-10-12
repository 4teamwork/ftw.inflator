
def recursive_encode(data):
    """Encodes unicodes (from json) to utf-8 strings recursively.
    """
    if isinstance(data, unicode):
        return data.encode('utf-8')

    elif isinstance(data, str):
        return data

    elif isinstance(data, dict):
        for key, value in data.items():
            del data[key]
            data[recursive_encode(key)] = recursive_encode(value)
        return data

    elif isinstance(data, list):
        new_data = []
        for item in data:
            new_data.append(recursive_encode(item))
        return new_data

    elif hasattr(data, '__iter__'):
        for item in data:
            recursive_encode(item)
        return data

    else:
        return data
