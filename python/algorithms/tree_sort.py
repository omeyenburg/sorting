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


class TreeSort(BaseSort):
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