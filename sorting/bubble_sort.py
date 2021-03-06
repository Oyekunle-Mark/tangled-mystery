from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    swapped = True

    while swapped:
        swapped = False

        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True

    return arr
