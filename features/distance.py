from wordfeature import WordFeature
import Levenshtein
from levenshtein import WeightedLevenshtein

class EditDistanceFeature(WordFeature):
    _name = "EditDistance"

    def value(self, word, correction):
        return Levenshtein.distance(word, correction)

class WeightedEditDistanceFeature(WordFeature):
    _name = "WeightedEditDistance"

    def __init__(self, OddFile=None, InsFile=None, DelFile=None):
        self.Levenshtein = WeightedLevenshtein(OddFile, InsFile, DelFile)

    def value(self, word, correction):
        return self.Levenshtein.dist(word, correction)

class JaroWinklerDistanceFeature(WordFeature):
    _name = "JaroWinklerDistance"

    def value(self, word, correction):
        return Levenshtein.jaro_winkler(word, correction)

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
        import fuzzy
        self.soundex = fuzzy.Soundex(4)

    def value(self, word, correction):
        "work around an error in 'fuzzy' which changes the unmutable string"
        return int(self.soundex("%s" %word) == self.soundex("%s" %correction))

class SplittedWordFeature(WordFeature):
    """ Splits word and looks for possible candidates (e.g. mydog => my day, my dog) """
    _name = "SplittedWord"

    def value(self, word, correction):
	return int(" " in correction)

