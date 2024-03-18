from algorithms.base_sort import BaseSort


class ShellSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.column_index = 0
        self.index = 0

        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def iter(self, array):
        if len(array) > 100:
            columns = (2147483647, 1131376761, 410151271, 157840433, 58548857, 21521774, 8810089, 3501671,
                       1355339, 543749, 213331, 84801, 27901, 11969, 4711, 1968, 815, 271, 111, 41, 13, 4, 1)
        else:
            columns = (111, 41, 13, 4, 1)

        if self.column_index == len(columns):
            self.done = True
            return

        column = columns[self.column_index]
        for i in range(len(array)):
            value = array[i]
            j = i
            while j >= column and array[j - column] > value:
                array[j] = array[j - column]
                j -= column
            array[j] = value

        self.column_index += 1

    def sort(self, array):
        iterations = 0
        columns = (2147483647, 1131376761, 410151271, 157840433, 58548857, 21521774, 8810089, 3501671,
                   1355339, 543749, 213331, 84801, 27901, 11969, 4711, 1968, 815, 271, 111, 41, 13, 4, 1)
    
        for column in columns:
            for i in range(len(array)):
                value = array[i]
                j = i

                while j >= column and array[j - column] > value:
                    array[j] = array[j - column]
                    j -= column
                    iterations += 1

                array[j] = value

        return iterations


