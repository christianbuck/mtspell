#!/usr/bin/env python
import re
import sys
import Levenshtein
from operator import itemgetter
import math

# from norvig.com
def tokens(text):
    """List all the word tokens (consecutive letters) in a text.
    Normalize to lowercase."""
    return re.findall('[a-z]+', text.lower())

class SpellChecker(object):
    def __init__(self, vocab_filename):
        self.words = {}
        for line in open(vocab_filename):
            word, count = line.split()
            self.words[word] = int(count)

    def tokens(self, line):
        return line.strip().split()

    def close_words(self, word, max_distance=2):
        candidates = []
        for w in self.words:
            distance = Levenshtein.distance(w, word)
            if distance <= max_distance:
                candidates.append((w,distance, self.words[w]))
        candidates.sort(key=itemgetter(1))
        return candidates

def write_hypergraph(sentence, filehandle):
    """ sentence is supposed to be a list of lists, where each position holds
        all the options for the word at that position """
    n_vertices = len(sentence) + 2
    n_edges = sum(map(len, sentence)) + 2
    filehandle.write("%d %d\n" %(n_vertices, n_edges))
    filehandle.write("1\n")
    filehandle.write("<s> ||| \n")

    for word_idx, possibilities in enumerate(sentence):
        filehandle.write("%d\n" %(len(possibilities)))
        for word, distance, count in possibilities:
            filehandle.write("[%d] %s ||| Distance=%d LogCount=%f\n"
                             %(word_idx, word, distance, math.log(count)))
    filehandle.write("1\n")
    filehandle.write("[%d] </s> ||| \n" %(n_vertices-2))


if __name__ == '__main__':
    spell_checker = SpellChecker('english.vocab')
    for line in sys.stdin:
        line = line.strip()
        sentence = tokens(line)
        sentence = map(spell_checker.close_words, sentence)
        #print sentence
        write_hypergraph(sentence, sys.stdout)
