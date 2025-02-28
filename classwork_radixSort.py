#Kevin Quan
#2/22/24 - 12:36 pm

# LSD and MSD Radix Sort Implementation
import random
import time

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    #count occurences of each digit at the 'exp' place value
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    
    #Convert count[i] to be the actual position index in our output[]
    for i in range(1,10):
        count[i] += count [i - 1]

    #Build Array
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    #Copy stored values from output[] into original array
    for i in range(n):
        arr[i] = output[i]

def lsd_radix_sort(arr):
    max_num = max(arr)
    exp = 1

    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10

    return arr #Return sorted array

def msd_radix_sort(arr):
    max_num = max(arr)
    max_digits = len(str(max_num))

    def msd_radix_helper(arr, digit_place):
        #Recursive functino for MSD Radix Sort
        if len(arr) <= 1 or digit_place < 0:
            return arr

        #Create 10 buckets fordigits 0-9
        buckets = [[] for _ in range(10)]

        for num in arr:
            digit = (num // (10 ** digit_place)) % 10 
            buckets[digit].append(num)

        sorted_arr = []
        for bucket in buckets:
            sorted_arr.extend(msd_radix_helper(bucket, digit_place - 1))
        return sorted_arr
    return msd_radix_helper(arr, max_digits - 1)

#Main Program: taking random input from the user
if __name__ == "__main__":
    num_elements = int(input("Enter the number of elements: "))
    random_list = [random.randint(10, 9999) for _ in range(num_elements)]

    print("\nOriginal Array: ", random_list)

    #Perform LSD Radix Sort
    start_time = time.time()
    lsd_sorted = random_list.copy()
    lsd_radix_sort(lsd_sorted)
    end_time = time.time()
    print("\nSorted using LSD Raidx Sort:", lsd_sorted)
    print(f"Execution time: {end_time - start_time:.6f}")

    #Perform LSD Radix Sort
    print("\nOriginal Array: ", random_list)
    start_time = time.time()
    msd_sorted = random_list.copy()
    msd_radix_sort(msd_sorted)
    end_time = time.time()
    print("\nSorted using MSD Raidx Sort:", msd_sorted)
    print(f"Execution time: {end_time - start_time:.6f}")
