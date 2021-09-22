from functools import reduce

class DictionaryUtils:

    @staticmethod
    def safe_get(dictionary, keys, default=None):
        return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."),
                      dictionary)
