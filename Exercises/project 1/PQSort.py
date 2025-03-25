import sys
from PQHeap import Heap

def pq_sort():
    H = Heap()  # Create an instance of the Heap class
    pq = H.createEmptyPQ()  # Get an empty list
    pq = [0]
    for line in sys.stdin:
        try:
            number = int(line.strip())
            H.min_heap_insert(pq, number)  # Call the method on the instance H
        except ValueError:
            pass

    while pq:
        minimum = H.min_heap_extract_min(pq)
        print(minimum)

if __name__ == "__main__":
    pq_sort()