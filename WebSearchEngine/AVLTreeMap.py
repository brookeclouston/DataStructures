"""
Author: Brooke Clouston
Date Created: March 11 2019

This script implements a basic Node class and an AVL Tree class consisting of a basic AVL Tree structure with the
additional get and searchPath methods. This class was created in response to part 1.2 of Assignment 3 of CISC235
Winter 2019. Inspiration for AVL Tree implementation came from https://www.youtube.com/watch?v=lxHF-mVdwK8.
"""


class Node:
    # node class that contains the basic information about a node in the AVL tree

    def __init__(self, key=None, value=None):
        # class constructor
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1


class AVLTreeMap:
    # class that implements AVL Tree

    def __init__(self):
        # class constructor
        self.root = None

    def put(self, key, value):
        # checks to make sure the tree is not empty and calls on actual put function
        if self.root is None:
            self.root = Node(key, value)
        else:
            self.Put(key, value, self.root)

    def Put(self, key, value, current):
        # inserts a new node into the AVL tree by using a basic binary tree implementation but calling on addition check
        # helper functions to ensure AVL Tree properties are preserved
            if key < current.key:  # inserting into left subtree
                if current.left is None:
                    current.left = Node(key, value)
                    current.left.parent = current
                    self.check(current.left)  # checking tree
                else:
                    self.Put(key, value, current.left)
            elif key > current.key:  # inserting into right subtree
                if current.right is None:
                    current.right = Node(key, value)
                    current.right.parent = current
                    self.check(current.right)  # checking tree
                else:
                    self.Put(key, value, current.right)
            else:
                current.value = value  # updating an existing node with a new value

    def get(self, key):
        # checks to make sure the tree is not empty and calls on actual get function
        if self.root is not None:
            return self.Get(key, self.root)
        else:
            return None

    def Get(self, key, current):
        # searches the recursively for a given key, if found then the value is returned, if not found None is returned
        if key == current.key:
            return current.value
        elif key < current.key:
            if current.left is None:
                return None
            return self.Get(key, current.left)
        elif key > current.key:
            if current.right is None:
                return None
            return self.Get(key, current.right)

    def searchPath(self, key):
        # checks to make sure the tree is not empty and calls on actual searchPath function
        if self.root is not None:
            return self.SearchPath(key, self.root)
        else:
            return None

    def SearchPath(self, key, current):
        # searches tree for key making a list of nodes visited on search path, if key is found list is returned
        search_path = []
        while current is not None:
            if key == current.key:
                return search_path + [key]
            elif key < current.key:
                search_path.append(current.key)
                current = current.left
            else:
                search_path.append(current.key)
                current = current.right
        return None

    def getHeight(self, current):
        # returns the current nodes height
        if current is None:
            return 0
        return current.height

    def check(self, current, searchPath=[]):
        # checks heights of subtrees to ensure a difference of no more than 1, if they do then tree is rebalanced
        if current.parent is None:
            return
        searchPath = [current] + searchPath  # creates a list of problem nodes, 3 at a time
        leftHeight = self.getHeight(current.parent.left)
        rightHeight = self.getHeight(current.parent.right)
        if abs(leftHeight-rightHeight) > 1:
            searchPath = [current.parent] + searchPath
            self.rebalance(searchPath[0], searchPath[1], searchPath[2])  # rebalanced nodes 3 at a time
            return

    def rebalance(self, a, b, c):
        # checks for the 4 cases in which an AVL tree would need to be rebalanced between 3 nodes
        if b == a.left and c == b.left:  # a left-left rotation is needed
            self.rightRotate(a)
        elif b == a.left and c == b.right:  # a left-right rotation is needed
            self.leftRotate(b)
            self.rightRotate(a)
        elif b == a.right and c == b.right:  # a right-left rotation is needed
            self.leftRotate(a)
        elif b == a.right and c == b.left:  # a right-right rotation is needed
            self.rightRotate(b)
            self.leftRotate(a)

    def rightRotate(self, node):
        # right rotation is performed where tree with a left child and left grandchild is transformed into a root
        # node with a right and left child
        pivot = node.parent
        b = node.left
        c = b.right
        b.right = node
        node.parent = b
        node.left = c
        if c is not None:
            c.parent = node
        b.parent = pivot
        if b.parent is None:
            self.root = b
        else:
            if b.parent.left == node:
                b.parent.left = b
            else:
                b.parent.right = b
        # updating heights of nodes
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        b.height = 1 + max(self.getHeight(b.left), self.getHeight(b.right))

    def leftRotate(self, node):
        # left rotation is performed where a tree with a right child and a right grandchild is transformed into a root
        # not with a right and left child
        pivot = node.parent
        b = node.right
        c = b.left
        b.left = node
        node.parent = b
        node.right = c
        if c is not None:
            c.parent = node
        b.parent = pivot
        if b.parent is None:
            self.root = b
        else:
            if b.parent.left == node:
                b.parent.left = b
            else:
                b.parent.right = b
        # updating heights of node
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        b.height = 1 + max(self.getHeight(b.left), self.getHeight(b.right))
