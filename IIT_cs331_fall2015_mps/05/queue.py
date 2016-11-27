class Queue:
    def __init__(self, size=10):
        self.data = [None] * size
        self.count = 0
        self.head  = self.tail = 0

    def enqueue(self, x):
        if self.count < len(self.data):
            self.data[self.tail] = x
            self.tail = (self.tail + 1) % len(self.data)
            self.count += 1
        elif self.count >= len(self.data):
            self.expand(1)
            self.data+=[x]

    def expand(self,x):
        for _ in range(x):
            if len(self.data)>=10:
                temp = self.data[0]
                mid = len(self.data)//2
                self.data= self.data[0:mid] + [None] + self.data[mid:]
                #self.tail = (self.tail-1)%len(self.data)
                self.tail = mid-1
                self.data = [self.data[x+1] for x in range(0,len(self.data)-1)]
                self.data+= [temp]
                self.count += 1

            else:
                self.data += [None]

    def dequeue(self):
        if self.count > 0:
            val = self.data[self.head]
            self.data[self.head] = None
            self.head = (self.head + 1) % len(self.data)
            self.count -= 1
            return val

    def __iter__(self):
        for offset in range(self.count):
            yield self.data[(self.head + offset) % len(self.data)]

    def __repr__(self):
        return repr(list(self))
