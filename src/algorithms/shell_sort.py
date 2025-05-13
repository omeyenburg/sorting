from algorithms.base_sort import BaseSort


class ShellSort(BaseSort):
    def sort(self, array):
        columns = (
            2147483647,
            1131376761,
            410151271,
            157840433,
            58548857,
            21521774,
            8810089,
            3501671,
            1355339,
            543749,
            213331,
            84801,
            27901,
            11969,
            4711,
            1968,
            815,
            271,
            111,
            41,
            13,
            4,
            1,
        )

        for column in columns:
            for i in range(len(array)):
                value = array[i]
                j = i

                while j >= column and array[j - column] > value:
                    array[j] = array[j - column]
                    j -= column

                    self.comparisons += 2
                    self.iterations += 1
                    self.reads += 2
                    self.writes += 1

                    self.highlight_index = (j, j - column)
                    self.highlight_group = range(0, len(array), column)
                    self.wait()

                array[j] = value

        return array
