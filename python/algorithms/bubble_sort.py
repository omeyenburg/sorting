from algorithms.base_sort import BaseSort


class BubbleSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0
        self.count = 0

        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def iter(self, array):
        if self.count == len(array) - 1:
            self.done = True
            self.highlight_sorting = -1
            self.highlight_comparing = -1
            self.highlight_sorted = range(len(array))
            return

        if array[self.index] > array[self.index + 1]:
            self.swap(array, self.index, self.index + 1)

        self.highlight_sorting = self.index + 1
        self.highlight_comparing = self.index
        self.highlight_sorted = range(len(array) - self.count, len(array))

        self.index += 1
        if self.index + 1 == len(array) - self.count:
            self.index = 0
            self.count += 1

    def sort(self, array):
        iterations = 0

        for i in range(1, len(array)):
            for j in range(len(array) - i):
                if array[j] > array[j + 1]:
                    self.swap(array, j, j + 1)
                iterations += 1
        
        return iterations