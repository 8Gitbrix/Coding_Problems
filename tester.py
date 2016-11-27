a = [1,-3,2,5,-2,-3,4,6,-5,2]

def find(a):
    currentMax = bestMax = 0
    start = end = 0
    for i in range(0, len(a)):
        currentMax = max(currentMax + a[i], 0)
        bestMax = max(currentMax, bestMax)
        if bestMax ==currentMax and start == 0:
            end = start = i
        if bestMax > 0 and bestMax == currentMax:
            end = i
    print(bestMax)
    print("start ",start, " end ", end)

print(find(a))

print(find([-2,-3,-4,-5])) #if negative array, then max = 0 and start=end=1
