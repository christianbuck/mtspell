#!/usr/bin/env python

import sys
import re
from collections import defaultdict

# from norvig.com
def tokens(text):
    """List all the word tokens (consecutive letters or ') in a text."""
    return re.findall("[a-zA-Z']+", text)

def read_voc(filename):
    voc = {}
    for w in open(filename):
        voc[w.strip()] = 0
    return voc

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('vocab', help="file with correct words")
    parser.add_argument('-all', action='store_true', help="keep unseen words")
    args = parser.parse_args(sys.argv[1:])

    valid_words = read_voc(args.vocab)
    voc = defaultdict(int)

    for linenr, line in enumerate(sys.stdin):
        line = line.strip().replace(" 's", "'s")
        if not line:
            continue
        for w in tokens(line):
            #print w
            if w in valid_words or w.lower() in valid_words:
                voc[w] += 1

    if args.all:
        for w in valid_words:
            voc[w] += 0

    for w in voc:
        sys.stdout.write("%s\t%d\n" %(w, voc[w]))

    sys.stderr.write("total count: %d words\n" %(sum(voc.values())))
