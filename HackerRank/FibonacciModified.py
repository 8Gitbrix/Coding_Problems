#Fibonacci Modified
def fibModified(a, b, n):
    if n == 3:
        return a + b*b
    return fibModified(b, b*b + a, n-1)

a, b, c = (int(x) for x in input().split())
print(fibModified(a,b,c))
