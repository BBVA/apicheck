import random


def dict_generator(field: dict, strategies):
    def _random_proc(size):
        def _next():
            n = random.randint(0, size-1)
            return values[n]
        return _next

    def _const(thing):
        return lambda: thing

    values = field["values"]
    size = len(values)

    if size == 1:
        proc = _const(values[0])
    else:
        proc = _random_proc(size)

    while True:
        yield proc()
