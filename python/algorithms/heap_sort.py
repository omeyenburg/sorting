from algorithms.base_sort import BaseSort


class MaxHeapTree:
    def __init__(self):
        self.root = None

    def append(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self.root.append(value)

    def heapify(self):
        if not self.root is None:
            self.root.heapify()


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def append(self, value):
        if self.value < value:
            value, self.value = self.value, value

        if self.left is None:
            self.left = Node(value)
        elif self.right is None:
            self.right = Node(value)
        elif self.left.value > self.right.value:
            self.left.append(value)
        else:
            self.right.append(value)

    def heapify(self):
        lnone = self.left is None
        rnone = self.left is None

        if lnone:
            if not rnone and self.right.value > self.value:
                self.value, self.right.value = self.right.value, self.value
        elif rnone:
            if self.left.value > self.value:
                self.value, self.left.value = self.left.value, self.value
        elif self.left.value > self.right.value:
            if self.value < self.left.value:
                self.value, self.left.value = self.left.value, self.value
        else:
            if self.value < self.right.value:
                self.value, self.right.value = self.right.value, self.value


class HeapSort(BaseSort):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.index = 0
        self.count = 0

        self.done = False
        self.highlight_sorting = -1
        self.highlight_comparing = -1
        self.highlight_sorted = set()

    def sort(self, array):
        tree = MaxHeapTree()
        for value in array:
            tree.append(value)

        array.clear()
        while not (tree.root.left is None and tree.root.right is None):
            pass