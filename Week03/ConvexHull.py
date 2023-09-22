import math
import timeit
import random


# Given a list of points (x, y)
#   find the convex hull using Graham's Scan
# Return a list of points in the convex hull in ccw order
def grahamScan(points):

    result = []

    # step1. 우측하단점 찾고, 결과 리스트에 삽입
    start_point = points[0]

    for point in points:
        if point[1] < start_point[1]:
            start_point = point
        elif point[1] == start_point[1]:
            if point[0] > start_point[0]:
                start_point = point


    # step2. 각 지점의 (인덱스, 각) 튜플 구하기
    angle_list = []

    for index in range(len(points)):
        target_point = points[index]
        angle = math.atan2(target_point[1]-start_point[1], target_point[0]-start_point[0])/math.pi*180
        dist = math.pow((target_point[1]-start_point[1]),2) + math.pow((target_point[0]-start_point[0]),2)
        angle_list.append((index, angle, dist))

    
    # step3. 각를 기준으로 점 정렬하기
    sorted_angle_list = sorted(angle_list, key = lambda p: (p[1], p[2]))

    # step4. convex hull에 포함하는 점 찾아 추가하기
    result.append(start_point)

    for index in range(1, len(sorted_angle_list)):
        k = points[sorted_angle_list[index][0]]

        while True:
            if len(result) > 1:
                i = result[-2]
                j = result[-1]

                det = (j[0] - i[0])*(k[1] - i[1]) - (j[1] - i[1])*(k[0] - i[0])

                if det > 0:
                    break
                else:
                    result.pop()
            else:
                break

        result.append(k)


    # step5. 마지막 점 검사하기
    k = start_point

    while True:
        if len(result) > 1:
            i = result[-2]
            j = result[-1]

            det = (j[0] - i[0])*(k[1] - i[1]) - (j[1] - i[1])*(k[0] - i[0])

            if det > 0:
                break
            else:
                result.pop()
        else:
            break
    
    return result


def correctnessTest(intput, expected_output, correct):
    output = grahamScan(input)
    print(f"grahamScan({input})\n{output}")
    if output == expected_output: print("Pass")
    else:        
        print(f"Fail - expected output: {expected_output}")
        correct = False
    print()    

    return correct


def simulateNSquare(points):    
    points = sorted(points, key = lambda p: (p[1], -p[0])) 
    result = []
    for i in range(len(points)):
        points_with_angle = []
        for j in range(i+1, len(points)):
            x, y = points[j]
            points_with_angle.append((x, y, math.atan2(y - points[i][1], x - points[i][0])))
        points_with_angle = sorted(points_with_angle, key = lambda p: p[2])


'''
Unit Test
'''
if __name__ == "__main__":
    '''# ccw turns
    print(ccw((0,0), (-1,1), (-2, -1)))
    print(ccw((-1,1), (-2, -1), (0,0)))
    print(ccw((-2, -1), (0,0), (-1,1)))

    # non-ccw turns
    print(ccw((0,0), (-2, -1), (-1,1)))
    print(ccw((-2, -1), (-1,1), (0,0)))
    print(ccw((-1,1), (0,0), (-2, -1)))
    print(ccw((0,0), (-1, 1), (-2, 2))) # Straight line'''

    print("Correctness test for grahamScan()")
    print("For each test case, if your answer does not appear within 5 seconds, then consider that you failed the case")
    print()
    correct = True
    
    input = [(3, -1), (2, -2), (4, -1)]
    expected_output = [(2, -2), (4, -1), (3, -1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(0, 0), (-2, -1), (-1, 1), (1, -1), (3, -1), (-3, -1)]
    expected_output = [(3, -1), (-1, 1), (-3, -1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(4, 2), (3, -1), (2, -2), (1, 0), (0, 2), (0, -2), (-1, 1), (-2, -1), (-2, -3), (-3, 3), (-4, 0), (-4, -2), (-4, -4)]
    expected_output = [(-4, -4), (2, -2), (3, -1), (4, 2), (-3, 3), (-4, 0)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(2, 0), (2, 2), (1, -1), (0, 2), (-1, 1), (-2, -2)]
    expected_output = [(-2, -2), (1, -1), (2, 0), (2, 2), (0, 2), (-1, 1)]
    correct = correctnessTest(input, expected_output, correct)

    input = [(2, 0), (2, 2), (1, -1), (0, 2), (-1, 1), (-2, -2), (-2, 2), (4, -4)]
    expected_output = [(4, -4), (2, 2), (-2, 2), (-2, -2)]
    correct = correctnessTest(input, expected_output, correct)

    # "342235" is a 6-digit number and is greater than the other 5-digit numbers
    input = [(342235, -23412), (-74545, 72345), (25812, -45689), (-45676, 24578), (45689, 0), (-74545, 0), (0, 45689), (0, -45689)]
    expected_output = [(25812, -45689), (342235, -23412), (-74545, 72345), (-74545, 0), (0, -45689)]
    correct = correctnessTest(input, expected_output, correct)
    
    print()
    print("Speed test for grahamScan()")
    if not correct: print("Fail (since the algorithm is not correct)")
    else:
        repeat = 10
        inputLength = 100
        minC, maxC = -1000000, 1000000
        points = [(random.randint(minC, maxC), random.randint(minC, maxC)) for _ in range(inputLength)]
        tSubmittedCode = timeit.timeit(lambda: grahamScan(points), number=repeat) / repeat
        tCodeToCompare = timeit.timeit(lambda: simulateNSquare(points), number=repeat) / repeat
        print(f"Average running time of grahamScan() and simulateNSquare() with {inputLength} points: {tSubmittedCode:.10f} and {tCodeToCompare:.10f}")                
        if tSubmittedCode < tCodeToCompare * 0.1: print("Pass")
        else:
            print("Fail")
        print()