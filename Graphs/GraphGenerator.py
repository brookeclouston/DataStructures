"""
Author: Brooke Clouston
Date Created: April 1 2019
This script implements a graph generator and multiple methods for graph searches. It is in response to Assignment 4
of CISC 235 Winter 2019.
"""

import random
import queue
import heapq
import operator as op


class Vertex:
    # Vertex class

    def __init__(self, name):
        # Constructor for vertex class, creates a dictionary of a vertex's neighbours
        self.name = name
        self.neighbourDict = {}

    def addNeighbour(self, neighbour, weight):
        # Adds a neighbour to the vertex by updating its neighbour dict with a corresponding weight
        if neighbour not in self.neighbourDict:
            self.neighbourDict[neighbour] = weight

    def getNeighbours(self):
        # returns the neighbours of a given vertex
        return [x.name for x in self.neighbourDict]


class Graph:
    # Graph class

    def __init__(self):
        # Constructor for the graph function, creates a dictionary of vertices
        self.vertices = {}

    def addVertex(self, vertex):
        # Adds a vertex if it is not already in the graph
        newVertex = Vertex(vertex)
        if newVertex.name not in self.vertices:
            self.vertices[vertex] = newVertex
            return True
        return False

    def addEdge(self, v1, v2, weight):
        # Adds a weighted edge between two vertices
        if v1 not in self.vertices:
            self.addVertex(v1)
        if v2 not in self.vertices:
            self.addVertex(v2)
        self.vertices[v1].addNeighbour(self.vertices[v2], weight)

    def randomGeneration(self, n):
        # Generates a random graph using format suggested in assignment outline
        for name in range(n):
            self.addVertex(name)
        for i in range(2, len(self.vertices)):
            x = random.randint(1, i-1)
            S = random.sample(range(1, i), x)
            for s in S:
                w = random.randint(10, 100)
                self.addEdge(i, s, w)
                self.addEdge(s, i, w)

    def BFS(self):
        # Breadth-First search implementation that starts at a random vertex and returns the total
        # weight of the edges selected using a queue structure
        start = random.randint(0, len(self.vertices)-1)
        total = 0
        visited = [False] * len(self.vertices)
        counter = 0
        Q = queue.Queue()
        Q.put(start)
        visited[start] = True
        while counter < len(self.vertices)-1:
            counter += 1
            x = Q.get()
            neighbours = self.vertices[x].neighbourDict.keys()
            for y in neighbours:
                if visited[y.name] is False:
                    Q.put(y.name)
                    visited[y.name] = True
                    total += self.vertices[x].neighbourDict[y]
        return total

    def prim(self):
        # Implements Prim's MST Algorithm, returns the total weights of the edges it selects using a heap structure
        vertex = random.randint(0, len(self.vertices)-1)  # choosing a random start vector
        total = 0
        edges, msT, leftOver, minHeap = [], [], [], []
        msT.append(vertex)  # the MST tree that is being build
        for key in self.vertices:
            # the rest of the vertices that are not in msT
            if key not in msT:
                leftOver.append(key)
        numEdges = len(self.vertices)-1
        neighbours = self.vertices[vertex].neighbourDict
        for y in neighbours:
            minHeap.append([(vertex, y.name,), self.vertices[vertex].neighbourDict[y]])
        minHeap = heapq.nsmallest(len(minHeap), minHeap, key=op.itemgetter(-1))
        while len(msT) < numEdges:
            e = heapq.heappop(minHeap)[0]
            b = e[1]
            while b in msT and minHeap != []:
                e = heapq.heappop(minHeap)[0]
                b = e[1]
            edges.append(e)
            total += e[1]
            msT.append(b)
            leftOver.remove(b)
            bNeighbours = self.vertices[b].neighbourDict
            for y in bNeighbours:
                if y.name in leftOver:
                    minHeap.append(([(b, y.name,), self.vertices[b].neighbourDict[y]]))
                    minHeap = heapq.nsmallest(len(minHeap), minHeap, key=op.itemgetter(-1))
        return total

    def find(self, parent, i):
        # Helper function for Kruskal's algorithm to find the parent set of i
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        # Helper function for Kruskal's algorithm which unions two sets together
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        # Implements Kruskal's MST algorithm and returns the total weight of the edges in the constructed MST
        # following GeeksForGeeks algorithm implementation outline
        mst, minHeap = [], []
        i, edge = 0, 0
        total = 0
        for vertex in self.vertices:
            neighbours = self.vertices[vertex].neighbourDict
            for y in neighbours:
                w = self.vertices[vertex].neighbourDict[y]
                if [vertex, int(y.name), w] not in minHeap:
                    minHeap.append([int(y.name), vertex, w])
        minHeap = heapq.nsmallest(len(minHeap), minHeap, key=op.itemgetter(-1))
        parent, rank = [], []
        for node in range(len(self.vertices)):
            parent.append(node)
            rank.append(0)
        while edge < len(self.vertices)-1:
            u, v, w = minHeap[i]
            i += 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                edge += 1
                mst.append([(u, v), w])
                total += w
                self.union(parent, rank, x, y)
        return total


def comparison(k):
    # Implements a comparision made for graphs with different numbers of vertices repeated k times to compare the
    # average percentage by which the BFS search is larger than Prim's MST algorithm.
    vertList = [20, 40, 60]
    for n in vertList:
        total = 0
        counter = k
        while counter > 0:
            g = Graph()
            counter -= 1
            g.randomGeneration(n)
            B = g.BFS()
            P = g.prim()
            diff = ((B-P)/ P) * 100
            total += diff
        avg = (total/n)
        print("The average percentage by which B is larger than P for a graph with", n, "vertices is %", avg, ".")

if __name__ == "__main__":
    comparison(5)  # used to call comparision function which drives the script, example using 5

