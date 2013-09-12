class WordFeature(object):
    """ Abstract base class of all word-level features """
    _name = "WordFeature"

    def name(self):
        """ Name of the feature. Should not contain spaces """
        return self._name

    def value(self, word, correction):
        """ Feature value, for example a distance """
        return 0
