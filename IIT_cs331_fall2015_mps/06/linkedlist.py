class LinkedList:
    class Link:
        def __init__(self, val, prior=None, next=None):
            self.val = val
            self.prior = prior # makes this a "doubly-linked" list
            self.next = next

    def __init__(self):
        self.head = LinkedList.Link(None) # "sentinel" value
        self.head.next  = self.head
        self.head.prior = self.head
        self.count = 0

    def __normalize_index(self, idx):
        """Normalizes negative indexes to positive values"""
        if idx < 0:
            idx = idx + self.count
            if idx < 0:
                idx = 0
        return idx

    def append(self, x):
        l = LinkedList.Link(x, self.head.prior, self.head)
        self.head.prior.next = l
        self.head.prior = l
        self.count += 1

    def clear(self):
        """Removes all elements from the list"""
        self = LinkedList()
        return(self)

    def count_if(self, x):
        """Returns the number of x's in the list"""
        counter = 0
        for k in self:
            if k == x:
                counter+=1
        return counter

    def extend(self, seq):
        """Appends all elements in seq to the list"""
        for i in seq:
            self.append(i)
        return(self)

    def insert(self, idx, x):
        """Inserts x into the list at idx"""
        if idx > self.count:
            raise IndexError
        idx = self.__normalize_index(idx)
        y = self.head.next
        for i in range(idx+1):
            if i == idx:
                insertLink = self.Link(x,y.prior,y)
                y.prior.next = insertLink
                y.prior = insertLink
                self.count+=1
                break
            y = y.next
        return(self)

    def pop(self, idx=-1):
        """Deletes and returns item at idx"""
        y = self.head.next
        if idx==-1:
            self.head.prior = self.head.prior.prior
            self.head.prior.next = self.head
            self.count-=1
        else:
            idx = self.__normalize_index(idx)
            if idx > self.count:
                raise IndexError
            for i in range(idx+1):
                if i==idx:
                    y.prior.next = y.next
                    y.next.prior = y.prior
                    self.count-=1
                    break
                y = y.next
        return(y.val)

    def prepend(self, x):
        l = LinkedList.Link(x, self.head, self.head.next)
        self.head.next.prior = l
        self.head.next = l
        self.count += 1

    def remove(self, x):
        """Deletes the first instance of x; raises ValueError if not found"""
        y = self.head.next
        flag = False
        for _ in range(self.count):
            if x == y.val:
                y.prior.next = y.next
                y.next.prior = y.prior
                self.count-=1
                flag = True
                break
            y = y.next
        if flag == False:
            raise ValueError

    def __add__(self, other):
        """Supports lst1 + lst2"""
        m = LinkedList()
        m.extend(self)
        m.extend(other)
        return m

    def __contains__(self, x):
        """Supports x in lst"""
        for i in self:
            if x == i:
                return True
        return False

    def __delitem__(self, idx):
        """Supports del lst[idx]"""
        idx = self.__normalize_index(idx)
        if idx > self.count:
            raise IndexError
        y = self.head.next
        for i in range(idx+1):
            if i==idx:
                y.prior.next = y.next
                y.next.prior = y.prior
                self.count-=1
                break
            y = y.next

    def __getitem__(self, idx):
        """Supports lst[i] (read)"""
        idx = self.__normalize_index(idx)
        if idx > self.count - 1:
            raise IndexError
        y = self.head.next
        for i in range(idx+1):
            if i==idx:
                return y.val
            y = y.next

    def __iter__(self):
        l = self.head.next
        while l is not self.head:
            yield l.val
            l = l.next

    def __len__(self):
        return self.count

    def __repr__(self):
        return repr(list(self))

    def __setitem__(self, idx, val):
        """Supports lst[i] = x"""
        idx = self.__normalize_index(idx)
        if idx > self.count - 1:
            raise IndexError
        y = self.head.next
        for i in range(idx+1):
            if i==idx:
                y.val = val
                break
            y = y.next

#test:
k = LinkedList()
for i in range(5):
    k.append(i)
print("k: ", k)
print(k.count_if(3))
la = [3,4,5,6,7]
k.extend(la)
print("After extend k: ", k)
k = k.insert(3,13)
print(k, "After insert ", k.count)
m = k.pop(2)
print(m)
print("After popping", k)
k.append(23)
print(k)
k.remove(4)
print("Get item at index 7", k[7])
k[7] = 41
print("Set item at index 7", k)
u = [147,12,23]
k+ u
print(k)
k.clear()
print(k)
