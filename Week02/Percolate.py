import statistics
import math
import random
import timeit

# Weighted Quick Union 방식으로 n개의 객체에 대해 t번 시뮬레이션하는 함수
def simulate(n, t):

    # WQU 연산 (1) - 특정 객체 i의 root를 반환하는 연산    
    def root(i):
        nonlocal ids
        while i != ids[i]: i = ids[i]
        return i

    # WQU 연산 (2) - 특정 객체 p와 q가 하나의 connected component 내에 속하는 지를 반환하는 연산
    def connected(p, q):
        return root(p) == root(q)

    # WQU 연산 (3) - 특정 객체 p가 속한 트리와 q가 속한 트리를 합치는 연산
    def union(p, q):    
        id1, id2 = root(p), root(q)
        if id1 == id2: return
        if size[id1] <= size[id2]: 
            ids[id1] = id2
            size[id2] += size[id1]
        else:
            ids[id2] = id1
            size[id1] += size[id2]
    

    results = []    # 각 시뮬레이션 결과를 저장하는 리스트 

    # Percolation 시뮬레이션 t회 진행
    for _ in range(t):
        ids = [i for i in range(n*n + 2)]               # 각 객체의 parent를 저장하는 리스트
        size = [1 for _ in range(n*n + 2)]              # 각 객체를 root노드로 보았을 때 트리의 크기를 저장하는 리스트
        open_flag = [False for i in range(n*n + 2)]     # 각 객체의 상태(열림, 닫힘)를 저장하는 리스트

        open_flag[n*n] = True                           # "가상 객체1"의 상태값(열림) 초기화
        open_flag[n*n + 1] = True                       # "가상 객체2"의 상태값(열림) 초기화

        indicesToOpen = [i for i in range(n*n)]         # 0 ~ N*N-1 의 값들을 임의로 섞어서 저장하는 리스트
        random.shuffle(indicesToOpen)                   # 셔플 수행

        for new_open in indicesToOpen:
            if open_flag[new_open] == False:        # 새로 열림을 수행한 노드의 open값이 False이면 객체 추가 진행
                open_flag[new_open] = True

                # 새로 open한 객체의 위, 아래를 확인하여 union을 수행하는 부분
                if new_open - n >= 0 and open_flag[new_open - n]:
                    union(new_open - n, new_open)
                if new_open + n < n*n and open_flag[new_open + n]:
                    union(new_open, new_open + n)

                # 새로 open한 객체의 좌, 우를 확인하여 union을 수행하는 부분
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

                # 새로 open한 객체가 1행에 속할 때, "가상객체1"와 union을 수행하는 부분
                if new_open < n:
                    union(new_open, n*n)

                # 새로 open한 객체가 N행에 속할 때, "가상객체2"와 union을 수행하는 부분   
                if new_open >= n*(n-1):
                    union(new_open, n*n + 1)

                # 가상 객체 간 연결이 True이면 객체 추가 종료
                if connected(n*n, n*n + 1) == True:
                    break


        open_count = 0      # 1회의 시뮬레이션에서 percolation이 될때까지 open한 객체의 수

        # 현 시뮬레이션에서 open한 객체의 수를 count하는 부분
        for i in range(n*n):
            if open_flag[i] == True:
                open_count += 1
        
        results.append(open_count/(n*n))    # result에 현재 시뮬레이션의 결과를 추가하는 부분

    return statistics.mean(results), statistics.stdev(results)  # t회의 시뮬레이션 결과에 대한 평균, 표준편차 값을 반환하는 부분


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


        
    