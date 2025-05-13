from algorithms.base_sort import BaseSort


class SelectionSort(BaseSort):
    def sort(self, array):
        for i, a in self.enumerate(array):
            lowest_index = i
            lowest_value = a

            for j, b in self.enumerate(array[i:]):
                if b < lowest_value:
                    lowest_index = i + j
                    lowest_value = b

                self.comparisons += 1
                self.highlight_index = (i, i + j, lowest_index)
                self.highlight_group = range(i)
                self.wait()

            self.highlight_index = (i, -1, lowest_index)
            self.swap(array, i, lowest_index)
            self.wait()

        return array
