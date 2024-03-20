from algorithms.base_sort import BaseSort


class BogoSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.done = False

        self.comparisons = 0
        self.iterations = 0

        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def iter(self, array):
        if self.is_sorted(array):
            self.done = True
            return

        self.shuffle(array)
    
    def sort(self, array):
        for i in range(2*len(array)):
            if self.is_sorted(array):
                self.done = True
                return i, 0

            self.shuffle(array)
        return 2*len(array), 0