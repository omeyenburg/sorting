from algorithms.base_sort import BaseSort


class ShellSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()