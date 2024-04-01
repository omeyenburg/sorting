from algorithms.base_sort import BaseSort


class HeapSort(BaseSort):
    def sort(self, array):
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

        array.clear()
        while heap:
            array[:] = [heap[0]] + array
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
                    self.swap(heap, i, left_child)
                    i = left_child
                elif heap[left_child] > heap[right_child]:
                    self.swap(heap, i, left_child)
                    i = left_child
                else:
                    self.swap(heap, i, right_child)
                    i = right_child

                left_child = get_left_child(i)
                right_child = get_right_child(i)

            while i != 0:
                parent = get_parent(i)
                if heap[parent] < heap[i]:
                    self.swap(heap, i, parent)
                    i = parent
                else:
                    break

def get_left_child(i):
    return 2 * i + 1

def get_right_child(i):
    return 2 * i + 2

def get_parent(i):
    return (i - 1) // 2
