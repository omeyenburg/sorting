from algorithms.base_sort import BaseSort


class TreeSort(BaseSort):
    def sort(self, array):
        out_index = 0
        old_array = array[:]
        tree = [None] * len(array) * 2

        def insert(index, pindex):
            self.iterations += 1
            self.comparisons += 1
            self.highlight_index.append(pindex)
            self.wait()

            if array[index] < array[pindex]:
                if tree[2 * pindex] is None:
                    self.writes += 1
                    self.reads += 3

                    tree[2 * pindex] = index
                else:
                    self.reads += 4

                    insert(index, tree[2 * pindex])
            else:
                if tree[2 * pindex + 1] is None:
                    self.writes += 1
                    self.reads += 3

                    tree[2 * pindex + 1] = index
                else:
                    insert(index, tree[2 * pindex + 1])

                    self.reads += 4
        
        def out(index):
            nonlocal out_index

            if index is None:
                return
            
            self.iterations += 1

            out(tree[2 * index])

            self.highlight_index = (out_index,)
            self.reads += 4
            self.writes += 1

            array[out_index] = old_array[index]
            
            self.wait()
            out_index += 1

            out(tree[2 * index + 1])

        for i in range(1, len(array)):
            self.highlight_index = []
            insert(i, 0)

        out(0)
        return array
