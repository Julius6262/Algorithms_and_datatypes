
# ====== working code =====
import sys
import PQHeap
from Element import Element
from bitIO import BitWriter
BYTES_BY_INTEGER = 256

class HuffmanNode:
    def __init__(self, byte=None, left=None, right=None):
        self.byte = byte
        self.left = left
        self.right = right
    # return true if it has no children, must be a leaf node
    def is_leaf(self):
        return self.left is None and self.right is None

def count_frequencies(filename):
    # Initialize a list of size 256 to hold frequency counts for each byte value
    freq_list = [0] * BYTES_BY_INTEGER
    # open inputfile in read binary mode (first time)
    with open(filename, "rb") as f:
        while True:
            # read one byte at a time
            # read(1) returns a bytes object of length 1 fx b'a'
            byte_obj = f.read(1)
            # if no more bytes to read, read(1) returns 0, and we break the loop
            if not byte_obj:
                break
            # acess the first byte of the bytes object to get the integer value in the range 0-255
            # increment the frequency count for that byte
            freq_list[byte_obj[0]] += 1
    return freq_list

def build_huffman_tree(freq_table):
    # start by building the tree using a priority queue
    pq = PQHeap.createEmptyPQ()
    for i in range(BYTES_BY_INTEGER):
        # create a leaf node for each byte 
        node = HuffmanNode(byte=i)
        # Insert a HuffmanNode for byte value i into the priority queue.
        # Each Element is prioritized by (frequency, byte value) to ensure
        # consistent tie-breaking when frequencies are equal cause of tuple
        # The first element of the tuple is the frequency, and the second is the byte value.
        PQHeap.insert(pq, Element((freq_table[i], i), node))

    ## if we only have one byte, we need to add a dummy node
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

# This function recursively traverses the Huffman tree to generate the bit string for each byte (character)
# node is current node, path is the current bit string, table is the list to store the codes
def generate_code_table(node, path="", table=None):
    # If the table dont exist, we create a new one, this will happen on first call
    if table is None:
        table = [""] * BYTES_BY_INTEGER # 256 possible byte values
    # if we reached a leaf node, and the byte is in the range 0-255 (internal nodes have byte = -1)
    if node.is_leaf() and 0 <= node.byte < BYTES_BY_INTEGER:
        # Assign the bit string to the corresponding index in the table
        table[node.byte] = path # fx tfor 'a' table[97] = "010"
    # since we are not in a leaf node, we need to go deeper in the tree
    # we add a 0 for left and a 1 for right
    else:
        if node.left:
            generate_code_table(node.left, path + "0", table)
        if node.right:
            generate_code_table(node.right, path + "1", table)
    # The table will be filled with the bit strings for each byte value
    return table

# This function encodes the input file using Huffman coding and writes the encoded data to the output file
# This function is the functions that combines all the other functions, and passes the correct parameters
def encode(input_filename, output_filename):
    # explanation of these methods can be found in the comments of the methods
    freq_table = count_frequencies(input_filename)
    root = build_huffman_tree(freq_table)
    code_table = generate_code_table(root)
    # open output file in write binary mode so we can write bytes to it
    with open(output_filename, "wb") as f_out:
        # Bitwriter class that handles writing bits to the output file
        writer = BitWriter(f_out)
        # Each of the 256 frequencies is written as a 32-bit integer
        for freq in freq_table:
            writer.writeint32bits(freq)

        bit_count = 0
        # open inputfile in read binary mode (second time)
        with open(input_filename, "rb") as f_in:
            while True:
                # Read one byte at a time
                byte_obj = f_in.read(1)
                # Stop if end of file 
                if not byte_obj:      
                    break
                # Look up Huffman code for the byte value (0–255)
                code = code_table[byte_obj[0]]  
                # Each code is a string like '010'
                for bit in code:
                    # Write each character as an integer bit (0 or 1)                
                    writer.writebit(int(bit))   
                    # Keep track of how many bits i’ve written
                    bit_count += 1              

        # Pad to byte boundary
        # A file on disk can only be saved in full bytes (8 bits). So if my total Huffman bitstream isn't divisible by 8 
        # # fx it ends at 101) pad it with 0s until the final byte is complete (fx 10100000).
        bits_left = (8 - (bit_count % 8)) % 8
        for _ in range(bits_left):
            writer.writebit(0)
        writer.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Running Encode.py - Usage: python Encode.py inputFile outputFile")
        sys.exit(1)
    encode(sys.argv[1], sys.argv[2])


