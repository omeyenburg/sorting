import random


def sort(array):
    for i in range(len(array)):
        lowest = array[i]
        lowest_i = i

        for j in range(i + 1, len(array)):
            if array[j] < lowest:
                lowest = array[j]
                lowest_i = j

        array[i], array[lowest_i] = array[lowest_i], array[i]

    return array


array = random.sample([i for i in range(20)], 20)
print(sort(array))