import fileinput

def test(strn):
    boolCount = 0
    ind = len(strn)-1
    for x in range(len(strn)-1):
        if abs(ord(strn[x+1])-ord(strn[x])) == abs(ord(strn[ind-x])-ord(strn[ind-x-1])):
                 boolCount+=1

    if boolCount== len(strn)-1:
        print ("Funny")
    else:
        print ("Not Funny")

number = int(input())
for i in range(number):
    test(input())
