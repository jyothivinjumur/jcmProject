__author__ = 'jyothi'


import math
import cPickle
import sys

class Probabilities:
    def getCaliberatedProbabilities(self,workDir,trainCount,parameters,tDfilepath,tLfilepath ):
        tInsDPL={}
        testInsScores={}
        testInsLabs={}
        testInsProbabilities={}
        paramFields=parameters.replace('(','').replace(')','').split(',')
        paramA=float(paramFields[0])
        paramB=float(paramFields[1])
        f = open(tDfilepath, 'r')
        lines=f.readlines()
        f.close()
        counter=0
        for l in lines:
            testInsScores[counter]=float(l.strip('\n'))
            counter=counter+1
        fl = open(tLfilepath, 'r')
        labs=fl.readlines()
        fl.close()
        c=0
        for l in labs:
            testInsLabs[c]=int(l.strip('\n'))
            c=c+1
        for k,v in testInsScores.iteritems():
            plattProbability=(float(1.0)/float(1.0 + math.exp((v*paramA)+paramB)))
            testInsProbabilities[k]=plattProbability

        for k,v in testInsProbabilities.iteritems():
            dplTuple=(float(v),float(testInsScores[k]),int(testInsLabs[k]))
            tInsDPL[k]=dplTuple
        cPickle.dump(tInsDPL,open(workDir+"/pickleFiles/ds-op-label.tuple.dictionary"+str(trainCount)+".p", "wb"))

def main(argv):
    try:
        caliberatedProbabilities=Probabilities()
        tup=caliberatedProbabilities.getCaliberatedProbabilities(argv[0],argv[4],argv[1],argv[2], argv[3])
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])
