from algorithms.base_sort import BaseSort
import math


class RadixSort(BaseSort):
    def sort(self, array):
        if min(array) < 0:
            raise Exception("Unable to sort values below 0!")

        max_length = int(math.log10(max(array)) + 1)
        sub_arrays = [[] for _ in range(10)]

        for i in range(max_length):
            for value in array:
                sub_arrays[value // 10 ** i % 10].append(value)

                self.reads += 2
                self.writes += 1
                self.iterations += 1

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
