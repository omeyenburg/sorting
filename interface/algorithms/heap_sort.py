from algorithms.base_sort import BaseSort


class HeapSort(BaseSort):
    def sort(self, array):
        heap_size = len(array)

        for i in range(heap_size):
            while i:
                self.reads += 2
                self.comparisons += 1

                parent = get_parent(i)
                if array[parent] >= array[i]:
                    break

                self.swap(array, i, parent)

                self.highlight_index = (i, parent)
                self.iterations += 1
                self.wait()

                i = parent

            self.wait()
        
        while heap_size > 1:
            i = 0
            heap_size -= 1
            self.swap(array, 0, heap_size)

            self.comparisons += 1
            self.highlight_index = (0, heap_size)
            self.highlight_group = range(heap_size, len(array))
            self.wait()

            left_child = get_left_child(i)
            right_child = get_right_child(i)
            
            while left_child < heap_size:
                self.comparisons += 2

                if right_child >= heap_size:
                    self.swap(array, i, left_child)
                    i = left_child
                elif array[left_child] > array[right_child]:
                    self.reads += 2
                    self.swap(array, i, left_child)
                    i = left_child
                else:
                    self.reads += 2
                    self.swap(array, i, right_child)
                    i = right_child

                left_child = get_left_child(i)
                right_child = get_right_child(i)

                self.highlight_index = (-1, -1, i,)
                self.wait()
            
            while i != 0:
                self.comparisons += 2
                self.reads += 2

                parent = get_parent(i)
                if array[parent] >= array[i]:
                    break
                
                self.swap(array, i, parent)
                i = parent

                self.highlight_index = (-1, -1, i,)
                self.wait()

def get_left_child(i):
    return 2 * i + 1

def get_right_child(i):
    return 2 * i + 2

def get_parent(i):
    return (i - 1) // 2
