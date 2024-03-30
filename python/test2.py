array = [6, 2, 0, 8, 7, 4, 1, 9, 5, 3]

print("Starting array:", array)

start = 0
stop = len(array)

def swap(array, first, second):
        a = array[first]
        array[first] = array[second]
        array[second] = a

pivot_position = stop -1
print("Pivot position:", pivot_position)

pivot = array[pivot_position]
smaller = start
greater = stop - 1

print("Pivot:", pivot)

while smaller <= greater:
    if array[smaller] == pivot:
        pivot_position = smaller
        smaller += 1
    if array[smaller] <= pivot:
        smaller += 1
    else:
        if greater == pivot_position:
             pivot_position = smaller
        swap(array, smaller, greater)
        greater -= 1

greater = smaller
smaller -= 1

swap(array, pivot_position, smaller)

print("Sorted array:", array)
print("Smaller/Greater:", smaller, greater)
print("Smaller array:", array[0:smaller])
print("Greater array:", array[greater:])