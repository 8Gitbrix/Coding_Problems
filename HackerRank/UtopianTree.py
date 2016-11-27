#Ashwin Jeyaseelan 5/24/2016
#Utopian Tree
def rec(x):
    if x == 0:
        return 1
    elif x == 1:
        return 2
    else:
        if x % 2 == 0:
            return 1 + rec(x-1)
        else:
            return 2 * rec(x-1)

#input:
t = int(input())
for _ in range(0, t):
    print(rec(int(input())))
