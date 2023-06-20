import pygame


class Tree:
    def __init__(self, data):
        self.branches = []
        self.data = data

    def insert(self, data):
        t = Tree(data)
        self.branches.append(t)

    def getEverythingInTree(self, numbers):
        numbers.append(self.data)
        if self.left != None:
            self.left.getEverythingInTree(numbers)

        if self.right != None:
            self.right.getEverythingInTree(numbers)
        return numbers
