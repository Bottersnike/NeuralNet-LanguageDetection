import collections


class Map(object):
    def __init__(self):
        self.data = []
        self.__iters = []

    def __getitem__(self, item):
        if type(item) == int:
            if len(self.data) <= item:
                return self.data[item]
            else:
                return []
        else:
            d = self.data
            for i in item:
                d = d[i]
            return d

    def __iter__(self):
        self.__iters = list(flatten(self.data))
        return self

    def next(self):
        if self.__iters:
            return self.__iters.pop(0)
        else:
            raise StopIteration

    def __setitem__(self, key, value):
        if type(key) == int:
            while len(self.data) <= key:
                self.data.append([])
            self.data[key] = value
        else:
            d = self.data
            for i in key:
                while len(d) <= i + 1:
                    d.append([])
                d = d[i]

            d = self.data
            for i in key[:-1]:
                d = d[i]
            d[key[-1]] = value


def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el
