
array = [1, 2, 3, 4, 5]


def insert(heap, index, value):
    if heap[index] is None:
        heap[index] = value
        return

    if heap[index] > value:
        ...


def create_heap(array):
    heap = [None] * len(array)

    for i, ivalue in enumerate(array):
        # insert(heap, 0, value)
        for j, jvalue in enumerate(heap):
            if jvalue is None or ivalue > jvalue:
                heap[j + 1:-1] = heap[j:-2]
                heap[j] = ivalue
                break

    print(heap)


def get_left_child(i):
    return 2 * i + 1


def get_right_child(i):
    return 2 * i + 2


def get_parent(i):
    return (i - 1) // 2


def create_heap(array):
    print("Array =", array)
    heap = []

    for value in array:
        i = len(heap)
        heap.append(value)

        while i:
            parent = get_parent(i)
            if heap[parent] < heap[i]:
                heap[parent], heap[i] = heap[i], heap[parent]
                i = parent
            else:
                break

    print("Heap =", heap)
    return heap


def swap(array, i, j):
    array[i], array[j] = array[j], array[i]


def heap_sort(heap):
    array = []

    while heap:
        array = [heap[0]] + array
        heap[0] = heap[-1]
        heap.pop(-1)

        i = 0
        l = len(heap)

        if not l:
            break

        left_child = get_left_child(i)
        right_child = get_right_child(i)
        
        while left_child < l:
            if right_child >= l:
                swap(heap, i, left_child)
                i = left_child
            elif heap[left_child] > heap[right_child]:
                swap(heap, i, left_child)
                i = left_child
            else:
                swap(heap, i, right_child)
                i = right_child

            left_child = get_left_child(i)
            right_child = get_right_child(i)

        while i != 0:
            parent = get_parent(i)
            if heap[parent] < heap[i]:
                swap(heap, i, parent)
                i = parent
            else:
                break

    print(array)


array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
array = [x for x in range(100)]
heap = create_heap(array)
heap_sort(heap)
