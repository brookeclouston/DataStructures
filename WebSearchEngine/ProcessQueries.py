"""
Author: Brooke Clouston
Date Created: March 15 2019

This class implements a simple web search engine by building a list of WebPageIndex Instances from a folder containing
a set of "web pages" (txt files) and then enters a loop to process a series of user queries. This class was created in
response to part 1.5 of Assignment 3 of CISC235 Winter 2019.
"""
import os
from WebPageIndex import WebPageIndex
from WebPagePriorityQueue import WebPagePriorityQueue


class ProcessQueries:

    def __init__(self, numOfQueries=None):
        # constructor for class, directs function calls, has optional value for a user specified number of results
        self.numOfQueries = numOfQueries
        self.buildWebPageIndexes()
        self.buildQueries()
        self.processQueries()

    def buildWebPageIndexes(self):
        # builds a list of WebPageIndexes by pointing to the file 'test data' containing the txt files
        webPageIndexes = []
        testdata = os.listdir("test data")
        for file in testdata:
            if file != "queries.txt"and file != ".DS_Store":
                instance = WebPageIndex(file)
                webPageIndexes.append(instance)
        return webPageIndexes

    def buildQueries(self):
        # creates a list of queries read in from file containing query list
        return [line.rstrip("\n") for line in open("test data/queries.txt", "r")]

    def processQueries(self):
        # processes each query by first building a MaxHeap then removing the highest element until there are none left
        queryList = self.buildQueries()
        webPageInstances = self.buildWebPageIndexes()
        for query in queryList:
            numOfQueries = self.numOfQueries
            print("PROCESSING QUERY: ", query, "\n")
            prioirtyQueue = WebPagePriorityQueue(query, webPageInstances)
            maxHeap = prioirtyQueue.maxHeap
            if numOfQueries is None:
                while len(maxHeap) != 1:
                    if maxHeap[1][0] != 0:
                        print(prioirtyQueue.poll().filename)

                    else:
                        prioirtyQueue.poll()
                print()
            else:
                while len(maxHeap) != 1 and numOfQueries != 0:
                    if maxHeap[1][0] != 0:
                        print(prioirtyQueue.poll().filename)

                    else:
                        prioirtyQueue.poll()
                    numOfQueries -= 1
                print()


if __name__ == "__main__":
    ProcessQueries()
