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

    @staticmethod
    def shuffle(array):
        for i in range(len(array) - 1):
            j = random.randint(i, len(array) - 1)
            array[i], array[j] = array[j], array[i]