__author__ = 'jyothi'

import cPickle
import math



class Phase2:
    def __init__(self):
        self.lam_r=5.0 # this is the cost value for Lambda_r = $5 per document
        self.lam_p=10.0 # this is the cost value for Lambda_p = $10 per document
        self.rankedDeltaOR=[]
        self.k_limit_percent=0.1


    def run(self,cpfile,clfile,cwfile,deltaorDictionaryFile,rJudgments):
        rJ={}
        rRJ = open(rJudgments, "r")
        rRJls=rRJ.readlines()
        rRJ.close()
        did=1
        for rRJln in rRJls:
            rJ[did]=int(rRJln.strip('\n'))
            did=did+1
        cost_a=0.0
        cP=cPickle.load(open(cpfile,'rb'))
        cL=cPickle.load(open(clfile,'rb'))
        cW=cPickle.load(open(cwfile,'rb'))

        deltaOR=cPickle.load(open(deltaorDictionaryFile,'rb'))

        print deltaOR.values()

        for w in sorted(deltaOR, key=deltaOR.get, reverse=True):
            self.rankedDeltaOR.append(w)
        insl=len(self.rankedDeltaOR)
        stopping_k=int(insl * self.k_limit_percent)
        correctionCounter=-1
        tp=0 ; fp=0 ; tn=0; fn=0
        for i in self.rankedDeltaOR:
            correctionCounter=correctionCounter+1
            if correctionCounter<stopping_k:
                if rJ[i]==1:
                    if not (cP.__contains__(i) or cL.__contains__(i)):
                        #print "FN- ",i
                        fn=fn+1
                    else:
                        tp=tp+1
                else:
                    if not cW.__contains__(i):
                        #print "FP- ",i
                        fp=fp+1
                    else:
                        tn=tn+1
                cost_a=cost_a+self.lam_r

        print "tp= ",tp
        print "fp= ",fp
        print "fn= ",fn
        print "tn= ",tn
        print "cost_a= ",cost_a





