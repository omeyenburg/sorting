from algorithms.base_sort import BaseSort


class SelectionSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    """
    def iter(self, array):
        if self.index == len(array):
            self.done = True
            self.highlight_sorting = -1
            self.highlight_comparing = -1
            return

        lowest_index = self.index
        lowest_value = array[self.index]
        for i, x in enumerate(array[self.index:]):
            if x < lowest_value:
                lowest_index = i + self.index
                lowest_value = x
        self.swap(array, self.index, lowest_index)
        self.index += 1

        self.highlight_sorting = self.index
        self.highlight_comparing = lowest_index
        self.highlight_sorted = range(self.index, len(array))
    """

    def sort(self, array):
        for i, a in self.enumerate(array):
            lowest_index = i
            lowest_value = a

            for j, b in self.enumerate(array[i:]):
                if b < lowest_value:
                    lowest_index = i + j
                    lowest_value = b

                self.comparisons += 1
                self.highlight_colored = (i, i+j, lowest_index)
                self.thread_wait()

            self.swap(array, i, lowest_index)
            self.thread_wait()

        return array