# ====== old code that encodes but does not pad ===== #


"""
import sys
import PQHeap
from Element import Element
from bitIO import BitWriter

def count_frequencies(filename):
    freq = [0] * 256
    with open(filename, "rb") as f:
        while True:
            byte = f.read(1)
            if not byte:
                break
            freq[byte[0]] += 1
    return freq

class HuffmanNode:
    def __init__(self, byte=None, freq=0, left=None, right=None):
        self.byte = byte  # byte >= 0 for leaf, -1 for internal
        self.freq = freq  # not used in encoding, just for building
        self.left = left
        self.right = right
    # less than method atuomatically called by the priority queue to compare elements
    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(freq_table):
    # priority queue will hold nodes of the Huffman tree, prioritized by their frequency.
    pq = PQHeap.createEmptyPQ()

    for i in range(256):
        # Create a leaf node for each byte with non-zero frequency
        if freq_table[i] > 0:
            leaf = HuffmanNode(byte=i)
            PQHeap.insert(pq, Element(freq_table[i], leaf))

    if len(pq) == 0:
        raise ValueError("Frequency table contains no non-zero frequencies.")
    # handle the case where there is only one unique byte in the file
    # create a dummy node to ensure the tree has two children
    if len(pq) == 1:
        only_elem = PQHeap.extractMin(pq)
        dummy = HuffmanNode(byte=-1)
        parent = HuffmanNode(byte=-1, left=only_elem.data, right=dummy)
        PQHeap.insert(pq, Element(only_elem.key, parent))
    #main loop of the Huffman algorithm's tree building process.
    while len(pq) > 1:
        # Extract the two elements with the smallest frequencies (priorities) from the PQ.
        # These represent the two trees with the lowest value currently.
        e1 = PQHeap.extractMin(pq)
        e2 = PQHeap.extractMin(pq)
        # Create a new internal node in the Huffman tree.
        # This node will be the parent of the two trees extracted (e1.data and e2.data).
        parent = HuffmanNode(byte=-1, left=e1.data, right=e2.data)
        # Create a new Element to represent this newly merged tree in the priority queue.
        # The key (priority) of this new element is the sum of the frequencies of its two children.
        # Insert the new Element back into the PQ.
        PQHeap.insert(pq, Element(e1.key + e2.key, parent))
    # When the while loop finishes, there is only one element left in the priority queue.
    # This final element contains the root node of the complete Huffman tree
    return PQHeap.extractMin(pq).data

def generate_code_table(node, path="", table=None):
    if table is None:
        table = [""] * 256
    # base case: if node is None, return the table
    if node is None:
        return table
    # internal nodes have byte = -1, leaf nodes have byte >= 0
    if node.byte >= 0:
        # assign bit code to corresponding index in the table list fx a = table[97] = "010"
        table[node.byte] = path
    else:
        # get the correct bits for left and right children, build path recursively
        generate_code_table(node.left, path + "0", table) 
        generate_code_table(node.right, path + "1", table)
    
    return table

def print_tree(node, prefix=""):
    if node is None:
        return
    if node.left is None and node.right is None:
        char = chr(node.byte) if 32 <= node.byte <= 126 else repr(chr(node.byte))
        print(f"{prefix}─ {char} (ASCII: {node.byte})")
    else:
        print(f"{prefix}─ *")
        print_tree(node.left, prefix + "  0")
        print_tree(node.right, prefix + "  1")

def encode(input_filename, output_filename):
    # Step 1: Count frequencies
    freq_table = count_frequencies(input_filename)

    # Try building Huffman tree only if there are bytes
    has_content = sum(freq_table) > 0
    if has_content:
        root = build_huffman_tree(freq_table)
        code_table = generate_code_table(root)
    else:
        root = None
        code_table = None

    # Step 4 & 5: Write frequency table and encoded content to output
    with open(output_filename, "wb") as fout:
        writer = BitWriter(fout)

        # Write 256 frequencies as 32-bit ints
        for freq in freq_table:
            writer.writeint32bits(freq)

        # Write encoded content only if file had data
        if has_content:
            with open(input_filename, "rb") as fin:
                while (byte := fin.read(1)):
                    code = code_table[byte[0]]
                    for bit in code:
                        writer.writebit(int(bit))

        writer.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Encode.py inputFile outputFile")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    encode(input_file, output_file)"""






