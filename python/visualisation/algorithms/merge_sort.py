from algorithms.base_sort import BaseSort


class MergeSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0
        self.parts = []

        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def sort(self, array):
        print(self.parts)
        if len(self.parts) == 1:
            self.done = True
            return

        if not self.parts:
            self.parts = [[x] for x in array]
        
        print(self.parts)
        
        part_a = self.parts[self.index]
        part_b = self.parts[self.index + 1]

        print(part_a, part_b)

        part = []
        for i in range(len(part_a) + len(part_b)):
            if (not len(part_a)) or len(part_b) and part_a[0] > part_b[0]:
                part.append(part_b[0])
                part_b = part_b[1:]
            else:
                part.append(part_a[0])
                part_a = part_a[1:]
        
        self.parts = self.parts[:self.index] + [part] + self.parts[self.index+2:]
        self.index += 1
        if self.index + 1 >= len(self.parts):
            self.index = 0

        array[:] = [x for y in self.parts for x in y]
