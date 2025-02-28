#Kevin Quan
#2/22/24 - 12:36 pm

import random
import time

def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2] 
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)

random_list = [random.randint(10,9999) for _ in range(10)]

print("Original Array: ", random_list)
start_time = time.time()
sorted_arr = quick_sort(random_list)
end_time = time.time()
print("Sorted Array: ", sorted_arr)

print(f"Execution time: {end_time - start_time:.6f}")