# ====== Old code that has the right length not does not decode correctly ===== #
"""import sys
import PQHeap
from Element import Element
from bitIO import BitWriter

class HuffmanNode:
    def __init__(self, byte=-1, left=None, right=None):
        self.byte = byte  # -1 for internal nodes, 0-255 for leaves
        self.left = left
        self.right = right

def count_frequencies(filename):
    freq = [0] * 256
    try:
        with open(filename, "rb") as f:
            while True:
                byte = f.read(1)
                if not byte:  # Proper EOF detection
                    break
                freq[byte[0]] += 1
    except IOError:
        pass  # File is empty or doesn't exist
    return freq

def build_huffman_tree(freq_table):
    pq = PQHeap.createEmptyPQ()
    
    # Insert all 256 possible bytes (including zero frequencies)
    for byte in range(256):
        node = HuffmanNode(byte=byte)
        PQHeap.insert(pq, Element(freq_table[byte], node))
    
    # Special case: empty file or all zeros
    if all(f == 0 for f in freq_table):
        # Create two dummy nodes to satisfy Huffman algorithm requirements
        dummy1 = HuffmanNode(byte=0)
        dummy2 = HuffmanNode(byte=1)
        PQHeap.insert(pq, Element(0, dummy1))
        PQHeap.insert(pq, Element(0, dummy2))

    # Build Huffman tree
    while len(pq) > 1:
        left = PQHeap.extractMin(pq)
        right = PQHeap.extractMin(pq)
        internal_node = HuffmanNode(left=left.data, right=right.data)
        PQHeap.insert(pq, Element(left.key + right.key, internal_node))
    
    return PQHeap.extractMin(pq).data

def build_codebook(root):
    codebook = [""] * 256
    
    def traverse(node, code):
        if node.byte != -1:  # Leaf node
            codebook[node.byte] = code
        else:  # Internal node
            traverse(node.left, code + "0")
            traverse(node.right, code + "1")
    
    traverse(root, "")
    return codebook

def encode_file(input_filename, output_filename):
    # 1. Get frequency table (will be all zeros for empty file)
    freq_table = count_frequencies(input_filename)
    
    # 2. Build Huffman tree (handles empty case)
    huffman_tree = build_huffman_tree(freq_table)
    
    # 3. Generate codebook
    codebook = build_codebook(huffman_tree)
    
    # 4. Write to output file
    with open(output_filename, 'wb') as output_file:
        bit_writer = BitWriter(output_file)
        
        # Always write frequency table (256 32-bit integers = 1024 bytes)
        for freq in freq_table:
            bit_writer.writeint32bits(freq)
        
        # Only attempt to encode content if file is not empty
        try:
            with open(input_filename, 'rb') as input_file:
                while True:
                    byte = input_file.read(1)
                    if not byte:
                        break
                    byte_value = byte[0]
                    code = codebook[byte_value]
                    for bit in code:
                        bit_writer.writebit(int(bit))
        except IOError:
            pass  # File is empty
        
        bit_writer.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python Encode.py inputFile outputFile")
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    encode_file(input_filename, output_filename)

if __name__ == "__main__":
    main()
"""
