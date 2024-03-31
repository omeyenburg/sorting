from algorithms.base_sort import BaseSort
import math


class RadixSort(BaseSort):
    def sort(self, array):
        if min(array) < 0:
            raise Exception("Unable to sort values below 0!")

        max_length = int(math.log10(max(array)) + 1)
        lists = [[] for _ in range(10)]

        for i in range(max_length):
            for x in array:
                lists[x // 10 ** i % 10].append(x)

            array.clear()
            for l in lists:
                array.extend(l)
                l.clear()

            self.wait()

        return array
