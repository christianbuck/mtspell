#!/usr/bin/env python
import re
import sys
import Levenshtein
from itertools import izip
from features.distance import CountFeature, \
                              EditDistanceFeature, \
                              WeightedEditDistanceFeature, \
                              JaroWinklerDistanceFeature, \
                              SoundMapFeature, \
                              SplittedWordFeature
from features.jaccard import Jaccard as JaccardDistanceFeature

# from norvig.com
def tokens(text):
    """List all the word tokens (consecutive letters) in a text.
    Normalize to lowercase."""
    return re.findall('[a-z]+', text.lower())

class Vocabulary(dict):
    def __init__(self, filename):
        for line in open(filename):
            word, count = line.split()
            self[word] = int(count)

class SpellChecker(object):
    def __init__(self, vocabulary, allowSplit):
        self.words = vocabulary
        self._word_features = []
        self.allow_split = allowSplit

    def tokens(self, line):
        return line.strip().split()

    def splits(self, text, start=0, L=20):
        "Return a list of all (first, rest) pairs; with start<=len(first)<=L."
        return [(text[:i], text[i:]) 
               for i in range(start, min(len(text), L)+1)]

    def make_candidates(self, word, keep_word=True, max_distance=2, allow_split=True):
        candidates = []
        if keep_word:
           candidates.append(word)
        for w in self.words:
            if w != "":
                if Levenshtein.distance(w, word) <= max_distance: # max distance?
                    candidates.append(w)
        if allow_split:
            for leftsplit, rightsplit in self.splits(word):
                if leftsplit and rightsplit:
                    for left_candidate in self.make_candidates(leftsplit,
                                                    keep_word=False,
                                                    max_distance = max_distance-1,
                                                    allow_split=False):
                        for right_candidate in self.make_candidates(rightsplit,
                                                    keep_word=False,
                                                    max_distance = max_distance-1,
                                                    allow_split=False):
                            candidates.append("%s %s" %(left_candidate, right_candidate))
        return list(set(candidates)) # unique candidates
    
    def register_feature(self, feature):
        self._word_features.append(feature)

    def process(self, sentence):
        "sentence is a string"
        sentence = tokens(line)
        candidates = map(self.make_candidates,sentence)
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
    vocabulary = Vocabulary('voc.counts')
    allowSplit=True
    spell_checker = SpellChecker(vocabulary, allowSplit)
    spell_checker.register_feature(EditDistanceFeature())
    spell_checker.register_feature(WeightedEditDistanceFeature(
        "resources/OddM", "resources/InsM", "resources/DelM" ))
    spell_checker.register_feature(JaroWinklerDistanceFeature())
    spell_checker.register_feature(CountFeature(vocabulary))
    spell_checker.register_feature(SoundMapFeature())
    spell_checker.register_feature(JaccardDistanceFeature(2))
    if allowSplit:
        spell_checker.register_feature(SplittedWordFeature())

    #for line in sys.stdin:
    while(1):
        line = raw_input()
        line = line.strip()
        corrections, candidates = spell_checker.process(line)
        print write_hypergraph(corrections, candidates, sys.stdout)
