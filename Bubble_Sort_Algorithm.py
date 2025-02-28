#Kevin Quan
#2/8/2024

# Bubble Sort Algorithm
#Execution time to be recorded

import time
def bubble_sort(students):
    n = len(students)

    for i in range(n):
        for j in range (0, n - i - 1):
            if students[j][1] > students[j + 1][1]: 
                students[j], students[j + 1] = students [j + 1], students[j]

#Take User Input
num_students = int(input("Enter number of students: "))
students = []
for _ in range(num_students):
    name = input("Enter student name: ")
    score = int(input(f"Enter {name}'s score: "))
    students.append((name,score))

#Measure execution time
start_time = time.time()
bubble_sort(students)
end_time = time.time()

print("Sorted students by score: ", students)
print(f"Execution time: {end_time - start_time:.6f} seconds")
