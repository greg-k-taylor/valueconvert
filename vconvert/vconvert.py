from vconvert.type import to_float
from vconvert.type import to_int


def last_element(d, key_list):
    k = key_list.pop(0)
    if not key_list:
        yield k, d
    if not d:
        yield k, d
    else:
        try:
            t = d[k]
        except:
            yield k, None
            return
        if isinstance(t, dict):                
            yield from last_element(d[k], key_list)
        elif isinstance(t, list):
            for l in t:
                yield from last_element(l, key_list.copy())
        elif isinstance(t, tuple):
            # unsupported type
            raise ValueError("unsupported type in key {}".format(k))

def safe_ref(k, d):
    if d:
        try:
            return d[k]
        except KeyError:
            pass
    
def key_value(dictionary, key):
    key_list = key.split('.')
    for k, le in last_element(dictionary, key_list):
        yield safe_ref(k, le)

def set_key_value(dictionary, key, value):
    def safe_assign(k, d):
        if d:
            try:
                d[k] = value
            except KeyError:
                pass

    key_list = key.split('.')
    for k, le in last_element(dictionary, key_list):
        safe_assign(k, le)
    return dictionary

def traverse_keys(d, include_keys=[], exclude_keys=[]):
    """
    # bydefault, traverse all kes
    # only traverse the list from include_kes a.b, a.b.c
    # only exclude the list from exclude_keys
    """
    if include_keys:
        for k in include_keys:
            for val in key_value(d, k):
                yield k, val

def value_convert(d, fn, include_keys=[], exclude_keys=[]):
    for path, value in traverse_keys(d, include_keys, exclude_keys):
        new_value = fn(value)
        set_key_value(d, path, new_value)
    return d

def int_convert(d, include_keys=[], exclude_keys=[]):
    return value_convert(d, to_int, include_keys, exclude_keys)

def float_convert(d, include_keys=[], exclude_keys=[]):
    return value_convert(d, to_float, include_keys, exclude_keys)
