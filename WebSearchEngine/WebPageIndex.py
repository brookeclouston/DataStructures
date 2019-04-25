"""
Author: Brooke Clouston
Date Created: March 11 2019

This class creates an AVL tree using words built from a text file. It contains the function getCount(s) which returns
the number of occurrences of the word 's'. This class was created in response to part 1.3 of Assignment 3 of CISC 235
Winter 2019.
"""

from AVLTreeMap import AVLTreeMap
import string


class WebPageIndex:

    def __init__(self, filename):
        # constructor for class
        self.filename = filename

    def loadFromFile(self):
        # reads and formats the file then returns as a list of individual words that are in the file
        lineList = []
        wordList=[]
        filepath = "test data/" + self.filename
        file = open(filepath, "r")
        for word in file:
            new = word.lower()  # makes each word lowercase
            lineList.append(new.translate(str.maketrans("", "", string.punctuation)))  # strips each word of punctuation
        for line in lineList:
            wordList += (line.split())
        return wordList  # returns a list of individual words

    def wordDictionary(self):
        # returns dictionary where each key refers to word appearing in file and each value represents a list
        # containing the positions of this word in the file
        wordList = self.loadFromFile()  # gets the wordList
        wordDict = {}
        indexcount = 0  # keeps track of current index in wordList
        for word in wordList:
            if word in wordDict:
                # if word is already in the dictionary, the index is appended to value list
                wordDict[word].append(indexcount)
            else:
                # if word in not in dictionary a new key-value pair is created
                wordDict[word] = [indexcount]
            indexcount += 1
        return wordDict

    def buildTree(self):
        # builds an AVL tree using AVLTreeMap preserving key-value pairs from the dictionary created
        wordDict = self.wordDictionary()  # creates dictionary of words
        avl = AVLTreeMap()
        for combo in wordDict:  # iterates through the dictionary and inserts into tree
            avl.put(combo, wordDict[combo])
        return avl

    def getCount(self, word):
        # returns the number of occurrences of a word in the text file
        avl = self.buildTree()
        node = avl.get(word)
        if node is None:
            return 0
        return len(node)
