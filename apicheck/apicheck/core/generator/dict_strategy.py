def dict_generator(words_dict):
    def _generator(field: dict, strategies):
        for n in words_dict:
            yield n
    return _generator