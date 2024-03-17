from algorithms.base_sort import BaseSort


class InsertionSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def sort(self, array):
        if self.index == len(array):
            self.done = True
            self.highlight_sorting = -1
            self.highlight_comparing = -1
            return

        x = array[self.index]
        goal = 0
        for i in range(self.index + 1):
            if x <= array[i]:
                goal = i
                break

        array.remove(x)
        array[:] = array[:goal] + [x] + array[goal:]
        self.index += 1

        self.highlight_sorting = goal
        self.highlight_comparing = self.index - 1
        self.highlight_sorted = range(self.index, len(array))