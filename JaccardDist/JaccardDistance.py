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

from pprint import pprint
import math, sys


class Jaccard(object):
    def __init__(self, ngramOrd):
	self.ngram = int(ngramOrd)


    def _extractNgrams(self, s):
	x = len(s)
	l1 = []
	if((x - self.ngram) <0):
		print "word: "+s+" too short for extracting "+str(self.ngram)+"-grams"
		sys.exit(0)
	else:
		for i in range(x-self.ngram+1):
			#for j in range(self.ngram):
			#print i
			ngram = s[i : (i+self.ngram)]
			l1.append(ngram)
			#print ngram
	#pprint(l1)
	return l1
   

    def _dist(self):
	#extract ngrams correct
	l1List = self._extractNgrams(self.s1)
        l2List = self._extractNgrams(self.s2)
	interL = set(l1List).intersection( set(l2List) )
	#print len(interL)
	unionL = set(l1List).union(set(l2List))
	#print len(unionL)
	#pprint(unionL)
	val = 1- float(len(interL))/float(len(unionL))
	return val


    def dist(self, correct, wrong):
	self.s1 = wrong
        self.s2 = correct
	val = self._dist()	
	#print val
        return val




if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('correctWord')
    parser.add_argument('wrongWord')
    parser.add_argument('ngramOrder')  

    args = parser.parse_args(sys.argv[1:])

    myJac = Jaccard(args.ngramOrder)
    print myJac.dist(args.correctWord, args.wrongWord)
    #print mylev.editops

   # file = open(args.filename,'r')

    #oddMFile = open(args.OddMatrix, 'w')
   # insMFile = open(args.InsertionMatrix, 'w')
   # delMFile = open(args.DeletionMatrix, 'w')

#read the file
#compute edit and parse the string and then compute statistics
        



    #mylev = Levenshtein(args.string1, args.string2)
    #print mylev.dist()
    #print mylev.editops()
