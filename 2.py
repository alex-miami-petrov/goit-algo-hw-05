def binary_search(arr, target):
    if not arr:
        return 0, float("inf")
    

    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = float("inf")

    while low <= high:
        iterations += 1
        mid = low + (high - low) // 2


        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            low = mid + 1
        else:
            upper_bound = arr[mid]
            high = mid - 1


    return iterations, upper_bound            


