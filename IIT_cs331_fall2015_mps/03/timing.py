from timeit import timeit
import random
import sort_algs

if __name__ == '__main__':
    # Delete or modify the following code to add your own implementation
    # that generates the required table of sort timings. Note that you
    # should also edit 'sort_algs.py' to add your own sort algorithm.
    print(('{:<5}'+'{:>10}'*4).format('n', 'Insertion', 'Divide', 'Merge', 'Selection'))
    for n_elems in range(100, 2001, 100):
        l = list(range(n_elems))

        def call_insertion_sort():
            random.shuffle(l)
            sort_algs.insertion_sort(l)

        def call_divide():
            random.shuffle(l)
            sort_algs.divide_sort

        def call_merge():
            random.shuffle(l)
            sort_algs.merge_sort(l)

        def call_selection():
            random.shuffle(l)
            sort_algs.selection_sort(l)

        t1 = timeit(call_insertion_sort, number=1000)
        t2 = timeit(call_divide,number =1000)
        t3 = timeit(call_merge,number = 1000)
        t4 = timeit(call_selection,number=1000)

        print(('{:5d}'+'{:10.5f}'*4).format(n_elems,t1,t2,t3,t4))
