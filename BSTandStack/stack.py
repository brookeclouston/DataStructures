"""
Date Created: February 6 2019
Author: Brooke Clouston

This script was created to implement the class Stack which is a representation of the functional stack object. This
script is in response to Assignment 2 of CISC235 Winter 2019.
"""


class Stack:

    def __init__(self):
        # Initializing stack
        self.stack = []

    def isEmpty(self):
        # Checks if stack is empty by looking at size of stack
        if self.size() == 0 or (self is None):
            return True
        return False

    def push(self, item):
        # Adds an item to the beginning of the stack
        self.stack.append(item)

    def pop(self):
        # Removes and returns the first element from the stack
        if self.isEmpty():
            return None
        return self.stack.pop()

    def size(self):
        # Returns the number of elements in the stack
        return len(self.stack)