"""
Author: Brooke Clouston
Date Created: March 14 2019

This class creates a MaxHeap implementation of a collection of instances of webPageIndexes by using an array based
list to hold the data items in a priority queue. This class was created in response to part 1.4 of Assignment 3 of
CISC235 Winter 2019.
"""
import string


class WebPagePriorityQueue:

    def __init__(self, query, webPageIndexes):
        # constructor which takes as input a query and a set of WebPageIndex instances
        self.query = query
        self.webPageIndexes = webPageIndexes
        self.heap = [[0, 0]]
        self.maxHeap = self.createHeap()

    def formatQuery(self):
        # formats the query into a list of lowercase words without punctuation
        queryList = []
        new = self.query.lower()  # makes each word lowercase
        queryList.append(new.translate(str.maketrans("", "", string.punctuation))) # strips punctuation
        return queryList[0].split()

    def createPriority(self, webPageIndex):
        # calculates the priority by summing the word count using the getCount method from the WebPageIndex class
        queryList = self.formatQuery()
        priority = 0
        for word in queryList:
            priority += webPageIndex.getCount(word)
        return priority

    def peek(self):
        # returns highest priority(largest value) item in the WebPagePriority without removing it
        return self.heap[1][1]

    def poll(self):
        # removes and returns the largest value item in the WebPagePriority queue
        poll = self.heap[1][1]
        del self.heap[1]
        return poll

    def reHeap(self, newQuery):
        # reheaps when given a new query by "resetting" initial conditions and recalling the heap building functions
        if newQuery == self.query:
            # if the new query is the same as the current one we do not have to reheap
            return
        self.heap = [[0, 0]]
        self.query = newQuery
        self.maxHeap = self.createHeap()
        return self.maxHeap

    def createHeap(self):
        # for every instance of a webPageIndex, its priority is first calculated then its priority and instance is
        # appended to the existing heap and reshuffled into its correct position
        for wpindex in self.webPageIndexes:
            priority = self.createPriority(wpindex)
            self.heap.append([priority, wpindex])  # adding to existing heap
            self.reshuffle(len(self.heap) - 1)  # calling on function to reshuffle
        return self.heap

    def reshuffle(self, index):
        # reshuffles based on the index
        parent = index//2
        if index <= 1:
            # we are at the top node and there is nothing left to do
            return
        elif self.heap[index][0] > self.heap[parent][0]:
            # if there is a child node that is greater than the parent and must be swapped
            self.swap(index, parent)
            self.reshuffle(parent)

    def swap(self, a, b):
        # swaps two nodes in the priority queue
        self.heap[a], self.heap[b] = self.heap[b], self.heap[a]

    def maxHeapify(self, index):
        # heapify each subtree by comparing the values of each parent node with its children, if there are children
        # that are larger then they are swapped
        left = index * 2
        right = (index * 2) + 1
        largest = index
        if len(self.heap) > left and self.heap[largest][0] < self.heap[left][0]:
            largest = left
        if len(self.heap) > right and self.heap[largest][0] < self.heap[right][0]:
            largest = right
        if largest != index:
            self.swap(index, largest)
            self.maxHeapify(largest)
