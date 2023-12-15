# WUGraph의 Edge 클래스 구현

class Edge:
    def __init__(self, v, w, weight):
        if v < w: 
            self.v, self.w = v, w
        else:
            self.v, self.w = w, v

        self.weight = weight

    def other(self, v):
        if self.v == v:
            return self.w
        else:
            return self.v
        
# WUGraph의 클래스 구현
        
class WUGraph:
    def __init__(self, V):
        self.V, self.E = V, 0
        self.adj = [[] for _ in range(V)]
        self.edges = []

    def addEdge(self, v, w, weight):
        e = Edge(v, w, weight)

        self.adj[v].append(e)
        self.adj[w].append(e)
        self.edges.append(e)
        self.E += 1


# Weight quick Union 구현
        
class QU:
    def __init__(self, V):
        self.id = [i for i in range(V)]
        self.size = [1 for _ in range(V)]

    def root(self, v):
        p = v

        while p != self.id[p]:
            p = self.id[p]

        return p

    def union(self, a, b):
        a_root = self.root(a)
        b_root = self.root(b)

        if self.size[a_root] < self.size[b_root]:
            self.id[a_root] = b_root
            self.size[b_root] += self.size[a_root]
        else:
            self.id[b_root] = a_root
            self.size[a_root] += self.size[b_root]

    def connected(self, a, b):
        return self.root[a] == self.root[b]


# Kruskal 알고리즘
from pathlib import Path
from queue import PriorityQueue
import timeit

'''
Class for storing weighted edges
'''
class Edge:
    def __init__(self, v, w, weight): # Create an edge v-w with a double weight
        if v<=w: self.v, self.w = v, w  # Put the lesser number in v for convenience
        else: self.v, self.w = w, v        
        self.weight = weight
    
    def __lt__(self, other): # < operator, used to sort elements (e.g., in a PriorityQueue, sorted() function)
        assert(isinstance(other, Edge))
        return self.weight < other.weight

    def __gt__(self, other): # > operator, used to sort elements
        assert(isinstance(other, Edge))
        return self.weight > other.weight

    def __eq__(self, other): # == operator, used to compare edges for grading
        assert(isinstance(other, Edge))
        return self.v == other.v and self.w == other.w and self.weight == other.weight

    def __str__(self): # Called when an Edge instance is printed (e.g., print(e))
        return f"{self.v}-{self.w} ({self.weight})"

    def __repr__(self): # Called when an Edge instance is printed as an element of a list
        return self.__str__()

    def other(self, v): # Return the vertex on the Edge other than v
        if self.v == v: return self.w
        else: return self.v

'''
Class for storing WUGraphs (Weighted Undirected Graphs)
'''
class WUGraph:
    def __init__(self, V): # Constructor
        self.V = V # Number of vertices
        self.E = 0 # Number of edges
        self.adj = [[] for _ in range(V)]   # adj[v] is a list of vertices adjacent to v
        self.edges = []

    def addEdge(self, v, w, weight): # Add edge v-w. Self-loops and parallel edges are allowed
        e = Edge(v, w, weight) # Create one edge instance and use it for adj[v], adj[w], and edges[]
        self.adj[v].append(e)
        self.adj[w].append(e)
        self.edges.append(e)
        self.E += 1

    def degree(self, v):
        return len(self.adj[v])

    def __str__(self):
        rtList = [f"{self.V} vertices and {self.E} edges\n"]
        for v in range(self.V):
            for e in self.adj[v]:
                if v == e.v: rtList.append(f"{e}\n") # Do not print the same edge twice
        return "".join(rtList)

    '''
    Create a WUGraph instance from a file
        fileName: Name of the file that contains graph information as follows:
            (1) the number of vertices, followed by
            (2) one edge in each line, where an edge v-w with weight is represented by "v w weight"
            e.g., the following file represents a digraph with 3 vertices and 2 edges
            3
            0 1 0.12
            2 0 0.26
        The file needs to be in the same directory as the current .py file
    '''
    @staticmethod
    def fromFile(fileName):
        filePath = Path(__file__).with_name(fileName)   # Use the location of the current .py file   
        with filePath.open('r') as f:
            phase = 0
            line = f.readline().strip() # Read a line, while removing preceding and trailing whitespaces
            while line:                                
                if len(line) > 0:
                    if phase == 0: # Read V, the number of vertices
                        g = WUGraph(int(line))
                        phase = 1
                    elif phase == 1: # Read edges
                        edge = line.split()
                        if len(edge) != 3: raise Exception(f"Invalid edge format found in {line}")
                        g.addEdge(int(edge[0]), int(edge[1]), float(edge[2]))                        
                line = f.readline().strip()
        return g

