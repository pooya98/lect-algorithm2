# Graph 클래스 선언해보기

from queue import Queue


class Graph:
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adj = [[] for _ in range(self.V)]

    def addEdge(self, v1, v2):
        self.adj[v1].append(v2)
        self.adj[v2].append(v1)
        self.E +=1 

    def degree(self, v):
        return len(self.adj[v])
    
    def __str__(self):
        rtList = [f"{self.V}개의 정점과 {self.E}개의 간선으로 이루어진 Digraph\n"]

        for v in range(self.V):
            for w in self.adj[v]:
                rtList.append(f"{v} - {w}\n")

        return "".join(rtList)
'''   
g = Graph(2)
g.addEdge(0, 1)
print(g)
'''



# DFS 구현

class DFS:
    def __init__(self, g, s):
        def recur(v):
            self.visited[v] = True

            for w in g.adj[v]:
                if not self.visited[w]:
                    recur(w)
                    self.fromVertex[w] = v


        self.g, self.s = g, s
        self.visited = [False for _ in range(g.V)]
        self.fromVertex = [None for _ in range(g.V)]
        
        recur(s)

    def pathTo(self, v):
        if not self.visited[v]:
            return None

        path = []
        curNode = v

        while curNode != None:
            path.append(curNode)
            curNode = self.fromVertex[curNode]

        path.reverse()
        return path
    

# BFS 구현
    
class BFS:
    def __init__(self, g, s):
        self.g, self.s = g, s
        self.visited = [False for _ in range(self.g.V)]
        self.fromVertex = [None for _ in range(self.g.V)]
        self.distance = [None for _ in range(self.g.V)]

        q = Queue()

        q.put(s)
        self.visited[s] = True
        self.distance[s] = 0

        while not q.empty():
            v = q.get()

            for w in self.g.adj[v]:
                if not self.visited[w]:
                    q.put(w)
                    self.visited[w] = True
                    self.fromVertex[w] = v
                    self.distance[w] = self.distance[v] + 1

    def pathTo(self, v):
        if not self.visited[v]:
            return None
        
        path = []
        curNode = v

        while curNode != None:
            path.append(curNode)
            curNode = self.fromVertex[curNode]

        path.reverse()
        return path
    

# msBFS 구현
    
class MsBFS:
    def __init__(self, g, S):
        self.g, self.S = g, S
        self.visited = [False for _ in range(g.V)]
        self.fromVertex = [None for _ in range(g.V)]
        self.distance = [None for _ in range(g.V)]

        q = Queue()

        for s in S:
            q.put(s)
            self.visited[s] = True
            self.distance[s] = 0

        while not q.empty():
            v = q.get()

            for w in self.g.adj[v]:
                if not self.visited[w]:
                    q.put(w)
                    self.visited[w] = True
                    self.fromVertex[w] = v
                    self.distance[w] = self.distance[v] + 1
    

# CC 클래스 구현
    
class CC:
    def __init__(self, g):
        def recur(v):
            self.id[v] = self.count

            for w in self.g.adj[v]:
                if self.id[w] == None:
                    recur(w)

        self.g = g
        self.count = 0

        self.id = [None for _ in range(self.g.V)]

        for v in range(self.g.V):
            if id[v] == None:
                self.recur(v)
                self.count += 1

    def connected(self, v, w):
        return self.id[v] == self.id[w]
    

# Digraph 클래스 구현

class Digraph:
    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adj = [[] for _ in range(self.V)]

    def addEdge(self, v, w):
        self.adj[v].append(w)
        self.E += 1

    def outDegree(self, v):
        return len(self.adj[v])
    
    def reverse(self):
        reversed_graph = Digraph(self.V)

        for v in range(self.V):
            for w in self.adj[v]:
                reversed_graph.addEdge(w, v)

        return reversed_graph
    
# Topological Sort 구현
def topologicalSort(g):
    def recur(v):
        if visited[v] == True:
            return
        
        visited[v] = True

        for w in g.adj[v]:
            if not visited[w]:
                recur(w)

        t_order.append(v)
 

    visited = [False for _ in range(g.V)]
    t_order = []

    for v in range(g.V):
        recur(v)

    t_order.reverse()
    return t_order


# SCC 구현

class SCC:
    def __init__(self, g): # Do strongly-connected-components pre-processing, based on Kosaraju-Sharir algorithm
        def recur(v):
            self.scc_id = self.scc_count

            for w in self.g.adj[v]:
                if self.scc_id[i] == None:
                    recur(w)

        self.g = g
        self.scc_id = [None for _ in range(g.V)]
        self.scc_count = 0
        reversed_g = g.reverse()
        reversed_to = topologicalSort(reversed_g)

        for i in reversed_to:
            if self.scc_id[i] == None:
                recur(i)
                self.scc_count += 1


    def connected(self, v, w): # Are v and w connected?
        if self.id[v] == self.id[w]:
            return True
        else:
            return False

        
if __name__ == "__main__":
    g = Graph(13)
    g.addEdge(0,1)
    g.addEdge(0,2)
    g.addEdge(0,5)
    g.addEdge(0,6)
    g.addEdge(3,4)
    g.addEdge(3,5)
    g.addEdge(4,5)
    g.addEdge(4,6)
    g.addEdge(7,8)
    g.addEdge(9,10)
    g.addEdge(9,11)
    g.addEdge(9,12)
    g.addEdge(11,12)

    print(g)
    
    print(g.adj[0], g.degree(0))    
    print(g.adj[5], g.degree(5))
    print(g.adj[9], g.degree(9))
    
    dfs = DFS(g,0)
    print(dfs.visited, dfs.fromVertex)
    print(dfs.pathTo(0))
    print(dfs.pathTo(1))
    print(dfs.pathTo(2))
    print(dfs.pathTo(3))
    print(dfs.pathTo(4))
    print(dfs.pathTo(5))
    print(dfs.pathTo(6))
    print(dfs.pathTo(7))
    #print(dfs.hasPathTo(6))
    #print(dfs.hasPathTo(7))