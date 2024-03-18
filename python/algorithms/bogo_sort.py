from algorithms.base_sort import BaseSort


class BogoSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()
        self.limit = 1000

    def reset(self):
        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def iter(self, array):
        if self.is_sorted(array):
            self.done = True
            return

        self.shuffle(array)
    
    def sort(self, array):
        for i in range(self.limit):
            if self.is_sorted(array):
                self.done = True
                return i

            self.shuffle(array)
        return 1000