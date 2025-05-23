# This is a simple implementation of a binary search tree (BST) in Python.
class BinNode:
    def __init__(self, key):
        self.key = key
        # when we make a node in the beginning they have no children
        self.left = None 
        self.right = None


class DictBinTree:
    def __init__(self):
        self.root = None

    def search(self, k):
        if self.root is None:
            return False
        # if there's an element, call '_search'
        else:
            return self._search(self.root,k)

    # private search method (recursive)
    # x is current node and k is the key to search for
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
        # what every _insert returns becomes the root. 
        self.root = self._insert(self.root, k)

    # x is the current node and k is the key to insert
    # We recursively walk through the tree to find the right place for the new key
    # We walk until we find a None node, with the proper tree walk, and insert the new key there
    def _insert(self, x, k):
        #base case
        if x is None:
            # make it a new node with the key k
            return BinNode(k)
        #Recurse into the left subtree
        if k < x.key:
            # compare to the left children
            x.left = self._insert(x.left, k)
        #Recurse into the right subtree
        else:
            # compare with the right children
            x.right = self._insert(x.right, k)
        # return the parent every time
        return x

    # Returns an ordered list of the keys in the tree
    def orderedTraversal(self):
        orded_list = []
        # start the tree walk from the root and with an empty list
        self._inorder_tree_walk(self.root, orded_list)
        return orded_list

    # x is the current node and result is the list to store the keys
    def _inorder_tree_walk(self, x, result):
        # check if x is not None (base case), if so call the function recursively
        if x:
            # go all the way to the left, here is the smallest. 
            self._inorder_tree_walk(x.left, result)
            result.append(x.key)
            # the right subtree is the next smallest, so go there
            self._inorder_tree_walk(x.right, result)
