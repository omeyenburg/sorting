from algorithms.base_sort import BaseSort


class QuickSort(BaseSort):
    """
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0
        self.parts = []

        self.iterations = 0

        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def iter(self, array):
        if self.index == len(array):
            self.done = True
            self.highlight_sorting = -1
            self.highlight_sorted = set()
            return

        if not self.parts:
            self.parts = [array]

        part = self.parts[self.index]
        if len(part) == 1:
            self.index += 1
            return

        pivot = part[0]
        smaller = [x for x in part[1:] if x <= pivot]
        greater = [x for x in part[1:] if x > pivot]
        if smaller and greater:
            self.parts = self.parts[:self.index] + [smaller,
                                                    [pivot], greater] + self.parts[self.index+1:]
        elif smaller:
            self.parts = self.parts[:self.index] + \
                [smaller, [pivot]] + self.parts[self.index+1:]
        else:
            self.parts = self.parts[:self.index] + \
                [[pivot], greater] + self.parts[self.index+1:]

        array[:] = [x for y in self.parts for x in y]

        self.highlight_sorting = array.index(pivot)
        self.highlight_sorted = range(
            self.highlight_sorting - len(smaller), self.highlight_sorting + len(greater))

    def sort(self, array):
        i = 0
        iterations = 0
        parts = [array]

        while i != len(array):
            part = parts[i]
            if len(part) < 2:
                i += 1
                continue

            pivot = part[0]
            smaller = []
            greater = []
            for x in part[1:]:
                if x <= pivot:
                    smaller.append(x)
                else:
                    greater.append(x)
                iterations += 1

            parts = parts[:i] + [smaller, [pivot], greater] + parts[i+1:]

        array[:] = [x for y in parts for x in y]
        return iterations

    def quick_sort(self, array):
        self.iterations += 1

        if len(array) == 2:
            if array[0] < array[1]:
                return array[::-1]
            return array

        if len(array) <= 1:
            return array

        pivot = array[0]
        smaller = []
        greater = []
        for x in array[1:]:
            self.iterations += 1

            if x <= pivot:
                smaller.append(x)
            else:
                greater.append(x)

        return self.quick_sort(smaller) + [pivot] + self.quick_sort(greater)

    def sort(self, array):
        self.quick_sort(array)
        return self.iterations, self.iterations
    """

    def sort(self, array, section=None):
        if section is None:
            section = slice(0, len(array))
        length = section.stop - section.start

        self.highlight_group = range(section.start, section.stop)
        self.iterations += 1
        self.thread_wait()
        
        if length == 2:
            self.comparisons += 2
            self.reads += 2

            if array[section.start] > array[section.start + 1]:
                self.swap(array, section.start, section.start + 1)
                return array
            return array

        if length <= 1:
            self.comparisons += 2
            return array

        pivot = array[section.start]
        smaller = []
        greater = []

        self.comparisons += length
        self.iterations += length
        self.writes += length * 2
        self.reads += length * 2

        for var in array[section]:
            if var < pivot:
                smaller.append(var)
            else:
                greater.append(var)

        array[section] = smaller + greater
        
        self.sort(array, slice(section.start, section.start + len(smaller)))
        self.sort(array, slice(section.start + len(smaller) + 1, section.stop))

        self.highlight_group = range(section.start, section.stop)
        self.thread_wait()

        return array
