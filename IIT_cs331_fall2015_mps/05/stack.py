class Stack:
    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        idx = len(self.data) - 1
        val = self.data[idx]
        del self.data[idx]
        return val

    def __repr__(self):
        return repr(self.data)

    def __len__(self):
        return len(self.data)

def check_parens(str):
    stack = Stack()
    # make a list just to focus on the parentheses of the string
    s = [x for x in str if x in ('(',')','[',']','{','}','<','>')]
    # compute the length only concerning the number of parentheses in the string
    l = len(s)-1
    for c in range(len(s)):
        if s[c] in ('(','{','[','<'):
            stack.push(s[c])
        elif s[c]==')' and s[l-c]=='(' or s[c]==']' and s[l-c]=='[' or s[c]=='}' and s[l-c]=='{' or s[c]=='>' and s[l-c]=='<':
            if stack:
                stack.pop()
            else:
                return False
    if stack:
        return False
    else:
        return True
