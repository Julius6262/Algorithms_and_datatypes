import math

# Return a new, empty priority queue (i.e., an empty list).
def createEmptyPQ ():
    return []



# Remove the item with the least priority from the priority queue A and return it.
"""
add element to end of list
move it up
swap (if larger)
"""

def insert(A,e):

    #add new element to list
    A.append(e)
    #get index of new element 
    i = len(A) - 1 


    while i > 0:
        #find parent  index
        parent = (i-1) // 2
        #if parent larger than new element
        if A[parent] > A[i]: 
            #this swaps the elements (called tupple unpacking)
            A[parent], A[i] = A[i], A[parent]
            # set the parent to i, to "bobble up"/ go up the tree until the conditon is satisfied
            i = parent
        else:
            break

# Insert the element e in the priority queue A.
def extractMin (A):
    # check if input list is empty
    if len(A) == 0:
        return None
    
    #smallest element = the root
    min_element = A[0]
    
    # Here we dont have enough elements to switch the first and the last element, since they are the same
    # so we just pop, since we exactred the only element just before
    if len(A) == 1:
        A.pop()
    else:
        #pop last element, and put at the first place
        A[0] = A.pop()

        #heapify (min)
        #start from root again
        i = 0 
        while True: 
            #children indexes
            left = 2 * i + 1 
            right = 2 * i + 2
            #say that current node is the smallest, will check in if statements
            smallest = i 

            # check if left smaller than length of the list, and compare values
            if left < len(A) and A[left] < A[smallest]:
                smallest = left

            # check if right smaller than length of the list, and compare values
            if right < len(A) and A[right] < A[smallest]:
                smallest = right

            #swap, when necessary
            if smallest != i:
                A[i], A[smallest] = A[smallest], A[i]
                i = smallest  

            else: 
                break 

    return min_element