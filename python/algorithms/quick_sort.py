from algorithms.base_sort import BaseSort


class QuickSort(BaseSort):
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
