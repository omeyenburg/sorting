from algorithms.base_sort import BaseSort


class QuickSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0
        self.parts = []

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
            self.parts = self.parts[:self.index] + [smaller, [pivot], greater] + self.parts[self.index+1:]
        elif smaller:
            self.parts = self.parts[:self.index] + [smaller, [pivot]] + self.parts[self.index+1:]
        else:
            self.parts = self.parts[:self.index] + [[pivot], greater] + self.parts[self.index+1:]

        array[:] = [x for y in self.parts for x in y]

        self.highlight_sorting = array.index(pivot)
        self.highlight_sorted = range(self.highlight_sorting - len(smaller), self.highlight_sorting + len(greater))

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

