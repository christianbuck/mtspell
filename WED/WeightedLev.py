#!/usr/bin/env python
#***********************************************************************
#Word level Jaccard Distance
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
# Author: Marco Turchi (FBK) on the base of the code written by Christian Buck (University of Edinburgh)
# Date: 11/09/2013

from pprint import pprint
import math


class Levenshtein(object):
    OPS = ["I", "D", "S", "K"]
    INS, DEL, SUB, KEEP = OPS

    def __init__(self, OddFile, InsFile, DelFile):
        #self.s1 = s1
        #self.s2 = s2
        #self.Q = self._matrix()
	self.OddD = self._loadFile(OddFile)
	self.InsD = self._loadFile(InsFile)
	self.DelD = self._loadFile(DelFile)

    def _loadFile(self, filename):
	file = open(filename, 'r')
	d = {}
    	while 1:
        	line = file.readline()
        	if not line:
                	break
        	pass # do something     
        	toks = line.split("\n")[0].strip().split(" ")
		k = toks[0]
		val=float(toks[1])
		d[k] =val
	return d

    def _matrix(self):
        Q = [[None]*(len(self.s1)+1) for i in range(len(self.s2)+1)]
        for i in range(len(self.s1)+1):
            Q[0][i] = (i, self.INS)
        for j in range(len(self.s2)+1):
            Q[j][0] = (j, self.DEL)
        for i, c1 in enumerate(self.s1):
            for j, c2 in enumerate(self.s2):
                # compute options for Q[j+1][i+1]
                #insert_cost  = Q[j+1][i][0] + 1
                #delete_cost  = Q[j][i+1][0] + 1
                #replace_cost = Q[j][i][0] + (c1 != c2)
		costIns = 0 
		if(self.InsD.has_key(c1) == True):
			costIns = self.InsD[c1]
		costDel = 0
		if(self.DelD.has_key(c2) == True):
			costDel = self.DelD[c2]
		costOdd = 0
		if(self.OddD.has_key(c1+c2) == True):
			costOdd = self.OddD[c1+c2]
		#print self.weighted
		if(self.weighted == "True"):
                	insert_cost  = Q[j+1][i][0] + (1*costIns)
                	delete_cost  = Q[j][i+1][0] + (1*costDel)
                	replace_cost = Q[j][i][0] + ((c1 != c2)* costOdd)
		else:
			insert_cost  = Q[j+1][i][0] + 1
                        delete_cost  = Q[j][i+1][0] + 1
                        replace_cost = Q[j][i][0] + (c1 != c2)
                cost = [insert_cost, delete_cost, replace_cost]
                best_cost = min(cost)
                best_op = self.OPS[cost.index(best_cost)]
                if best_op == Levenshtein.SUB and c1 == c2:
                    best_op = Levenshtein.KEEP

                Q[j+1][i+1] = (best_cost, best_op)
        self._dist = Q[-1][-1][0]
        return Q

    def __printQ(self, Q):
        for linenr, line in enumerate(Q):
            print linenr, line

    def dist(self, correct, wrong, weighted ):
	self.s1 = wrong
        self.s2 = correct
	self.weighted = weighted
        self.Q = self._matrix()

        return self._dist

    def editops(self):
        """ how to turn s2 into s1 """
        ops = []
        i, j = len(self.Q[0])-1 , len(self.Q)-1
        while i > 0 or j > 0:
            ops.append(self.Q[j][i][1])
            if ops[-1] == self.INS:
                i -= 1
            elif ops[-1] == self.DEL:
                j -= 1
            elif ops[-1] == self.SUB or ops[-1] == self.KEEP:
                i -= 1
                j -= 1
        ops.reverse()
        return ops



if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('correctWord')
    parser.add_argument('wrongWord')
    parser.add_argument('weighted')
    parser.add_argument('OddMatrix')
    parser.add_argument('InsertionMatrix')
    parser.add_argument('DeletionMatrix')

    args = parser.parse_args(sys.argv[1:])

    mylev = Levenshtein( args.OddMatrix, args.InsertionMatrix, args.DeletionMatrix)
    print mylev.dist(args.correctWord, args.wrongWord, args.weighted)
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
