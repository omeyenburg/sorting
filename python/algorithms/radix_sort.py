from algorithms.base_sort import BaseSort
import math


class RadixSort(BaseSort):
    def sort(self, array):
        offset = max(0, -min(array))
        max_length = int(math.log10(max(array)) + 1)
        sub_arrays = [[] for _ in range(10)]

        for i in range(max_length):
            for value in array[:]:
                sub_arrays[(value + offset) // 10 ** i % 10].append(value)

                self.reads += 2
                self.writes += 1
                self.iterations += 1

                self.variant(self, array, sub_arrays)

            j = 0
            for sub_array in sub_arrays:
                k = j + len(sub_array)
                array[j:k] = sub_array
                sub_array.clear()
                j = k

                self.reads += 1
                self.writes += 1
                self.iterations += 1
                self.wait()

            self.wait()

        return array
    
    def variant_hide_collecting(*_):
        "Hide Collecting"
        return

    def variant_show_collecting(self, array, sub_arrays):
        "Show Collecting"
        start = 0
        for j in range(10):
            array[start:start+len(sub_arrays[j])] = sub_arrays[j]
            start = len(sub_arrays[j])
        self.wait()
