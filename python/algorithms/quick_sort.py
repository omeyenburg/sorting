from algorithms.base_sort import BaseSort
# from algorithms.insertion_sort import InsertionSort
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
                self.comparisons += 2
                self.thread_wait()
                return array

            self.comparisons += 3
            self.reads += 2

            if array[start] > array[start + 1]:
                self.swap(array, start, start + 1)
                self.thread_wait()
                return array

            self.thread_wait()
            return array

        """
        if length < 9:
            for i in range(start, stop):
                value = array[i]
                j = i

                while j > 0 and array[j - 1] > value:
                    array[j] = array[j - 1]
                    j -= 1

                    self.reads += 2
                    self.writes += 1
                    self.iterations += 1
                    self.comparisons += 2
                    self.highlight_index = (i, j)
                    self.highlight_group = range(i)
                    self.thread_wait()
                
                array[j] = value

                self.writes += 1
                self.thread_wait()

            return array
        """

        pivot = array[self.variant_func(self, array, start, stop)]
        smaller = start
        greater = stop - 1

        while smaller <= greater:
            self.iterations += 1
            self.comparisons += 1
            self.reads += 1

            if array[smaller] <= pivot:
                smaller += 1
            else:
                self.swap(array, smaller, greater)
                greater -= 1

                self.highlight_index = (-1, smaller, greater)
                self.thread_wait()

        smaller -= 1
        greater += 1
        self.swap(array, start, smaller)

        self.highlight_index = (smaller,)
        self.highlight_group = range(start, stop)
        self.thread_wait()

        self.sort(array, start, smaller)
        self.sort(array, greater, stop)

        return array
    
    def pivot_first(self, array, start, stop):
        return start

    def pivot_last(self, array, start, stop):
        return stop - 1

    def pivot_middle(self, array, start, stop):
        return (start + stop) // 2

    def pivot_random(self, array, start, stop):
        return random.randint(start, stop - 1)

    def pivot_median_of_three(self, array, start, stop):
        middle = (start + stop) // 2
        if (array[start] > array[middle]) ^ (array[start] > array[stop - 1]):
            return start
        elif (array[start] > array[middle]) ^ (array[stop - 1] > array[middle]):
            return middle
        else:
            return stop - 1

    variants = {
        "Pivot = First": pivot_first,
        "Pivot = Last": pivot_last,
        "Pivot = Middle": pivot_middle,
        "Pivot = Random": pivot_random,
        "Pivot = Median": pivot_median_of_three,
    }
