"""
Date Created: February 6 2019
Author: Brooke Clouston

This script was created to implement the class BinarySearchTree which is a representation of a binary tree object. This
script is in response to Assignment 2 of CISC235 Winter 2019.
"""

from stack import Stack


class BinarySearchTree:

    def __init__(self, value=None):
        # Initializes the tree with a value node, a left child and a right child
        self.leftChild = None
        self.rightChild = None
        self.value = value

    def __str__(self):
        # Helper function to display tree nicely
        return "%s: [%s, %s]" % (str(self.value), self.leftChild, self.rightChild)

    def insert(self, value):
        # Inserts a new node into the BST
        if self is None:  # Checks if tree is empty
            self.value = value
        elif value <= self.value:  # If the value is less than or equal to the current node, moves left
            if self.leftChild is None:
                self.leftChild = BinarySearchTree(value)  # Recursively calls insert function until a leaf is reached
            else:
                self.leftChild.insert(value)
        elif value > self.value:  # If the value is greater than the current node, move right
            if self.rightChild is None:
                self.rightChild = BinarySearchTree(value)  # Recursively calls insert function until a leaf is reached
            else:
                self.rightChild.insert(value)


    def searchPath(self, targetValue):
        # Returns a list of all the values visited while searching for a target value
        search_path = []
        while self is not None:
            if targetValue == self.value:
                return search_path + [targetValue]
            elif targetValue < self.value:
                search_path.append(self.value)
                self = self.leftChild
            else:
                search_path.append(self.value)
                self = self.rightChild
        return "%d is not in this binary search tree" % targetValue # Returns if target value is not found

    def getTotalDepth(self, depth=0):
        # Returns the sum of all of the depths of the nodes in the tree using recursion and working from top down
        left, right = 0, 0
        if self is None:
            return 0
        if self.leftChild is not None:  # Traversing left subtree and adding 1 to total depth
            left = self.leftChild.getTotalDepth(depth+1)
        if self.rightChild is not None:  # Traversing right subtree and adding 1 to total depth
            right = self.rightChild.getTotalDepth(depth+1)
        return left + depth + right  # Sums together the total depths

    def getWeightBalanceFactor(self, maximum=0, left=0, right=0):
        # Uses recursion to calculate the maximum value of the nodes in every subtree of the BST
        if self is None:  # Base case
            return 0
        if self.leftChild is not None:  # Searches left subtree and adds 1 to left counter and node depth value
            left = self.leftChild.getWeightBalanceFactor(maximum, (left + 1), right) + 1
        if self.rightChild is not None:  # Searches right subtree and adds 1 to left counter and node depth value
            right = self.rightChild.getWeightBalanceFactor(maximum, left, (right + 1)) + 1
        difference = abs(left - right)  # Determining the difference between the left and right subtrees
        if difference > maximum: # if the difference is greater than the current max value, the max is updated
            maximum = difference
        return maximum

    def loadTreeFromFile(self):
        # Reconstructs a tree from a text file using the helper class Stack
        binarySearchTree = Stack()
        with open("testTree.txt") as file:  # Gets a list containing only the elements in the txt file
            for level in file.readlines():
                nodeInfo = level.rstrip().split()
                # Formats the tags as ints and assigns variable names
                data, lc, rc = int(nodeInfo[0]), int(nodeInfo[1]), int(nodeInfo[2])
                if rc == 1:
                    right_tree = binarySearchTree.pop()
                if lc == 1:
                    left_tree = binarySearchTree.pop()
                newTree = BinarySearchTree(data)
                if rc == 1:
                    newTree.rightChild = right_tree
                else:
                    newTree.rightChild = None
                if lc == 1:
                    newTree.leftChild = left_tree
                else:
                    newTree.leftChild = None
                binarySearchTree.push(newTree)
        file.close()
        final_tree = binarySearchTree.pop()
        return final_tree
