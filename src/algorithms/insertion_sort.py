from algorithms.base_sort import BaseSort


class InsertionSort(BaseSort):
    def sort(self, array):
        for i, value in self.enumerate(array):
            j = i

            while j > 0 and array[j - 1] > value:
                array[j] = array[j - 1]
                j -= 1

                self.reads += 2
                self.writes += 1
                self.iterations += 1
                self.comparisons += 2
                self.highlight_index = (i, j)
                self.highlight_group = range(i)
                self.wait()

            array[j] = value

            self.writes += 1
            self.wait()

        return array

