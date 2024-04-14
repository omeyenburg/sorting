import random


def sort(array):
    if len(array) < 2:
        return array

    pivot = array[0]
    smaller = []
    greater = []

    for value in array[1:]:
        if value <= pivot:
            smaller.append(value)
        else:
            greater.append(value)
    
    return sort(smaller) + [pivot] + sort(greater)


array = random.sample([i for i in range(20)], 20)
print(sort(array))