from algorithms.base_sort import BaseSort


class BogoSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def sort(self, array):
        last = array[0] - 1
        for x in array:
            if x < last:
                break
            last = x
        else:
            self.done = True
            return

        self.shuffle(array)
        return