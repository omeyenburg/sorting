from algorithms.base_sort import BaseSort


class BubbleSort(BaseSort):
    def sort(self, array):
        for i in range(1, len(array)):
            for j in range(len(array) - i):
                if array[j] > array[j + 1]:
                    self.swap(array, j, j + 1)

                self.highlight_index = (j, j + 1)
                self.highlight_group = range(len(array) - i + 1, len(array))
                self.thread_wait()

            self.iterations += len(array) - i
            self.comparisons += len(array) - i
        
        return array
