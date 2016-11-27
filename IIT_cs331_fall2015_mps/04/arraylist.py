class ArrayList:
    """List ADT based around an array as a storage device"""
    def __init__(self):
        self.data = []

    def append(self, x):
        self.data.append(x)
        return self

    def extend(self, seq):
        for i in seq:
            self.append(i)
        return self

    def __repr__(self):
        return repr(self.data)

    def __str__(self):
        return str(self.data)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return 'slice'
        return self.data[idx]

    def __setitem__(self, idx, val):
        self.data[idx] = val

    def __iter__(self):
        class Iteration:
            def __init__(self, data):
                self.data = data
                self.idx = 0

            def __next__(self):
                if self.idx < len(self.data):
                    print('at index', self.idx)
                    self.idx += 1
                    return self.data[self.idx-1]
                raise StopIteration
        return Iteration(self.data)

    # def __iter__(self):
    #     for i in self.data: # using the list's builtin iterator
    #         yield i
    #     for i in range(len(self.data)):
    #         yield self.data[i]
    def __in__(self, x):
        if x in self.data:
            return True
        else:
            return False

    def __add__(self, arr):
        k = self.extend(arr)
        return k

    def __len__(self):
        return len(self.data)

    def count(self,x):
        #cant use + operator, so use an array of counters
        return len([y for y in self.data if y==x])

    def __delitem__(self,i):
        self.data[i:i+1] = []
        return self

    def clear(self):
        self.data = []

    def insert(self,i,x):
        m = ArrayList().extend(self.data[0:i]).append(x)
        self = m .extend(self.data[i:])
        return self

    def remove(self,x):
        #can only delete the first x!
        for a in range(len(self.data)):
            if self[a]==x:
                self.data[a:a+1] = []
                break

        return self

    def pop(self,i=-1):
        m = self[i]
        del self[i]
        return m
