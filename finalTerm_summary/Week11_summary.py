# Symbol Table에서 리스트를 Value로 갖는 경우
'''
st = {}

st["A"] = [1, 2]
st["B"] = [3, 4]

st["A"].remove(1)
st["A"].append(1)


print(st)
del st["A"][0]
print(st)
'''

# Set() 자료구조
'''
s = set()

s.add("a")
s.update(["b", "c"])
s.remove("a")

print(s)
'''

# Cycle Detection 알고리즘 구현

import queue


def cycleDetection(g):
    def recur(v):
        visited[v] = True
        verticesInRecurStack.add(v)

        for w in g.adj[v]:
            if w in verticesInRecurStack:
                return True
            
            if not visited[w]:
                if recur(w) :
                    return True
                
        verticesInRecurStack.remove(v)
        return False
            
    visited = [False for _ in range(g.V)]
    verticesInRecurStack = set()

    for v in range(g.V):
        if not visited[v]:
            recur(v)



# sap() 함수 구현
            
def sap(g, aList, bList):

    A, B = 1, 2

    sca = -1
    pathlen = 100000000000000000000

    a_visited = [False for _ in range(g.V)]
    b_visited = [False for _ in range(g.V)]

    a_len = [None for _ in range(g.V)]
    b_len = [None for _ in range(g.V)]

    q = queue()

    for a_elemenet in aList:
        q.put((a_elemenet, A))
        a_visited[a_elemenet] = True
        a_len[a_elemenet] = 0

    for b_element in bList:
        q.put((b_element, B))
        b_visited[b_element] = True
        b_len[b_element] = 0

    for v in range(g.V):
        if a_len[v] == 0 and b_len[v] == 0:
            return v, 0

    while not q.empty():
        v, side = q.get()

        if side == A:
            if a_len[v] + 1 >= pathlen:
                break

            for w in g.adj[v]:
                if not a_visited[w]:
                    q.put((w, A))
                    a_visited[w] = True
                    a_len[w] = a_len[v] + 1

                    if b_len[w] != None and (a_len[w] + b_len[w]) < pathlen:
                        pathlen = a_len[w] + b_len[w]
                        sca = w

        else:
            for w in g.adj[v]:
                if not b_visited[w]:
                    q.put((w, B))
                    b_visited[w] = True
                    b_len[w] = b_len[v] + 1

                    if a_len[w] != None and (a_len[w] + b_len[w]) < pathlen:
                        pathlen = a_len[w] + b_len[w]
                        sca = w
                        
    return sca, pathlen