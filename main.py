# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 15:04:56 2016

@author: guttag, revised egrimson
@modify for self usage by : tzlil lev or
"""
sizes = {}
class Node(object):
    def __init__(self, name):
        """Assumes name is a string"""
        self.name = name
    def getName(self):
        return self.name
    def __add__(self, other):
        try:
            global sizes
            return sizes[(self, other)]
        except:
            return None
    def __repr__(self):
        return self.name

class Edge(object):
    def __init__(self, src, dest, length=1):
        """Assumes src and dest are nodes"""
        self.src = src
        self.dest = dest
        self.length = length
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def __repr__(self):
        return self.src.getName() + '->' + self.dest.getName()
               
class Digraph(object):
    """edges is a dict mapping each node to a list of
    its children"""
    def __init__(self):
        self.edges = {}
        global sizes
        if sizes!={}:
            sizes = {}
    def addNode(self, node):
        if node in self.edges:
            raise ValueError('Duplicate node')
        else:
            self.edges[node] = []
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.edges and dest in self.edges):
            raise ValueError('Node not in graph')
        self.edges[src].append(dest)
        global sizes
        sizes[(src, dest)]=edge.length
    def childrenOf(self, node):
        return self.edges[node]
    def hasNode(self, node):
        return node in self.edges
    def getNode(self, name):
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)
    def __repr__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.getName() + '->'\
                         + dest.getName() + '\n'
        return result[:-1] #omit final newline

class Graph(Digraph):
    def addEdge(self, edge, length=1):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource(), length)
        Digraph.addEdge(self, rev)
    
def buildGraph(graphType):
    g = graphType()
    for name in ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'M', 'N', 'Z'): #Create 7 nodes
        g.addNode(Node(name))
    g.addEdge(Edge(g.getNode('C'), g.getNode('E'),10))
    g.addEdge(Edge(g.getNode('E'), g.getNode('G')))
    g.addEdge(Edge(g.getNode('D'), g.getNode('F')))
    g.addEdge(Edge(g.getNode('F'), g.getNode('G')))
    g.addEdge(Edge(g.getNode('A'), g.getNode('C')))
    g.addEdge(Edge(g.getNode('A'), g.getNode('B')))
    g.addEdge(Edge(g.getNode('B'), g.getNode('D')))
    g.addEdge(Edge(g.getNode('A'), g.getNode('M'), 2))
    g.addEdge(Edge(g.getNode('M'), g.getNode('N')))
    g.addEdge(Edge(g.getNode('N'), g.getNode('E')))
    g.addEdge(Edge(g.getNode('M'), g.getNode('Z')))
    # g.addEdge(Edge(g.getNode('Denver'), g.getNode('Phoenix')))
    # g.addEdge(Edge(g.getNode('Denver'), g.getNode('New York')))
    # g.addEdge(Edge(g.getNode('Los Angeles'), g.getNode('Boston')))
    return g

def get_len(path):
    total = 0
    if path==[]:
        return 0
    elif not path:
        return 0
    else:
        for i in range(len(path)-1):
            total += path[i] + path[i+1]
        return total


def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result 

def DFS(graph, start, end, path, shortest, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns a shortest path from start to end in graph ~ TCD Track"""
    path = path + [start]
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path: #avoid cycles
            if shortest == None or get_len(path) < get_len(shortest):
                newPath = DFS(graph, node, end, path, shortest,
                              toPrint)
                if newPath != None:
                    shortest = newPath
        elif toPrint:
            print('Already visited', node)
    return shortest

def DFS_TPD(graph, start, end, path, longest, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns a shortest path from start to end in graph ~ TCD Track"""
    path = path + [start]
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path: #avoid cycles
            if longest == None or get_len(path) > get_len(longest):
                newPath = DFS(graph, node, end, path, longest,
                              toPrint)
                if newPath != None:
                    longest = newPath
        elif toPrint:
            print('Already visited', node)
    return longest

def shortestPath(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return DFS(graph, start, end, [], None, toPrint)
def longestPath(graph, start, end, toPrint=False):
    """Assume the graph is a Digraph; start and end are Nodes
    Returns a longest path from start to end in graph"""
    return DFS_TPD(graph,start,end, [], None, toPrint)

def testSP(source, destination):
    g = buildGraph(Digraph)
    sp = shortestPath(g, g.getNode(source), g.getNode(destination),
                      toPrint = False)
    if sp != None:
        print('Shortest path from', source, 'to',
              destination, 'is', printPath(sp), "The Length is ", get_len(sp))
    else:
        print('There is no path from', source, 'to', destination)
    lp = longestPath(g, g.getNode(source), g.getNode(destination))
    if lp != None:
        print('Longest path from', source, 'to',
              destination, 'is', printPath(lp), "The Length is ", get_len(lp))
    else:
        print('There is no path from', source, 'to', destination)


testSP('A', 'G')

#testSP('Boston', 'Phoenix')
#print()

printQueue = True 

def BFS(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    initPath = [start]
    pathQueue = [initPath]
    while len(pathQueue) != 0:
        #Get and remove oldest element in pathQueue
        if printQueue:
            print('Queue:', len(pathQueue))
            for p in pathQueue:
                print(printPath(p))
        tmpPath = pathQueue.pop(0)
        print(tmpPath, "S~~23")
        if toPrint:
            print('Current BFS path:', printPath(tmpPath))
            print()
        lastNode = tmpPath[-1]
        if lastNode == end:
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath:
                newPath = tmpPath + [nextNode]
                pathQueue.append(newPath)
    return None

def shortestPath(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    return BFS(graph, start, end, toPrint)
#
# testSP('A', 'G')
#
