from algorithms.base_sort import BaseSort
import random


# How to properly implement quick sort:
# https://www.angelfire.com/pq/jamesbarbetti/articles/sorting/001_QuicksortIsBroken.htm


class QuickSort(BaseSort):
    def sort(self, array, start=0, stop=-1):
        self.iterations += 1

        if stop == -1:
            stop = len(array)
        length = stop - start

        if length <= 2:
            self.highlight_index = ()
            self.highlight_group = range(start, stop)

            if length <= 1:
                self.comparisons += 3
                self.wait()
                return array

            self.comparisons += 4
            self.reads += 2

            if array[start] > array[start + 1]:
                self.swap(array, start, start + 1)
                self.wait()
                return array

            self.wait()
            return array
        
        self.comparisons += 1

        pivot_position = self.variant(self, array, start, stop)
        pivot = array[pivot_position]
        smaller = start
        greater = stop - 1

        while smaller <= greater:
            self.iterations += 1

            if array[smaller] <= pivot:
                self.comparisons += 2
                smaller += 1
            else:
                self.comparisons += 3
                if greater == pivot_position:
                    pivot_position = smaller
                self.swap(array, smaller, greater)
                greater -= 1

        greater = smaller
        smaller -= 1
        self.swap(array, pivot_position, smaller)

        self.highlight_index = (smaller,)
        self.highlight_group = range(start, stop)
        self.wait()

        self.sort(array, start, smaller)
        self.sort(array, greater, stop)

        return array

    def variant_pivot_first(self, array, start, stop):
        "Pivot = First"
        return start

    def variant_pivot_last(self, array, start, stop):
        "Pivot = Last"
        return stop - 1

    def variant_pivot_middle(self, array, start, stop):
        "Pivot = Middle"
        return (start + stop) // 2

    def variant_pivot_random(self, array, start, stop):
        "Pivot = Random"
        return random.randint(start, stop - 1)

    def variant_pivot_median_of_three(self, array, start, stop):
        "Pivot = Median"
        middle = (start + stop) // 2
        if (array[start] > array[middle]) ^ (array[start] > array[stop - 1]):
            self.comparisons += 2
            return start
        elif (array[start] > array[middle]) ^ (array[stop - 1] > array[middle]):
            self.comparisons += 4
            return middle
        else:
            self.comparisons += 4
            return stop - 1
