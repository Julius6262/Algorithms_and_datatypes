# ========== working code that match Encode ========== #
import sys
from bitIO import BitReader
import PQHeap
from Element import Element

BYTES_BY_INTEGER = 256

class HuffmanNode:
    def __init__(self, byte=None, left=None, right=None):
        self.byte = byte
        self.left = left
        self.right = right

    # return true if it has no children, must be a leaf node
    def is_leaf(self):
        return self.left is None and self.right is None

def rebuild_tree(freq_table):
    # start by building the tree using a priority queue
    pq = PQHeap.createEmptyPQ()
    # create a leaf node for each byte 
    for i in range(BYTES_BY_INTEGER):
        node = HuffmanNode(byte=i)
        # Insert a HuffmanNode for byte value i into the priority queue.
        # Each Element is prioritized by (frequency, byte value) to ensure
        # consistent tie-breaking when frequencies are equal cause of tuple
        # The first element of the tuple is the frequency, and the second is the byte value.
        PQHeap.insert(pq, Element((freq_table[i], i), node))

    # if we only have one byte, we need to add a dummy node
    if len(pq) == 1:
        only = PQHeap.extractMin(pq)
        # Byte 256 is dummy and unused cause of 0-255 for bytes
        dummy = HuffmanNode(byte=BYTES_BY_INTEGER)
        # Create a parent node with the only node and the dummy node as children
        # The parent node has a byte value of -1 to indicate it's not a leaf.  
        parent = HuffmanNode(byte=-1, left=only.data, right=dummy)
        # Insert the new parent node back into the priority queue 
        PQHeap.insert(pq, Element((only.key[0], BYTES_BY_INTEGER), parent))

    while len(pq) > 1:
        #extract the two elements with the smallest frequencies (priorities) from the PQ.
        e1 = PQHeap.extractMin(pq)
        e2 = PQHeap.extractMin(pq)
        # Create a new parent node (internal node)
        # Internal nodes have byte = -1
        # The two extracted nodes become the left and right childre
        parent = HuffmanNode(byte=-1, left=e1.data, right=e2.data)
        # Calculate the combined frequency for the new parent
        combined_freq = e1.key[0] + e2.key[0]
        # - Take the minimum byte value of the two children
        # - Ensures consistent order when combining nodes with equal frequency
        tiebreaker = min(e1.key[1], e2.key[1])
        # Insert the new parent node back into the priority queue
        PQHeap.insert(pq, Element((combined_freq, tiebreaker), parent))
    # Once the loop finishes, there's one element left — the root of the full Huffman tree
    root = PQHeap.extractMin(pq).data
    return root

    return PQHeap.extractMin(pq).data

def decode(input_filename, output_filename):
    # Open the input file in binary mode for reading
    with open(input_filename, "rb") as f_in:
        # bitreader class to read the bits from the file
        reader = BitReader(f_in)
        # read bytes form the file and store them in a frequency table
        freq_table = [reader.readint32bits() for _ in range(BYTES_BY_INTEGER)] # runs 256 times
        # This tells us exactly how many bytes the decoder needs to write to the output file
        total_bytes = sum(freq_table)

        # Handle empty file case
        # If the total bytes to write is 0, we can just create an empty file
        if total_bytes == 0:
            with open(output_filename, "wb") as f_out:
                return

        root = rebuild_tree(freq_table)
        # open output file in write binary mode so we can write bytes to it
        with open(output_filename, "wb") as f_out:
            count = 0
            # start at the root of the tree
            node = root
            # Read and decode bits until all original bytes are written
            while count < total_bytes:
                # move in the tree based on the bit read
                bit = reader.readbit()
                node = node.left if bit == 0 else node.right
                # safety check: If the tree traversal goes wrong, raise an error instead of crashing silently
                if node is None:
                    raise ValueError("Reached None during tree traversal")
                # if we reached a leaf node, and the byte is in the range 0-255 (internal nodes have byte = -1)
                if node.is_leaf() and 0 <= node.byte < BYTES_BY_INTEGER:
                    # Writes the decoded byte to the output file.
                    f_out.write(bytes([node.byte]))
                    count += 1
                    # Resets decoding traversal to the root of the Huffman tree to process the next set of bits
                    node = root
        reader.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Running Decode.py - Usage: python Decode.py inputFile outputFile")
        sys.exit(1)
    decode(sys.argv[1], sys.argv[2])

# ========= Old code that match on of the old solutions for encode ========= #
"""import sys
import PQHeap
from Element import Element
from bitIO import BitReader

class HuffmanNode:
    def __init__(self, byte=None, freq=0, left=None, right=None):
        self.byte = byte      # -1 for internal node, 0–255 for leaf
        self.freq = freq      # only used during tree building
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_table):
    pq = PQHeap.createEmptyPQ()

    for i in range(256):
        if freq_table[i] > 0:
            leaf = HuffmanNode(byte=i)
            PQHeap.insert(pq, Element(freq_table[i], leaf))

    if len(pq) == 0:
        raise ValueError("Frequency table contains no non-zero frequencies.")

    if len(pq) == 1:
        only_elem = PQHeap.extractMin(pq)
        dummy = HuffmanNode(byte=-1)
        parent = HuffmanNode(byte=-1, left=only_elem.data, right=dummy)
        PQHeap.insert(pq, Element(only_elem.key, parent))

    while len(pq) > 1:
        e1 = PQHeap.extractMin(pq)
        e2 = PQHeap.extractMin(pq)
        parent = HuffmanNode(byte=-1, left=e1.data, right=e2.data)
        PQHeap.insert(pq, Element(e1.key + e2.key, parent))

    return PQHeap.extractMin(pq).data

def decode(compressed_filename, output_filename):
    with open(compressed_filename, "rb") as fin, open(output_filename, "wb") as fout:
        reader = BitReader(fin)

        # Step 1: Read the frequency table (256 × 4 = 1024 bytes)
        freq_table = [reader.readint32bits() for _ in range(256)]
        total_bytes_to_write = sum(freq_table)

        # Handle empty file case
        if total_bytes_to_write == 0:
            print("File is empty — nothing to decode.")
            reader.close()
            return
        # Step 2: Rebuild the Huffman tree
        root = build_huffman_tree(freq_table)

        written = 0
        node = root

        while written < total_bytes_to_write:
            bit = reader.readbit()
            if bit == 0:
                node = node.left
            else:
                node = node.right

            if node.byte >= 0:
                # Leaf node: write byte to output
                fout.write(bytes([node.byte]))
                written += 1
                node = root  # restart from root for next byte

        reader.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Decode.py compressedFile outputFile")
        sys.exit(1)

    compressed_file = sys.argv[1]
    output_file = sys.argv[2]

    decode(compressed_file, output_file)"""