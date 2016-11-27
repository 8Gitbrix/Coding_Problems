#Ashwin Jeyaseelan 5/23/2016
#Hackerrank: Maximum Element
class Stack: #partial linkedlist implementation of stack------------------------
    class Node:
        def __init__(self, a, b):
            self.data = a
            self.next = b

    def __init__(self):
        self.head = None
        self.max = 0

    def push(self, element):
        if self.head == None or self.max < element:
            self.max = element
        self.head = self.Node(element, self.head) #1st index always = new element

    def pop(self):
        self.head = self.head.next
        temp = self.head.data if self.head != None else 0
        travel = self.head
        while travel != None: #recalculate max value
            if temp < travel.data:
                temp = travel.data
            travel = travel.next
        self.max = temp

    def getMax(self):
        print(self.max)
#input--------------------------------------------------------------------------
n = int(input())
st = Stack()
for _ in range(0, n):
    m = [int(x) for x in input().split()]
    if m[0] == 1:
        st.push(m[1])
    elif m[0] == 2:
        st.pop()
    else:
        st.getMax()
