import random
import timeit


def quickSelect(a, k, m):
    '''
    Find all elements (in order) in between k-th and m-th smallest elements, 
        including the k-th and the m-th, where 0 <= k <= m <= len(a)-1
    '''
    assert isinstance(a, list) 
    assert isinstance(k, int) and isinstance(m, int) and 0 <= k and k <= m and m <= len(a)-1

    pass


def speedCompare(a):
    def recur(a, lo, hi):
        if hi <= lo: return

        i, j = lo+1, hi
        while True:
            while i <= hi and a[i] < a[lo]: i = i+1
            while j >= lo+1 and a[j] > a[lo]: j = j-1

            if (j <= i): break
            a[i], a[j] = a[j], a[i]
            i, j = i+1, j-1
        a[lo], a[j] = a[j], a[lo]        
           
        recur(a, lo, j-1)
        recur(a, j+1, hi)

    random.shuffle(a)
    recur(a, 0, len(a)-1)
    return a


def testCorrectness(a, k, m, expectedOutput, correct, output2console):    
    print(f"Correctness test for selecting {m-k+1} out of {len(a)} elements")
    output = quickSelect(a.copy(), k, m)
    if output2console: print(f"quickSelect({a}, {k}, {m}) = {output}")
    if output == expectedOutput: print("Pass")
    else:
        print("Fail")
        if output2console: print(f"expected output = {expectedOutput}")
        correct = False
    print()

    return correct


if __name__ == "__main__":    
    correct = True

    a = [2, 9, 3, 0, 6, 1, 4, 5, 7, 8]
    correct = testCorrectness(a, 0, 0, [0], correct, True)
    correct = testCorrectness(a, 3, 5, [3, 4, 5], correct, True) 
    correct = testCorrectness(a, 6, 9, [6, 7, 8, 9], correct, True)
    correct = testCorrectness(a, 0, 9, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], correct, True)

    size, k, m = 100, 57, 73
    offset, step = random.randint(100, 1000), random.randint(2, 100)
    a = [offset + step*i for i in range(size)]
    random.shuffle(a)    
    expectedOutput = [offset + step*i for i in range(k, m+1)]
    correct = testCorrectness(a, k, m, expectedOutput, correct, False)

    size, k, m = 10000, 2000, 2100
    offset, step = random.randint(100, 1000), random.randint(2, 100)
    a = [offset + step*i for i in range(size)]
    random.shuffle(a)    
    expectedOutput = [offset + step*i for i in range(k, m+1)]
    correct = testCorrectness(a, k, m, expectedOutput, correct, False) 

    size, k, m, n = 100000, 20000, 20100, 1
    print(f"Speed test for selecting {m-k+1} out of {size} elements in random order")
    if not correct: print("Fail since the algorithm is not correct")
    else:                 
        a = [i for i in range(size)]        
        random.shuffle(a)
        
        tSpeedCompare = timeit.timeit(lambda: speedCompare(a.copy()), number=n)/n
        tQuickSelect = timeit.timeit(lambda: quickSelect(a.copy(), k, m), number=n)/n
        print(f"QuickSort and QuickSelect({k}, {m}) took {tSpeedCompare:.10f} and {tQuickSelect:.10f} seconds")
        print(f"thus tSpeedCompare / tQuickSelect = {tSpeedCompare / tQuickSelect:.10f}")
        if tSpeedCompare / tQuickSelect > 2.0: print("Pass")
        else: print("Fail")
    print()

    size, k, m, n = 100000, 20000, 20100, 1
    print(f"Speed test for selecting {m-k+1} out of {size} elements in ascending order")
    if not correct: print("Fail since the algorithm is not correct")
    else:                 
        a = [i for i in range(size)]        
        
        tSpeedCompare = timeit.timeit(lambda: speedCompare(a.copy()), number=n)/n
        tQuickSelect = timeit.timeit(lambda: quickSelect(a.copy(), k, m), number=n)/n
        print(f"QuickSort and QuickSelect({k}, {m}) took {tSpeedCompare:.10f} and {tQuickSelect:.10f} seconds")
        print(f"thus tSpeedCompare / tQuickSelect = {tSpeedCompare / tQuickSelect:.10f}")
        if tSpeedCompare / tQuickSelect > 2.0: print("Pass")
        else: print("Fail")
    print()

    size, k, m, n = 100000, 0, 100000 - 1, 1
    print(f"Speed test for selecting {m-k+1} out of {size} elements with 3 unique keys")
    if not correct: print("Fail since the algorithm is not correct")
    else:                 
        a = [random.randint(0,2) for i in range(size)]        
        
        tSpeedCompare = timeit.timeit(lambda: speedCompare(a.copy()), number=n)/n
        tQuickSelect = timeit.timeit(lambda: quickSelect(a.copy(), k, m), number=n)/n        
        print(f"QuickSort and QuickSelect({k}, {m}) took {tSpeedCompare:.10f} and {tQuickSelect:.10f} seconds")
        print(f"thus tSpeedCompare / tQuickSelect = {tSpeedCompare / tQuickSelect:.10f}")
        if tSpeedCompare / tQuickSelect > 2.0: print("Pass")
        else: print("Fail")
    print()
    