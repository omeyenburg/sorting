from algorithms.base_sort import BaseSort


class BinarySortTree:
    def __init__(self):
        self.root = None
        self.iterations = 0

    def append(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self.root.append(value)

    def array(self):
        if self.root is None:
            return []
        return self.root.array()


class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.left = None
        self.right = None

        self.iterations = 0
    
    def append(self, value):
        if value < self.value:
            if self.left is None:
                self.left = Node(value)
            else:
                self.left.append(value)
        else:
            if self.right is None:
                self.right = Node(value)
            else:
                self.right.append(value)

    def array(self):
        array = []
        if not self.left is None:
            array.extend(self.left.array())
        array.append(self.value)
        if not self.right is None:
            array.extend(self.right.array())
        return array
    
def iter(self, array):
    if self.index == len(array):
        self.done = True
        self.highlight_sorting = -1
        self.highlight_sorted = set()
        return

    value = array[self.index]
    self.tree.append(array[self.index])
    array[:] = self.tree.array() + array[self.index+1:]
    self.index += 1

    self.highlight_sorting = array.index(value)
    self.highlight_sorted = range(self.index, len(array))

def sort(self, array):
    tree = BinarySortTree()

    for value in array:
        tree.append(value)

    array[:] = tree.array()
    
    self.wait()
    return array


class TreeSort(BaseSort):
    def sort(self, array):
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

        for i in range(1, len(array)):
            self.highlight_index = []
            insert(i, 0)

        out_index = 0
        old_array = array[:]
        
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
        
        out(0)

        return array
