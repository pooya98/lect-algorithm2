import math
import timeit
import random

def collinearPoints(points):
    # step00. 변수, 상수 선언
    candidates = []             # "4개 이상 점 연결하는 직선"을 저장하는 리스트
    result = []                 # "4개 이상 점 연결하는 직선 중 Maximal한 직선"을 저장하는 리스트


    # step01. x(1순위 기준), y(2순위 기준) 좌표를 기준으로 좌표 정렬
    sorted_points = sorted(points, key = lambda p:(p[0], p[1]))


    # step02. 각 점 기준으로 기울기 같은 점 찾기
    for basis_index in range(len(sorted_points)):
        slope_list = []     # 기준점과 x좌표가 같거나 큰 점들의 기울기를 저장하는 리스트

        # step02-1. 각 점의 기울기 계산 후, 저장
        for opponent_index in range(basis_index + 1, len(sorted_points)):
            if sorted_points[opponent_index][0] == sorted_points[basis_index][0]:
                slope_list.append((opponent_index, float('inf')))
            else:
                slope = (sorted_points[opponent_index][1] - sorted_points[basis_index][1]) / (sorted_points[opponent_index][0] - sorted_points[basis_index][0])
                slope = math.floor(slope*1000000) / 1000000
                slope_list.append((opponent_index, slope))
            
        # step02-2. 각 점을 기울기을 기준으로 stable하게 정렬
        slope_list.sort(key = lambda x:x[1])

        # step02-3. collinear Points를 찾아 candidates에 저장

        prev_slope = float('-inf')  # 이전 slope를 저장하는 변수
        prev_index = (0, 0)         # 이전 점의 인덱스를 저장하는 변수
        count = 0                   # 같은 기울기가 연속되는 횟수 저장하는 변수

        for (cur_index, cur_slope) in slope_list:
            if prev_slope == cur_slope:             # 직전 원소와 기울기가 같다면, count 1증가하고, prev_index 갱신
                count += 1
                prev_index = cur_index
            else:                                   # 직전 원소와 기울기가 다르다면, 직전까지의 count값을 확인 후, collinear points 저장
                if count >= 3:
                    basis_point = (sorted_points[basis_index][0], sorted_points[basis_index][1])
                    opponent_point = (sorted_points[prev_index][0], sorted_points[prev_index][1])
                    candidates.append((basis_point, opponent_point, prev_slope))
                
                prev_slope = cur_slope              # 새로운 기울기를 가진 원소가 탐색되었기 때문에, prev_slope, prev_index, count 값 초기화
                prev_index = cur_index
                count = 1

        if count >= 3:                              # 반복문 종료 후, count값 확인 후, collinear points 저장
            last_point_index = slope_list[-1][0]
            basis_point = (sorted_points[basis_index][0], sorted_points[basis_index][1])
            opponent_point = (sorted_points[last_point_index][0], sorted_points[last_point_index][1])
            candidates.append((basis_point, opponent_point, prev_slope))


    # step03. Candidates 리스트에서 Maximal한 collinear points를 찾아 result 리스트에 저장
    if len(candidates) > 0:
        candidates.sort(key=lambda x : (x[2], x[1]))

        prev_end_point = (0, 0)
        prev_slope = candidates[0][2] - 1

        for candidate in candidates:
            if (candidate[1] == prev_end_point) and (candidate[2] == prev_slope):
                continue
            else:
                result.append((candidate[0][0], candidate[0][1], candidate[1][0], candidate[1][1]))
                prev_end_point = candidate[1]
                prev_slope = candidate[2]


    # step04. result 리스트의 원소들을 px, py, qx, qy 순으로 기준 정렬
    result.sort(key = lambda x : (x[0], x[1], x[2], x[3]))

    return result


def correctnessTest(input, expected_output, correct):
    output = collinearPoints(input)
    print(f"collinearPoints({input})\n{output}")
    if output == expected_output: print("Pass")
    else:        
        print(f"Fail - expected output: {expected_output}")
        correct = False
    print()    

    return correct


def simulateNSquareLogN(points):
    points = sorted(points, key=lambda p:(p[1], -p[0]))
    for i in range(0, len(points)):
        slopes = []
        for j in range(i+1, len(points)):
            if points[i][0] == points[j][0]: slopes.append((points[j][0], points[j][1], float('inf')))
            else: slopes.append((points[j][0], points[j][1], (points[j][1]-points[i][1])/(points[j][0]-points[i][0])))
        slopes.sort(key=lambda p:(p[1],p[2],p[0]))
        
        for j in range(1, len(slopes)):
            if slopes[j][2] == slopes[j-1][2]:
                for k in range(5): pass


'''
Unit Test
'''
if __name__ == "__main__":

    print("Correctness test for collinearPoints()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    print()
    correct = True

    # No collinear sets found, thus return the empty list []
    input = [(0,0),(1,1)]
    expected_output = []
    correct = correctnessTest(input, expected_output, correct)


    input = [(0,0), (1,1), (3,3), (4,4), (6,6), (7,7), (9,9)]
    expected_output = [(0,0,9,9)]    
    correct = correctnessTest(input, expected_output, correct)

    input = [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (8,0)]
    expected_output = [(1,0,8,0)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(7,0), (14,0), (22,0), (27,0), (31,0), (42,0)]
    expected_output = [(7,0,42,0)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,-2), (0,-53)]
    expected_output = [(0, -53, 0, 5)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(19000,10000), (18000,10000), (32000,10000), (21000,10000), (1234,5678), (14000,10000)]
    expected_output = [(14000,10000,32000,10000)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(12446,18993), (12798,19345), (12834,19381), (12870,19417), (12906,19453), (12942,19489)]
    expected_output = [(12446,18993,12942,19489)]
    correct = correctnessTest(input, expected_output, correct)


    input = [(0,0), (0,1), (0,2), (0,3), (1,0), (1,1), (1,2), (1,3)]
    expected_output = [(0,0,0,3), (1,0,1,3)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(10000,0), (0,10000), (3000,7000), (7000,3000), (20000,21000), (3000,4000), (14000,15000), (6000,7000)]
    expected_output = [(0, 10000, 10000, 0), (3000, 4000, 20000, 21000)]    
    correct = correctnessTest(input, expected_output, correct)    


    # Case where the same point appears multiple times
    input = [(1,1), (2,2), (3,3), (4,4), (2,0), (3,-1), (4,-2), (0,1), (-1,1), (-2,1), (-3,1), (2,1), (3,1), (4,1), (5,1)]
    expected_output = [(-3, 1, 5, 1), (1, 1, 4, -2), (1, 1, 4, 4)]
    correct = correctnessTest(input, expected_output, correct)    


    print()
    print("Speed test for collinearPoints()")
    if not correct: print("Fail (since the algorithm is not correct)")
    else:
        repeat = 10
        inputLength = 100
        minC, maxC = -1000000, 1000000
        points = [(random.randint(minC, maxC), random.randint(minC, maxC)) for _ in range(inputLength)]
        tCodeToCompare = timeit.timeit(lambda: simulateNSquareLogN(points), number=repeat) / repeat
        tSubmittedCode = timeit.timeit(lambda: collinearPoints(points), number=repeat) / repeat        
        print(f"Average running time of collinearPoints() and simulateNSquareLogN() with {inputLength} points: {tSubmittedCode:.10f} and {tCodeToCompare:.10f}")
        #print(f"{tSubmittedCode / tCodeToCompare}")
        if tSubmittedCode < tCodeToCompare * 3: print("Pass")
        else:
            print("Fail")
        print()
        
    