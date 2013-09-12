#!/usr/bin/env python
#***********************************************************************
# ngram based Jaccard Distance
#Copyright (C) 2013 Matecat (ICT-2011.4.2-287688).

#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.

#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#***********************************************************************
# Author: Marco Turchi (Fondazione Bruno Kessler, Trento Italy)
# Date: 11/09/2013

from wordfeature import WordFeature
class Jaccard(WordFeature):
    """ Extracts character ngrams and computes Jaccard distance """
    _name = "JaccardDistance"

    def __init__(self, ngramOrd):
        assert ngramOrd > 0, "ngram size must be positive"
        self.ngramOrd = int(ngramOrd)

    def _ngrams(self, s, verbose=False):
        if verbose and len(s) - self.ngram < 0:
            sys.stderr.write("word '%s' too short to extract %d-grams.\n" \
                                                            %(s, self.ngram))
        return [s[i:i+self.ngramOrd] for i in range(len(s) - self.ngramOrd+1)]

    def value(self, word1, word2):
        ngrams1 = set(self._ngrams(word1))
        ngrams2 = set(self._ngrams(word2))
        #print ngrams1, ngrams2
        ngram_intersection = ngrams1.intersection(ngrams2)
        ngram_union = ngrams1.union(ngrams2)

        jaccard = 1.0
        if ngram_union:
            jaccard = 1 - float(len(ngram_intersection))/float(len(ngram_union))
        return jaccard

if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('correctWord')
    parser.add_argument('wrongWord')
    parser.add_argument('ngramOrder', type=int, default=3)

    args = parser.parse_args(sys.argv[1:])

    myJac = Jaccard(args.ngramOrder)
    print myJac.value(args.correctWord, args.wrongWord)