'''
Class for performing Union Find using weighted quick union
    and storing the results    
'''
class UF:
    def __init__(self, V): # V: the number of vertices
        self.ids = [] # ids[i]: i's parent
        self.size = [] # size[i]: size of tree rooted at i
        for idx in range(V):
            self.ids.append(idx)
            self.size.append(1)       

    def root(self, i):
        while i != self.ids[i]: i = self.ids[i]
        return i

    def connected(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):    
        id1, id2 = self.root(p), self.root(q)
        if id1 == id2: return
        if self.size[id1] <= self.size[id2]: 
            self.ids[id1] = id2
            self.size[id2] += self.size[id1]
        else:
            self.ids[id2] = id1
            self.size[id1] += self.size[id2]

'''
Min Priority Queue based on a binary heap 
    with decreaseKey operation added
'''
class IndexMinPQ:
    def __init__(self, maxN): # Create an indexed PQ with indices 0 to (N-1)
        if maxN < 0: raise Exception("maxN < 0")
        self.maxN = maxN # Max number of elements on PQ
        self.n = 0 # Number of elements on PQ
        self.keys = [None] * (maxN+1)  # keys[i]: key with index i
        self.pq = [-1] * (maxN+1)  # pq[i]: index of the key at heap position i (pq[0] is not used)        
        self.qp = [-1] * maxN # qp[i]: heap position of the key with index i (inverse of pq[])        

    def isEmpty(self):
        return self.n == 0

    def contains(self, i): # Is i an index on the PQ?
        self.validateIndex(i)
        return self.qp[i] != -1

    def size(self):
        return self.n

    def insert(self, i, key): # Associate key with index i
        self.validateIndex(i)
        if self.contains(i): raise Exception(f"index {i} is already in PQ")
        self.n += 1
        self.qp[i] = self.n
        self.pq[self.n] = i
        self.keys[i] = key
        self.swimUp(self.n)

    def minIndex(self): # Index associated with the minimum key
        if self.n == 0: raise Exception("PQ has no element, so no min index exists")
        return self.pq[1]

    def minKey(self):
        if self.n == 0: raise Exception("PQ has no element, so no min key exists")
        return self.keys[self.pq[1]]

    def delMin(self):
        if self.n == 0: raise Exception("PQ has no element, so no element to delete")
        minIndex = self.pq[1]
        minKey = self.keys[minIndex]
        self.exch(1, self.n)
        self.n -= 1
        self.sink(1)
        assert(minIndex == self.pq[self.n+1])
        self.qp[minIndex] = -1 # Mark the index as being deleted
        self.keys[minIndex] = None
        self.pq[self.n+1] = -1
        return minKey, minIndex

    def keyOf(self, i):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        else: return self.keys[i]

    def changeKey(self, i, key):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        self.keys[i] = key
        self.swimUp(self.qp[i])
        self.sink(self.qp[i])

    def decreaseKey(self, i, key):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        if self.keys[i] == key: raise Exception(f"calling decreaseKey() with key {key} equal to the previous key")
        if self.keys[i] < key: raise Exception(f"calling decreaseKey() with key {key} greater than the previous key {self.keys[i]}")
        self.keys[i] = key
        self.swimUp(self.qp[i])

    def increaseKey(self, i, key):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        if self.keys[i] == key: raise Exception(f"calling increaseKey() with key {key} equal to the previous key")
        if self.keys[i] > key: raise Exception(f"calling increaseKey() with key {key} smaller than the previous key {self.keys[i]}")
        self.keys[i] = key
        self.sink(self.qp[i])

    def delete(self, i):
        self.validateIndex(i)
        if not self.contains(i): raise Exception(f"index {i} is not in PQ")
        idx = self.qp[i]
        self.exch(idx, self.n)
        self.n -= 1
        self.swimUp(idx)
        self.sink(idx)
        self.keys[i] = None
        self.qp[i] = -1   

    def validateIndex(self, i):
        if i < 0: raise Exception(f"index {i} < 0")
        if i >= self.maxN: raise Exception(f"index {i} >= capacity {self.maxN}")

    def greater(self, i, j):
        return self.keys[self.pq[i]] > self.keys[self.pq[j]]

    def exch(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]] = i
        self.qp[self.pq[j]] = j

    def swimUp(self, idx): # idx is the index in pq[]
        while idx>1 and self.greater(idx//2, idx):
            self.exch(idx, idx//2)            
            idx = idx//2

    def sink(self, idx): # idx is the index in pq[]
        while 2*idx <= self.n:    # If a child exists
            idxChild = 2*idx # Left child
            if idxChild<self.n and self.greater(idxChild, idxChild+1): idxChild = idxChild+1 # Find the smaller child
            if not self.greater(idx, idxChild): break
            self.exch(idx, idxChild) # Swap with (i.e., sink to) the greater child
            idx = idxChild

'''
Find an MST (Minimum Spanning Tree) using Kruskal's algorithm
    and return the MST with its weight sum
'''
def mstKruskal(g): # Constructor: finds an MST and stores it
    assert(isinstance(g, WUGraph))
    
    edgesInMST = [] # List that stores edges selected as part of the MST
    weightSum = 0 # Sum of edge weights in the MST

    pq = PriorityQueue()
    uf = UF(g.V)

    for e in g.edges:
        pq.put(e)

    while not pq.empty() and len(edgesInMST) < g.V - 1:
        e = pq.get()

        if not uf.connected(e.v, e.w):
            uf.union(e.v, e.w)
            edgesInMST.append(e)
            weightSum += e.weight

    return edgesInMST, weightSum


'''
Find an MST (Minimum Spanning Tree) using Prim's algorithm (lazy version)
    and return the MST with its weight sum
'''
def mstPrimLazy(g):
    assert(isinstance(g, WUGraph))

    edgesInMST = [] # Stores edges selected as part of the MST
    weightSum = 0
    included = [False for _ in range(g.V)]

    pq = PriorityQueue()
    included[0] = True

    for e in g.adj[0]:
        pq.put(e)

    while not pq.empty() and len(edgesInMST) < g.V - 1:
        e = pq.get()

        if not included[e.v] or not included[e.w]:
            if not included[e.v]:
                included[e.v] = True
                for ed in g.adj[e.v]:
                    if not included[ed.other(e.v)]:
                        pq.put(ed)

            if not included[e.w]:
                included[e.w] = True
                for ed in g.adj[e.w]:
                    if not included[ed.other(e.w)]
                        pq.put(ed)

            edgesInMST.append(e)
            weightSum += e.weight

    return edgesInMST, weightSum    


'''
Find an MST (Minimum Spanning Tree) using Prim's algorithm (eager version)
    and return the MST with its weight sum
'''
def mstPrimEager(g):
    def include(v):
        included[v] = True

        for e in g.adj[v]:
            op = e.other(v)
            if not included[op]:
                if not pq.contains(op):
                    pq.insert(op, e)
                else:
                    if e < pq.keyOf[op]:
                        pq.decreaseKey(op, e)

    edgesInMST = []
    weightSum = 0
    included = [False for _ in range(g.V)]

    pq = IndexMinPQ(g.V)

    include(0)

    while not pq.isEmpty() and len(edgesInMST) < g.V-1:
        e_key, e_index = pq.delMin()

        edgesInMST.append(e_index)
        weightSum += e_key.weight
        include(e_key)

    return edgesInMST, weightSum


