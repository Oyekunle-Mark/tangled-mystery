def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        midpoint = (low + high) // 2

        if arr[midpoint] == target:
            return midpoint

        if arr[midpoint] > target:
            high = midpoint - 1
        else:
            low = midpoint + 1

    return -1
