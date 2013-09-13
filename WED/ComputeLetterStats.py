#!/usr/bin/env python
from pprint import pprint
import math

#***********************************************************************
#Compute Letter to Letter statistics
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


class Levenshtein(object):
    OPS = ["I", "D", "S", "K"]
    INS, DEL, SUB, KEEP = OPS

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        self.Q = self._matrix()

    def _matrix(self):
        Q = [[None]*(len(self.s1)+1) for i in range(len(self.s2)+1)]
        for i in range(len(self.s1)+1):
            Q[0][i] = (i, self.INS)
        for j in range(len(self.s2)+1):
            Q[j][0] = (j, self.DEL)
        for i, c1 in enumerate(self.s1):
            for j, c2 in enumerate(self.s2):
                # compute options for Q[j+1][i+1]
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

    def dist(self):
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
    #parser.add_argument('string1')
    #parser.add_argument('string2')
    parser.add_argument('filename')
    parser.add_argument('OddMatrix')
    parser.add_argument('InsertionMatrix')
    parser.add_argument('DeletionMatrix')
    pj ={} #count j in the correct
    pi={}  # count i in the wrong
		
    mij = {} #count statistics for letter i transformed into j in the correct
    di = {} #count statistics for deleted letters
    insj = {} #count statistics for inserted letters
    args = parser.parse_args(sys.argv[1:])

    file = open(args.filename,'r')
    # the input file from which we want to extract statistics should have this format:
    # $correctWord1
    # mispelledWord1 
    # mispelledWord1
    # ...
    # $correctWord2
    # mispelledWord2
    # ...	

    oddMFile = open(args.OddMatrix, 'w')
    insMFile = open(args.InsertionMatrix, 'w')
    delMFile = open(args.DeletionMatrix, 'w')

    c=0
    while 1:
        line = file.readline()
        if not line:
                break
        pass # do something     
        w = line.split("\n")[0].strip().split("\t")[0]
	if(w.startswith("$")):
		correct = w
	elif(len(correct) !=0):
		wrong = w
		#Run LEV and update stats
		corr = correct[1:].lower()
		wrg = wrong.lower()
		mylev = Levenshtein( corr, wrg)
		print "Correct: "+corr + " Wrong: "+wrg 
		print mylev.dist()
    		print mylev.editops()
		#UPDATE STATS
		align = mylev.editops()
		#for i in range(len(align)):
		corC = 0
		wrgC = 0
		i=0
		while(i < len(align)):
			print align[i]
			#k= wrg[wrgC]+corr[corC]
			if align[i] == "K":
				print wrg[wrgC]
				print corr[corC]
				#i=i+1	
				#wrgC = wrgC + 1
				#corC = corC + 1
				k = wrg[wrgC]+corr[corC]	
				if(mij.has_key(k) == False):
					mij[k]=1
				else:
					mij[k] += 1
				if(pi.has_key(wrg[wrgC]) == False ):
					pi[wrg[wrgC]] =1
				else:
					pi[wrg[wrgC]] +=1

                                if(pj.has_key(corr[corC]) == False ):
                                        pj[corr[corC]] =1
                                else:
                                        pj[corr[corC]] +=1
				
				wrgC = wrgC + 1
                                corC = corC + 1

				
			elif (align[i] == "S"):
				#i=i+1	
                                print wrg[wrgC]
                                print corr[corC]
				
                                
                                k = wrg[wrgC]+corr[corC]
                                if(mij.has_key(k) == False):
                                        mij[k]=1
                                else:
                                        mij[k] += 1
                                if(pi.has_key(wrg[wrgC]) == False ):
                                        pi[wrg[wrgC]] =1
                                else:
                                        pi[wrg[wrgC]] +=1

                                if(pj.has_key(corr[corC]) == False ):
                                        pj[corr[corC]] =1
                                else:
                                        pj[corr[corC]] +=1					

				wrgC = wrgC + 1
                                corC = corC + 1
				
				

			elif (align[i] == "I"):
				#inserted into the correct 	
                                #print wrg[wrgC]
				print corr[corC]
                                print ""
				#i = i+1

                                
                                if(pj.has_key(corr[corC]) == False ):
                                        pj[corr[corC]] =1
                                else:
                                        pj[corr[corC]] +=1

				if(insj.has_key(corr[corC]) == False ):
                                        insj[corr[corC]] =1
                                else:
                                        insj[corr[corC]] +=1


				corC = corC +1
			elif(align[i] == "D"):
				#deleted from the misspelled
				#i = i+1

                                if(di.has_key(wrg[wrgC]) == False ):
                                        di[wrg[wrgC]] =1
                                else:
                                        di[wrg[wrgC]] +=1

				if(pi.has_key(wrg[wrgC]) == False ):
                                        pi[wrg[wrgC]] =1
                                else:
                                        pi[wrg[wrgC]] +=1
                                

                                print ""
                                #print corr[corC]
				print wrg[wrgC]
				wrgC = wrgC + 1
			print "i: "+str(i)
			print "corC: "+str(corC)
			print "wrgC: "+str(wrgC)
			i = i + 1	
		wrong = ""
	c = c +1

    print c

pprint(mij)

pprint(pj)

pprint(di)

pprint(insj)


Odds = {}

for kk in mij.keys():
	
	val = (float(mij[kk])/float(pj[kk[1]]))
	#print kk+" "+kk[1]+" "+str(val)
	Odds[kk] =val; 
	oddMFile.write(kk+" "+str(val)+"\n")
	oddMFile.flush()
pprint(Odds)
oddMFile.close()

condDel = {}

for kkk in di.keys():
	valD = (float(di[kkk])/float(pi[kkk]))
        print kkk+" "+str(valD)+ " " + str(di[kkk])+" "+str(pi[kkk])
        condDel[kkk] =valD;
	insMFile.write(kkk + " "+str(valD)+"\n")
insMFile.close()
#pprint(condDel)

condIns = {}
print len(di)
print len(insj)

for kkkk in insj.keys():
        valI = (float(insj[kkkk])/float(pj[kkkk]))
        print kkkk+" "+str(valI)+ " " + str(insj[kkkk])+" "+str(pj[kkkk])
        condIns[kkkk] =valI;
	delMFile.write(kkkk+" "+str(valI)+"\n")
delMFile.close()

