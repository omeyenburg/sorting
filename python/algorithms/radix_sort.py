from algorithms.base_sort import BaseSort
import math


class RadixSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0

        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def iter(self, array):
        if self.index > math.log10(max(array)) + 1:
            self.done = True
            self.highlight_sorted = set()
            return 0

        lists = [[] for _ in range(10)]
        for x in array:
            i = x // 10 ** self.index % 10
            lists[i].append(x)

        self.index += 1
        self.highlight_sorted = set()
        array.clear()
        for l in lists:
            self.highlight_sorted.add(len(array))
            array.extend(l)
        return 1

    def sort(self, array):
        if min(array) < 0:
            return -1, -1

        max_length = int(math.log10(max(array)) + 1)
        lists = [[] for _ in range(10)]

        for i in range(max_length):
            for x in array:
                lists[x // 10 ** i % 10].append(x)

            array.clear()
            for l in lists:
                array.extend(l)
                l.clear()

        return max_length * (len(array) + 10), 0
        
