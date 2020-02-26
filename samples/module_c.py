def find(symbol_to_find, in_str: str):
    accum = 0
    for s in in_str:
        if s == symbol_to_find:
            return accum
        accum += 1
    return -1

def kwar_testing(**kwargs):
    x = kwargs.get('x')
    y = kwargs.get('b')
    if not y:
        x = 2 + x
    something = 42