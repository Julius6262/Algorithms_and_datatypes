# Eksempelprogram, som viser brugen af Element sammen med PQHeap.py fra del I.

import sys
import PQHeap # Dette er gruppens PQHeap.py fra del I.
from Element import Element

pq = PQHeap.createEmptyPQ() # Opret en tom prioritetskø.

for line in sys.stdin:
    # Man opretter et nyt element med kaldet Element(key,data), som
    # sætter værdier i dets felter key og data. Dette vises her med et
    # heltal som key og en tilfældig string som data. I del III skal
    # data i stedet være træer (se projektbeskrivelsen for del III).
    e = Element(int(line),"Some appropriate data")
    # Indsæt det nye Element i prioritetskøen.
    PQHeap.insert(pq,e)

while len(pq) > 0:
    # Udtag det Element fra prioritetskøen, som har mindste key.
    e = PQHeap.extractMin(pq)
    # Tilgå og print dets felter key og data.
    extractedKey = e.key
    extractedData = e.data
    print(extractedKey)
    print(extractedData)
