import time
import random
# Note: you shouldn't need to import any additional modules!

def times_table(n, upto):
    """Returns a list of tuples that represent the "times-table" of `n`, up to (and
    including) the multiple `upto`. E.g., the call `times_table(5, 4)` should
    produce the result `[(5, 1, 5), (5, 2, 10), (5, 3, 15), (5, 4, 20)]`

    """
    k = [(n,x,n*x) for x in range(1,upto+1)]
    return k

def time_reverse(nitems, ntimes):
    """Returns the number of seconds it takes to reverse a list of `nitems` items
    `ntimes` times. Should not make use of the `timeit` module --- instead,
    should use the `time` function in the `time` module.

    """
    pass

def shuffle(l):
    """Given a list, "shuffles" it by exchanging items at two randomly generated
    indexes a number of times equal to twice the number of items in the list.
    `random.shuffle` should not be used, but `random.randrange` can be used to
    generate random index values.

    """
    for _ in range(0,len(l)*2):
        randIndex1 = random.randrange(0,len(l)-1,1)
        randIndex2 = random.randrange(0,len(l)-1,1)
        temp = l[randIndex1]
        l[randIndex1] = l[randIndex2]
        l[randIndex2] = temp

    return l

def is_permutation(s, t):
    """Returns true if the sequence `s` is a permutation of the sequence `t`, i.e.,
    if `s` is the same length as `t` and contains all the same elements the same
    number of times (though not necessarily in the same order). Hint: you may
    use the `sorted` built-in function.

    """
    pass

def inverted(d):
    """Given a dictionary `d`, returns a new dictionary where the values of `d` are
    keys, and the corresponding entries are lists of keys that mapped to the
    values in `d`. E.g., calling this function with the argument `{1: 2, 2: 3,
    3: 2}` will return `{2: [1, 3], 3: [2]}`.

    """
    pass

def count_each(l):
    """Given a sequence, returns a dictionary containing each item in the sequence
    as a key whose value is the number of times that item appears in the
    sequence. E.g., calling this function with `'hello there'` will return
    `{'e': 3, 'r': 1, 'h': 2, ' ': 1, 'l': 2, 'o': 1, 't': 1}`.

    """
        counter = 1
        indexFlag = []
        cList = []
        d = {}
        for x in range(0,len(l)):
            #make sure the same character isn't counter again in the second for loop
            #by flagging it in indexFlag!
            if x in indexFlag:
                continue
            for y in range(x+1,len(l)):
                if l[x]==l[y]:
                    counter+=1
                    indexFlag.append(y)
            d[l[x]] = counter
            cList.append(counter)
            counter = 1
        return d


def avg_attempts(n_trials, success_rate=0.5):
    """Simulates an event with a success rate of `success_rate` (which is a fraction
    between 0.0 and 1.0) `n_trials` times, and returns the average number of
    attempts before 'succeeding' in each event. Whether an event "succeeds" can
    be determined by checking whether a random number (generated with
    `random.random()`, say) is greater than or equal to `success_rate`. E.g.,
    calling this function with `n_trials`=1000 and `success_rate`=0.5 will
    return roughly 1.0.

    """
    pass

def ranked_list(d):
    """Called with a list where all keys map to comparable values (e.g., numbers),
    returns a list containing key, value tuples, ordered by the values (in
    descending order). E.g., called with `{'John': 3.8, 'Mary': 3.95, 'Jim':
    3.6, 'Jose': 3.7}`, will return `[('Mary', 3.95), ('John', 3.8), ('Jose',
    3.7), ('Jim', 3.6)]`.

    """
    pass

def piglatinify(s):
    """Called with a string of whitespace separated words, will return the Pig Latin
    version of the string. See https://en.wikipedia.org/wiki/Pig_Latin for the
    rules on transforming English to Pig Latin (use the basic rules). E.g.,
    called with 'I love to eat pretty cakes', should return 'Iyay ovelay otay
    eatyay ettypray akescay'.

    """
    pass

def histogram(ns, scale=10, char='X'):
    """Prints a vertical histogram of the numeric values in the sequence `ns`,
    scaled according to the maximum value in `ns`, using the character
    `char`. E.g., called as `histogram([1, 2, 3, 4, 5], 5, 'X'), should
    output:

                X
              X X
            X X X
          X X X X
        X X X X X

    Called as `histogram([43, 65, 97, 33, 22], 8, 'O')`, should output:

            O
            O
            O
          O O
          O O
        O O O
        O O O O
        O O O O O
    """
    pass
