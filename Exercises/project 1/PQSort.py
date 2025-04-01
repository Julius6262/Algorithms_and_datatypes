import sys
import PQHeap

pq = PQHeap.createEmptyPQ()

n = 0
for line in sys.stdin:
    PQHeap.insert(pq,int(line))
    n = n+1

print()
while n > 0:
    print(PQHeap.extractMin(pq))
    n = n-1

"""import sys
from PQHeap1 import Heap

PQHeap = Heap()

pq = PQHeap.createEmptyPQ()

n = 0
for line in sys.stdin:
    PQHeap.min_heap_insert(pq,int(line))
    n = n+1

print()
while n > 0:
    print(PQHeap.min_heap_extract_min(pq))
    n = n-1"""
