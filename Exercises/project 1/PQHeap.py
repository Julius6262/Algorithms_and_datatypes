
class Heap():

    # empty priority que is just an empty list
    @staticmethod
    def createEmptyPQ():
        return []
    @staticmethod
    def left(i):
        return 2*i +1
    @staticmethod
    def right(i):
        return 2*i+2
    @staticmethod
    def parent(i):
        return(i-1)//2

    def min_heapify(self,A,i):
        # calculate index of left and right child
        l = self.left(i)
        #print("l",l, "with value", A[l]) 
        r = self.right(i)
        #print("r",r, "with value", A[r])
        heap_size = len(A)
        # check that the index found is with in bound and that if the value of the left child is less than value of i.
        if l < heap_size and A[l] < A[i]:
            smallest = l
        else:
            smallest = i
        # no matter what smallest hold the smallest value and compare with the value of the right child
        if r < heap_size and A[r]<A[smallest]:
            smallest = r
        # if the smallest is not the inserted node, we made a change and neep to heapify again
        if smallest != i:
            A[i], A[smallest] = A[smallest], A[i]
            self.min_heapify(A,smallest)


    def build_min_heap(self,A):
        heap_size = len(A)
        # round down and count down 0 (-1 is excluded)
        for i in range(heap_size // 2 - 1, -1, -1):
            print(i)
            self.min_heapify(A,i)

    def min_heap_min(self,A):
        return A[0]


    def min_heap_extract_min(self,A):
        if len(A) <1:  # Prevent extracting from an empty heap
            print("The que is empty")
            return
        minimum = self.min_heap_min(A)

        if len(A) == 1:
            A.pop()
        else:
            #remove last element and make it the first(shift all elements would take longer) 
            A[0] = A.pop()  #
            #Run min heap from the top
            self.min_heapify(A,0)
        return minimum

    def min_heap_insert(self,A,e):
        A.append(e)
        i = len(A)-1
        # while not the root and parant bigger than current node
        while i > 0 and A[self.parent(i)] > A[i]:
            A[i], A[self.parent(i)] = A[self.parent(i)], A[i]
            i = self.parent(i)
