
#must implement the data structure binary search tree with numbers as keys

"""class BinNode:
    def __init__(self,key):
        self.key = key
        self.leftchild = None
        self.rightchild = None
        self.parent = None
# New trees are created with a call DictBinTree(), which should return an empty tree.
class DictBinTree:
    def __init__(self):
        self.root = None
    #returns a Boolean indicating whether the key k is in the tree T
    def search(self,x,k):
        if x == None or k == x.key:
            return x
        if k < x.key:
            return self.search(x.leftchild, k)
        else:
            return self.search(x.rightchild, k)
    # inserts the key k in the tree T
    # k 
    def insert(self, T, k):
        x = T.root
        y = None # will be the parent of k
        while x != None: # descend until reaching a leaf
            y = x
            if k.key < x.key:
                x = x.leftchild
            else:
                x = x.rightchild
        k.parent = y # found the location4insert k with parent y
        if y == None:
            T.root = k # tree T was empty
        elif k.key < y.key:
            y.leftchild = k
        else:
            y.rightchild = k

        
    #returns a list of the keys in the tree T in sorted order (rather than printing them to the screen as in the
    #book's pseudo-code)
    # Inorder_tree_walk
    def orderedTraversal(self,x, result=None):
        # first time create the result list
        if result == None:
            result = []
        if x != None:
            self.orderedTraversal(x.leftchild, result)
            result.append(x.key)
            self.orderedTraversal(x.rightchild, result)
        return result"""

# DictBinTree.py

# DictBinTree.py

class BinNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class DictBinTree:
    def __init__(self):
        self.root = None

    def search(self, k):
        return self._search(self.root, k)

    # Internal search method (recursive)
    def _search(self, x, k):
        if x is None:
            return False  # Return False if the node is not found
        if k == x.key:
            return True  # Return True if the key matches
        elif k < x.key:
            return self._search(x.left, k)  # Search in the left subtree
        else:
            return self._search(x.right, k)  # Search in the right subtree

    def insert(self, k):
        self.root = self._insert(self.root, k)

    def _insert(self, x, k):
        if x is None:
            return BinNode(k)
        if k < x.key:
            x.left = self._insert(x.left, k)
        else:
            x.right = self._insert(x.right, k)
        return x

    def orderedTraversal(self):
        orded_list = []
        self._inorder_tree_walk(self.root, orded_list)
        return orded_list

    def _inorder_tree_walk(self, x, result):
        if x:
            self._inorder_tree_walk(x.left, result)
            result.append(x.key)
            self._inorder_tree_walk(x.right, result)


# running only in the DictBinTree.py file, not if the file is imported
# Testing the DictBinTree class
if __name__ == "__main__":
    def test_dict_bin_tree():
        # Create an instance of the binary search tree
        tree = DictBinTree()

        sorted_keys = tree.orderedTraversal()
        print(sorted_keys)

        # Test: Insert values into the tree
        tree.insert(10)
        tree.insert(5)
        tree.insert(15)
        tree.insert(3)
        tree.insert(7)
        tree.insert(13)
        tree.insert(18)

        # Test: orderedTraversal should return the keys in sorted order
        print("Ordered Traversal (in sorted order):")
        sorted_keys = tree.orderedTraversal()
        print(sorted_keys)  # Expected: [3, 5, 7, 10, 13, 15, 18]

        # Test: Search for a key that is present in the tree
        print("\nSearch for key 7:")
        search_result = tree.search(7)
        print(search_result)  # Expected: True

        # Test: Search for a key that is not in the tree
        print("\nSearch for key 20:")
        search_result = tree.search(20)
        print(search_result)  # Expected: False

        # Test: Search for another key that is present in the tree
        print("\nSearch for key 13:")
        search_result = tree.search(13)
        print(search_result)  # Expected: True

        # Test: Search for key 10 (the root node)
        print("\nSearch for key 10 (root):")
        search_result = tree.search(10)
        print(search_result)  # Expected: True

# Run the test
#test_dict_bin_tree()


# calls on an object T
#T = T.DictBinTree()
# running only in the DictBinTree.py file, not if the file is imported
"""if __name__ == "__main__":
    tree = DictBinTree()
    # set the key of each node, and insert the node on the tree
    tree.insert(tree, BinNode(10))
    tree.insert(tree, BinNode(5))
    tree.insert(tree, BinNode(15))
    tree.insert(tree, BinNode(7))
    tree.insert(tree, BinNode(8))
    tree.insert(tree, BinNode(1))

    print("In-order:", tree.orderedTraversal(tree.root))  # ➜ [5, 7, 10, 15]"""