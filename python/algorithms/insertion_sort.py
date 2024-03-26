from algorithms.base_sort import BaseSort


class InsertionSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset_old(self):
        self.index = 0

        self.comparisons = 0
        self.iterations = 0

        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def iter(self, array):
        if self.index == len(array):
            self.done = True
            self.highlight_sorting = -1
            self.highlight_comparing = -1
            return

        value = array[self.index]
        i = self.index
        while i > 0 and array[i - 1] > value:
            array[i] = array[i - 1]
            i -= 1
        array[i] = value
        self.index += 1

        self.highlight_sorting = i
        self.highlight_comparing = self.index - 1
        self.highlight_sorted = range(self.index, len(array))

    def sort(self, array):
        iterations = 0

        for i, value in enumerate(array):
            j = i
            while j > 0 and array[j - 1] > value:
                array[j] = array[j - 1]
                j -= 1
            
            iterations += i

            array[j] = value
        
        return iterations, iterations
    
    def sort(self, array):
        self.thread_wait()

        for i, value in self.enumerate(array):
            j = i

            while j > 0 and array[j - 1] > value:
                array[j] = array[j - 1]
                j -= 1

                self.reads += 2
                self.writes += 1
                self.iterations += 1
                self.comparisons += 2
                self.highlight_colored = (i, j)
                self.thread_wait()
            
            array[j] = value

            self.writes += 1
            self.thread_wait()

        self.highlight_colored = ()
        self.sorted = True
        self.running = False

        return array