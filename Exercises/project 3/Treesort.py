# Treesort.py
import sys
from DictBinTree import DictBinTree

def treesort():
    tree = DictBinTree()
    # Read integers from stdin
    for line in sys.stdin:
        line = line.strip()
        if line:  # Ignore empty lines
            try:
                number = int(line)
                tree.insert(number)
            except ValueError:
                print(f"Invalid input: {line}", file=sys.stderr)

    # Perform the in-order traversal and print sorted numbers
    for key in tree.orderedTraversal():
        print(key)

if __name__ == "__main__":
    treesort()
