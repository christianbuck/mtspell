#!/usr/bin/env python
#***********************************************************************
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

class WeightedLevenshtein(object):
    OPS = ["I", "D", "S", "K"]
    INS, DEL, SUB, KEEP = OPS

    def __init__(self, OddFile=None, InsFile=None, DelFile=None):
        self.OddD = self._loadFile(OddFile)
        self.InsD = self._loadFile(InsFile)
        self.DelD = self._loadFile(DelFile)

    def _loadFile(self, filename):
        d = {}
        if filename:
            for line in open(filename):
                k, val = line.rstrip().split()
                d[k] = float(val)
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
                costIns = self.InsD.get(c1, 1)
                costDel = self.DelD.get(c2, 1)
                costOdd = self.OddD.get(c1+c2, 1)

                insert_cost  = Q[j+1][i][0] + costIns
                delete_cost  = Q[j][i+1][0] + costDel
                replace_cost = Q[j][i][0] + (c1 != c2) * costOdd

                cost = [insert_cost, delete_cost, replace_cost]
                best_cost = min(cost)
                best_op = self.OPS[cost.index(best_cost)]
                if best_op == WeightedLevenshtein.SUB and c1 == c2:
                    best_op = WeightedLevenshtein.KEEP

                Q[j+1][i+1] = (best_cost, best_op)
        self._dist = Q[-1][-1][0]
        return Q

    def __printQ(self, Q):
        for linenr, line in enumerate(Q):
            print linenr, line

    def dist(self, correct, wrong):
        " report the cost of turning 'wrong' into 'correct' "
        self.s1 = wrong
        self.s2 = correct
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
    parser.add_argument('-OddMatrix', default=None)
    parser.add_argument('-InsertionMatrix', default=None)
    parser.add_argument('-DeletionMatrix', default=None)

    args = parser.parse_args(sys.argv[1:])

    mylev = WeightedLevenshtein(args.OddMatrix,
                                args.InsertionMatrix,
                                args.DeletionMatrix)
    print mylev.dist(args.correctWord, args.wrongWord)
