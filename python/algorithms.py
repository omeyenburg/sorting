import random


class BaseSort:
    def __init__(self):
        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def swap(self, array, first, second):
        a = array[first]
        array[first] = array[second]
        array[second] = a


class SelectionSort(BaseSort):
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


class BubbleSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0
        self.count = 0
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def sort(self, array):
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


class QuickSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def sort(self, array):
        pass


class BogoSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
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
            self.highlight_sorting = -1
            self.highlight_comparing = -1
            self.highlight_sorted = range(len(array))
            return

        a = random.randint(0, len(array) - 1)
        b = random.randint(0, len(array) - 1)
        array[a], array[b] = array[b], array[a]
        self.highlight_sorting = a
        self.highlight_comparing = b
