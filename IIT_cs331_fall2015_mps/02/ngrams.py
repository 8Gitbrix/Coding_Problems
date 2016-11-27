"""CS 331 MP2: ngram extractor and passage generator"""

import sys
import random
from pprint import pprint

def get_file_contents(filename):
    """Returns the contents of the specified file as a single string."""
    with open(filename, 'r') as f:
        content = f.read()
    return content

def compute_ngrams(str, n=2):
    """Returns an n-gram dictionary based on tokens from the given string.

    Each key in the dictionary will be a token from the string, and will map to
    a list of tuples of length (n-1) containing tokens that follow it in the
    string. For instance, the string "I really really like cake." will generate
    the following n-gram dictionary, with n=3:

        {'I': [('really', 'really')],
         'really': [('really', 'like'), ('like', 'cake.')]}

    """
    #split the string
    st = tuple(str.split())
    #not list of list but list of tuple..
    gram = [st[x:x+n] for x in range(len(st)-n+1)]
    dgram = {}
    #convert ngram into dictionary:
    for key in gram:
        dgram.setdefault(key[0],[]).append(key[1:])
    return dgram

def gen_passage(ngrams, start=None, min_length=100, max_sentence_length=10):
    """Generates and returns a string based on the provided n-gram dictionary.

    The generated passage of text will start with either the provided start
    token or a randomly selected key from the dictionary, and the following text
    will be based on randomly generated tokens based on n-gram dictionary
    entries. After min_length is reached, the function will look for a place to
    gracefully end the passage --- e.g., after a token ending with a period.

    The following dictionary:

        {'I': [('really', 'really')],
         'really': [('really', 'like'), ('like', 'cake.')]}

    May generate this passage, for instance (with a bit of programmed
    embellishment vis-a-vis punctuation and capitalization):

        I really really like. Really really like. Really really like. Really
        like cake. Really like cake. Really like cake.

    """
    counter = 0
    strn =""
    while counter < max_sentence_length:
        if start == None:
            start = str(random.choice((list(ngrams.keys()))))
        k = random.choice(ngrams[start])
        strn += str.capitalize(start) +" " + " ".join(k)+" "
        #last token/word of selected sequence is the new start token IFF it is a KEY!
        for i in range(min_length):
            start = k[-1]
            if start not in ngrams.keys() and start:
                if "." in start:
                    start = None
                    break
                else:
                    strn+=". "
                    start = None
                #make sure this completely breaks out...
                break
            else:
                k = random.choice(ngrams[start])
                strn+= " ".join(k)
        counter+=1
    print(strn)
    return strn


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python', sys.argv[0], 'NGRAM-LENGTH FILENAME')
        sys.exit(0)

    ngram_len = int(sys.argv[1])
    filename = sys.argv[2]


    ngrams = compute_ngrams(get_file_contents(filename), ngram_len)
    pprint(ngrams) # use for debugging (note: pretty-print for easy inspection)
    #print(gen_passage(ngrams))
