from algorithms.base_sort import BaseSort


class BubbleSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0

        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def iter(self, array):
        if self.index > len(str(max(array))):
            return

        lists = [[] for _ in range(10)]
        for x in array:
            i = x // 10 ** self.index
            lists[i].append(x)

        array.clear()
        for l in lists:
            array.extend(l)


    def sort(self, array):
        iterations = 0

        for i in range(1, len(array)):
            for j in range(len(array) - i):
                if array[j] > array[j + 1]:
                    self.swap(array, j, j + 1)
                iterations += 1
        
        return iterations