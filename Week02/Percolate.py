import statistics
import math
import random
import timeit

def simulate(n, t):    
    def root(i):
        nonlocal ids
        while i != ids[i]: i = ids[i]
        return i

    def connected(p, q):
        return root(p) == root(q)

    def union(p, q):    
        id1, id2 = root(p), root(q)
        if id1 == id2: return
        if size[id1] <= size[id2]: 
            ids[id1] = id2
            size[id2] += size[id1]
        else:
            ids[id2] = id1
            size[id1] += size[id2]
    
    p = []

    for _ in range(t):
        ids = [i for i in range(n*n + 2)]
        size = [1 for _ in range(n*n + 2)]
        open_flag = [False for i in range(n*n + 2)]

        open_flag[n*n] = True
        open_flag[n*n + 1] = True

        indicesToOpen = [i for i in range(n*n)]
        random.shuffle(indicesToOpen)

        for new_open in indicesToOpen:
            if open_flag[new_open] == False:
                open_flag[new_open] = True

                if new_open - n >= 0 and open_flag[new_open - n]:
                    union(new_open - n, new_open)
                if new_open + n < n*n and open_flag[new_open + n]:
                    union(new_open, new_open + n)

                if new_open % n == 0:
                    if new_open + 1 < n*n and open_flag[new_open + 1]:
                        union(new_open, new_open + 1)
                elif new_open % n == n - 1:
                    if new_open - 1 >= 0 and open_flag[new_open - 1]:
                        union(new_open - 1, new_open)
                else:
                    if new_open - 1 >= 0 and open_flag[new_open - 1]:
                        union(new_open - 1, new_open)
                    if new_open + 1 < n*n and open_flag[new_open + 1]:
                        union(new_open, new_open + 1)

                if new_open < n:
                    union(new_open, n*n)
                if new_open >= n*(n-1):
                    union(new_open, n*n + 1)

                if connected(n*n, n*n + 1) == True:
                    break

        open_count = 0
        for i in range(n*n):
            if open_flag[i] == True:
                open_count += 1
        
        p.append(open_count/(n*n))

    return statistics.mean(p), statistics.stdev(p)


'''
Simulate the performance of Quick Union
'''
def simulateQU(n, t):
    def root(i):
        nonlocal ids
        while i != ids[i]: i = ids[i]
        return i

    def connected(p, q):
        return root(p) == root(q)

    def union(p, q):
        nonlocal ids
        id1, id2 = root(p), root(q)
        ids[id1] = id2
    
    for _ in range(t):
        ids = [i for i in range(n*n + 2)]
        for _ in range(math.floor(n*n*2)):
            connected(0, len(ids)-1)
            union(random.randint(0, len(ids)-1), random.randint(0, len(ids)-1))

'''
Simulate the performance of Quick Find
'''
def simulateQF(n, t):
    def connected(p, q):
        nonlocal ids
        return ids[p] == ids[q]

    def minMax(a, b):
        if a < b: return a, b
        else: return b, a

    def union(p, q):
        nonlocal ids
        id1, id2 = minMax(ids[p], ids[q])
        for idx, _ in enumerate(ids):
            if ids[idx] == id2: ids[idx] = id1
    
    for _ in range(t):
        ids = [i for i in range(n*n + 2)]
        for _ in range(math.floor(n*n*2)):
            connected(0, len(ids)-1)
            union(random.randint(0, len(ids)-1), random.randint(0, len(ids)-1))


'''
Unit Test
'''
if __name__ == "__main__":

    print("Correctness test for simulate()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    correct = True
    
    input = 1,100
    rt_val = simulate(*input)
    print(f"simulate{input}: {rt_val} ", end="")
    if rt_val[0] == 1: print("Pass ", end="")
    else:
        print("Fail ", end="")
        correct = False
    if rt_val[1] == 0: print("Pass ", end="")
    else:
        print("Fail ", end="")
        correct = False
    print()    

    input = 2,10000
    rt_val = simulate(*input)
    print(f"simulate{input}: {rt_val} ", end="")
    if math.floor(rt_val[0]*100) == 66: print("Pass ", end="")
    else:
        print("Fail ", end="")
        correct = False
    if round(rt_val[1]*10) == 1: print("Pass ", end="")
    else:
        print("Fail ", end="")
        correct = False
    print()

    input = 200,100
    rt_val = simulate(*input)
    print(f"simulate{input}: {rt_val} ", end="")
    if math.floor(rt_val[0]*100) == 59: print("Pass ", end="")
    else:
        print("Fail ", end="")
        correct = False
    if round(rt_val[1]*100) == 1: print("Pass ", end="")
    else:
        print("Fail ", end="")
        correct = False
    print()


    print()
    print()
    print("Speed test for simulate()")
    if not correct: print("Fail (since the algorithm is not correct)")
    else:
        repeat = 10
        input = 10,100
        simulateCompare = simulateQF
        tSubmittedCode = timeit.timeit(lambda: simulate(*input), number=repeat) / repeat
        tCodeToCompare = timeit.timeit(lambda: simulateCompare(*input), number=repeat) / repeat
        print(f"Average running time of simulate{input} and {simulateCompare.__name__}{input} : {tSubmittedCode:.10f} and {tCodeToCompare:.10f} ", end="")        
        if tSubmittedCode < tCodeToCompare * 0.2: print("Pass ", end="")
        else:
            print("Fail ", end="")
        print()
        #print(tSubmittedCode / tCodeToCompare)

        repeat = 10
        input = 10,100
        simulateCompare = simulateQU
        tSubmittedCode = timeit.timeit(lambda: simulate(*input), number=repeat) / repeat
        tCodeToCompare = timeit.timeit(lambda: simulateCompare(*input), number=repeat) / repeat
        print(f"Average running time of simulate{input} and {simulateCompare.__name__}{input} : {tSubmittedCode:.10f} and {tCodeToCompare:.10f} ", end="")        
        if tSubmittedCode < tCodeToCompare * 0.3: print("Pass ", end="")
        else:
            print("Fail ", end="")
        print()        
        #print(tSubmittedCode / tCodeToCompare)


        
    