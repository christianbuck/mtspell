from wordfeature import WordFeature
import Levenshtein

class EditDistanceFeature(WordFeature):
    _name = "EditDistance"

    def value(self, word, correction):
        return Levenshtein.distance(word, correction)

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

