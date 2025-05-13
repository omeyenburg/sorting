from algorithms.base_sort import BaseSort


class BogoSort(BaseSort):
    def sort(self, array):
        while True:
            self.iterations += 1

            if self.check_sorted(array):
                return array

            self.shuffle(array)
            self.wait()
