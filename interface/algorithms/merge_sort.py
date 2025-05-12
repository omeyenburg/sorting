from algorithms.base_sort import BaseSort


class MergeSort(BaseSort):
    def sort(self, array, start=0, stop=-1):
        self.iterations += 1

        if stop == -1:
            stop = len(array)
        length = stop - start

        if length == 1:
            self.comparisons += 2
            self.wait()
            return array

        if length == 2:
            self.comparisons += 4
            if array[start] > array[start + 1]:
                self.swap(array, start, start + 1)
            self.wait()
            return array

        self.comparisons += 3

        center = start + length // 2

        self.highlight_index = ()
        self.highlight_group = range(start, stop)
        self.wait()

        a = self.sort(array, start, center)[start:center]
        b = self.sort(array, center, stop)[center:stop]

        a_i = 0
        b_i = 0

        self.highlight_group = range(start, stop)

        while a_i + b_i < length:
            self.iterations += 1
            self.comparisons += 4

            i = start + a_i + b_i
            self.highlight_index = (i,)

            if b_i == len(b) or (not a_i == len(a)) and a[a_i] < b[b_i]:
                array[i] = a[a_i]
                a_i += 1
            else:
                array[i] = b[b_i]
                b_i += 1

            self.wait()

        return array
