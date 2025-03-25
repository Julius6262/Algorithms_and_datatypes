"""todo:#extractMin(A): Remove the item with the least priority from the priority queue A and return it
# For simplicity, assume that extractMin(A) is only called on a non-empty
#priority queue. It is left to the user of the priority queue to ensure this, for
#example by keeping track of the number of elements in the priority queue.

todo:#insert(A,e): Insert the element e in the priority queue A
todo: #createEmptyPQ(): Return a new, empty priority queue (i.e., an emptylist)
"""
# empty priority que is just an empty list
def createEmptyPQ():
    return []
def left(i):
    return 2*i +1

def right(i):
    return 2*i+2
def parent(i):
    return(i-1)//2


def min_heapify(A,i):
    # calculate index of left and right child
    l = left(i)
    #print("l",l, "with value", A[l]) 
    r = right(i)
    #print("r",r, "with value", A[r])
    heap_size = len(A)
    # check that the index found is with in bound and that if the value of the left child is less than value of i.
    if l < heap_size and A[l] < A[i]:
        print("if left side value", A[l], "is less than value", A[i])
        smallest = l
        print("set smallest to", l)
    else:
        smallest = i
        print("else smallest is", i)
    # no matter what smallest hold the smallest value and compare with the value of the right child
    if r < heap_size and A[r]<A[smallest]:
        print("if right side value", A[r], "is less than smallest value", A[smallest])
        smallest = r
    # if the smallest is not the inserted node, we made a change and neep to heapify again
    if smallest != i:
        print("if smallest isn't index", i)
        A[i], A[smallest] = A[smallest], A[i]
        print("change place between",A[i], "and ", A[smallest])
        print("A and smallest",A, smallest)
        min_heapify(A,smallest)

A = [10, 7, 8, 3, 5, 20, 12,2,1]

def build_min_heap(A):
    heap_size = len(A)
    # round down and count down 0 (-1 is excluded)
    for i in range(heap_size // 2 - 1, -1, -1):
        print(i)
        min_heapify(A,i)
build_min_heap(A)
print(A)

def min_heap_min(A):
    return A[0]

def min_heap_extract_min(A):
    minimum = min_heap_min(A)
    print("length of array", len(A))
    #remove last element and make it the first(shift all elements would take longer) 
    A[0] = A.pop() #
    print("new length of array", len(A))
    #Run min heap from the top
    min_heapify(A,0)
    return minimum
#print(min_heap_extract_min(A))
#print(A)
def min_heap_insert(A,e):
    A.append(e)
    i = len(A)-1

    # while not the root and parant bigger than current node
    while i > 0 and A[parent(i)] > A[i]:
        A[i], A[parent(i)] = A[parent(i)], A[i]
        i = parent(i)

print(A)
min_heap_insert(A,4)
print(A)