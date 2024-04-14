import random


def sort(array):
    for i in range(len(array)):
        value = array[i]
        j = i

        while j > 0 and array[j - 1] > value:
            array[j], array[j - 1] = array[j - 1], array[j]
            j -= 1

        array[j] = value

    return array


array = random.sample([i for i in range(20)], 20)
print(sort(array))