#!/usr/bin/env python
import re
import sys
import Levenshtein
from operator import itemgetter
import math
import fuzzy

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
    def __init__(self, vocabulary):
        self.words = vocabulary
        self._word_features = []

    def tokens(self, line):
        return line.strip().split()

    def close_words(self, word, max_distance=1):
        candidates = []
        for w in self.words:
            distance = Levenshtein.distance(w, word)
            if distance <= max_distance:
                candidate = {'original':word, 'correction':w, 'features': []}
                for feature in self._word_features:
                    value = feature.value(word, w)
                    candidate['features'].append( (feature.name(), value))
                candidates.append(candidate)

        #candidates.sort(key=itemgetter(1))
        return candidates

    def register_feature(self, feature):
        self._word_features.append(feature)

    def process(self, sentence):
        "sentence is a string"
        sentence = tokens(line)
        sentence = map(spell_checker.close_words, sentence)
        return sentence

class WordFeature(object):
    """ Abstract base class of all word-level features """
    _name = "WordFeature"

    def name(self):
        """ Name of the feature. Should not contain spaces """
        return self._name

    def value(self, word, correction):
        """ Feature value, for example a distance """
        return 0

class EditDistanceFeature(WordFeature):
    _name = "EditDistance"

    def value(self, word, correction):
        return Levenshtein.distance(word, correction)

class CountFeature(WordFeature):
    _name = "Count"

    def __init__(self, vocabulary):
        self.vocabulary = vocabulary

    def value(self, word, correction):
        if not correction in self.vocabulary:
            return 0
        else:
            return self.vocabulary[correction]

class SoundMapFeature(WordFeature):
    """ Uses soundex algorithm to find possible homophones """
    _name = "SoundMap"

    def __init__(self):
        self.soundex = fuzzy.Soundex(4)
        
    def value(self, word, correction):
        return int(self.soundex("%s" %word) == self.soundex("%s" %correction))
    
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
        for candidate in possibilities:
            features = ["=".join((f, str(val))) for f,val in candidate['features']]
            word = candidate['correction']
            filehandle.write("[%d] %s ||| %s\n"
                             %(word_idx, word, " ".join(features)))
    filehandle.write("1\n")
    filehandle.write("[%d] </s> ||| \n" %(n_vertices-2))


if __name__ == '__main__':
    vocabulary = Vocabulary('english.vocab')
    spell_checker = SpellChecker(vocabulary)
    spell_checker.register_feature(EditDistanceFeature())
    spell_checker.register_feature(CountFeature(vocabulary))
    spell_checker.register_feature(SoundMapFeature())
    #for line in sys.stdin:
    while 1:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            break

        if not line:
            break
        else:
            line = line.strip()
            corrections = spell_checker.process(line)
            #print corrections
            print write_hypergraph(corrections, sys.stdout)