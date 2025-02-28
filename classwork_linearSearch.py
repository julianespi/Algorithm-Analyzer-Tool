
#Kevin Quan
#2/1/2024

#Write algorithm for performing Linear Serach, where we will find Target element, T, from
def linear_search_all(L, T):

    indices = []

    for index in range(len(L)):
        if L[index] == T:
            indices.append(index)
    return indices

#Taking user input for the list elements
user_input = input("Enter list elements separated by spaces: ")
L = list(map(int, user_input.split()))

#Taking user input for the target element
T = int(input("Enter the target element to search: "))

#Call our function and store the results
result = linear_search_all(L,T)

if result:
    print(f"Element {T} found at indexes: {result}")
else:
    print(f"Element {T} not found in the list")