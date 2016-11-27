def insertion_sort(vals):
    """Insertion sort implementation"""
    for j in range(1, len(vals)):
        to_insert = vals[j]
        i = j - 1
        while i >= 0 and vals[i] > to_insert:
            vals[i+1] = vals[i]
            i -= 1
        vals[i+1] = to_insert

def merge(l1, l2):
    """Merges two sorted lists into a single sorted list, which is returned"""
    res = []
    while l1 and l2:
        if l1[0] < l2[0]:
            res.append(l1.pop(0))
        else:
            res.append(l2.pop(0))
    res.extend(l1 if l1 else l2)
    return res

def divide_sort(l):
    """Splits list in two, insertion sorts each half, then merges"""
    c = len(l) // 2
    l1 = l[:c]
    l2 = l[c:]
    insertion_sort(l1)
    insertion_sort(l2)
    return merge(l1, l2)

def merge_sort(vals):
    """Recursive mergesort implementation"""
    if len(vals) <= 1:
        return vals
    c = len(vals) // 2
    return merge(merge_sort(vals[0:c]), merge_sort(vals[c:len(vals)]))

### Add your sort algorithm(s) below! ##########################################
def selection_sort(vals):
    for x in range(len(vals)-1,0,-1):
        Max = 0
        for y in range(1,x):
            if vals[y]>vals[Max]:
                Max = y
        temp = vals[x]
        vals[x] = vals[Max]
        vals[Max] = temp
