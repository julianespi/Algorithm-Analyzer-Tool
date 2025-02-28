# Kevin Quan
# 2/8/2024 11:52 AM

# Merge Sort Algorithm

import random
import time

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Recursively apply merge sort on both halves
        merge_sort(left_half)
        merge_sort(right_half)

        # Merge the two sorted halves
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Add remaining elements from left_half
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        # Add remaining elements from right_half
        while j < len(right_half):
            arr[k] = right_half[j]  
            j += 1
            k += 1

# User input to generate random numbers
num_elements = int(input("Enter the number of elements to be generated in the array: "))

# Generate a list of random integers between 1 and 100
arr = [random.randint(1, 100) for _ in range(num_elements)]
print(f"\nGenerated random array: {arr}")

# Ask user if they want to run Merge Sort on the given array
user_response = input("\nDo you want to run Merge Sort Now? (yes/no): ").strip().lower()

if user_response == 'yes':
    # Measure execution time for Merge Sort
    start_time = time.time()
    merge_sort(arr)
    end_time = time.time()
    
    # Display the Results
    print(f"\nSorted Array: {arr}")
    print(f"Execution time: {end_time - start_time:.6f} seconds")
