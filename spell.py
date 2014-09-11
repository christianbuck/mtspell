#!/usr/bin/env python

import re
import sys
import os
import Levenshtein
from itertools import izip
from features.distance import CountFeature, \
                              EditDistanceFeature, \
                              WeightedEditDistanceFeature, \
                              JaroWinklerDistanceFeature, \
                              SoundMapFeature, \
                              SplittedWordFeature
from features.jaccard import Jaccard as JaccardDistanceFeature

# assume utf8 as input
import codecs
sys.stdin = codecs.getreader('UTF-8')(sys.stdin)
sys.stdout = codecs.getwriter('UTF-8')(sys.stdout);

# from norvig.com
def tokens(text):
    #"""List all the word tokens (consecutive letters) in a text.
    #Normalize to lowercase."""
    #return re.findall(u'[a-z]+', text.lower())
    """List all tokens as delimited by whitespace"""
    return text.split()

class Vocabulary(dict):
    def __init__(self, filename, min_count=0):
        sys.stderr.write("reading %s\n" % filename)
        nr = 0
        for line in codecs.open(filename, "r", "utf-8"):
            nr += 1
            # sys.stderr.write("line %i: %s\n" %(nr, line))
            word, count = line.split()
            count = int(count)
            if count >= min_count:
                self[word] = count
        sys.stderr.write("read %d entries from %s with min count %d \n"
                         %(len(self), filename, min_count))

class SpellChecker(object):
    def __init__(self, vocabulary, max_distance=2, allowSplit=False):
        self.words = vocabulary
        self._word_features = []
        self.allow_split = allowSplit
        self.max_distance = max_distance

    def tokens(self, line):
        return line.strip().split()

    def splits(self, text, start=0, L=20):
        "Return a list of all (first, rest) pairs; with start<=len(first)<=L."
        return [(text[:i], text[i:])
               for i in range(start, min(len(text), L)+1)]

    def _make_candidates(self, word, keep_word, max_distance, allow_split):
        candidates = []
        if keep_word:
           candidates.append(word)
        # naive production of close-edit candidates
        for w in self.words:
            # sys.stderr.write("considering distance of %s to %s\n" %(word, w))
            if w != "":
                if Levenshtein.distance(w, word) <= max_distance: # max distance?
                    candidates.append(w)
        if allow_split:
            for leftsplit, rightsplit in self.splits(word):
                if leftsplit and rightsplit:
                    for left_candidate in self._make_candidates(leftsplit,
                                                    keep_word = False,
                                                    max_distance = max_distance-1,
                                                    allow_split = False):
                        for right_candidate in self._make_candidates(rightsplit,
                                                    keep_word = False,
                                                    max_distance = max_distance-1,
                                                    allow_split = False):
                            candidates.append("%s %s" %(left_candidate, right_candidate))
        return list(set(candidates)) # unique candidates

    def register_feature(self, feature):
        self._word_features.append(feature)

    def process(self, sentence):
        "sentence is a string"
        sys.stderr.write("processing: %s\n" % sentence)
        sentence = "%s%s" %(sentence[0].lower(), sentence[1:])
        sentence = tokens(line)
        sys.stderr.write(" tokens: %s\n" % (":".join(sentence)))
        candidates = [self._make_candidates(word, keep_word=True,
                                            max_distance = self.max_distance,
                                            allow_split = self.allow_split) for
                                            word in sentence]
        assert len(sentence) == len(candidates)
        scores = []
        for word, word_candidates in izip(sentence, candidates):
            word_features = self.score(word, word_candidates)
            assert len(word_features) == len(word_candidates)
            scores.append(word_features)
        assert len(sentence) == len(scores)
        return scores, candidates

    def score(self, word, candidates):
        scores = []
        for candidate in candidates:
            scores.append([])
            for feature in self._word_features:
                val = feature.value(word, candidate)
                name = feature.name()
                scores[-1].append( (val, name) )
        return scores

#def write_hypergraph(sentence, filehandle):
#    """ sentence is supposed to be a list of lists, where each position holds
#        all the options for the word at that position """
#    n_vertices = len(sentence) + 2
#    n_edges = sum(map(len, sentence)) + 2
#    filehandle.write("%d %d\n" %(n_vertices, n_edges))
#    filehandle.write("1\n")
#    filehandle.write("<s> ||| \n")
#
#    for word_idx, possibilities in enumerate(sentence):
#        filehandle.write("%d\n" %(len(possibilities)))
#        for candidate in possibilities:
#            features = ["=".join((f, str(val))) for f,val in candidate['features']]
#            word = candidate['correction']
#            filehandle.write("[%d] %s ||| %s\n"
#                             %(word_idx, word, " ".join(features)))
#    filehandle.write("1\n")
#    filehandle.write("[%d] </s> ||| \n" %(n_vertices-2))

def write_hypergraph(scores, word_candidates, filehandle):
    """ sentence is supposed to be a list of lists, where each position holds
        all the options for the word at that position """
    n_vertices = len(scores) + 2
    n_edges = sum(map(len, scores)) + 2
    filehandle.write("%d %d\n" %(n_vertices, n_edges))
    filehandle.write("1\n")
    filehandle.write("<s> ||| \n")
    for word_idx, (possibilities, word) in enumerate(izip(scores, word_candidates)):
        filehandle.write("%d\n" %(len(possibilities)))
        for cand_idx, candidate in enumerate(possibilities):
            features = ["=".join((str(val), str(n))) for n,val in candidate]
            filehandle.write("[%d] %s ||| %s\n"
                             %(word_idx, word[cand_idx], " ".join(features)))
    filehandle.write("1\n")
    filehandle.write("[%d] </s> ||| \n" %(n_vertices-2))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-dist', type=int,
                        help="maximum edit distancce for candidates", default=2)
    parser.add_argument('-mincount', type=int,
                        help="minimum count for dictionary entries", default=100)
    parser.add_argument('-counts', help="dictionary with counts", default="dict/english.counts")
    parser.add_argument('-split', action='store_true', help='allow splits', default=False)
    args = parser.parse_args(sys.argv[1:])


    vocabulary = Vocabulary(args.counts, args.mincount)
    spell_checker = SpellChecker(vocabulary, args.dist, args.split)

    spell_checker.register_feature(EditDistanceFeature())
    # locate our resources/ relative to this very script
    resourcesdir = os.path.dirname(os.path.realpath(__file__))+"/resources/"
    spell_checker.register_feature(WeightedEditDistanceFeature(
        resourcesdir+"OddM", resourcesdir+"InsM", resourcesdir+"DelM" ))
    spell_checker.register_feature(JaroWinklerDistanceFeature())
    spell_checker.register_feature(CountFeature(vocabulary))
    spell_checker.register_feature(SoundMapFeature())
    spell_checker.register_feature(JaccardDistanceFeature(2))
    if args.split:
        spell_checker.register_feature(SplittedWordFeature())

    #for line in sys.stdin:
    while(1):
        line = raw_input()
        line = line.strip()
        corrections, candidates = spell_checker.process(line)
        print write_hypergraph(corrections, candidates, sys.stdout)
