__author__ = 'jyothi'

import sys
import os
from SimulateCorrection import HumanAnnotator

def main(argv):
    try:
        anntr=HumanAnnotator()
        lamdaR=0.1  #costs of annotating a single document for responsiveness
        lamdaP=0.5  #costs of annotating a single document for responsiveness
        TauR= 10000 # Number of Documents that require Manual Annotation (Where to draw the line)
        TauP= 10000 # Number of Documents that require Manual Annotation (Where to draw the line)


        costMatrix=[[0 for x in range(4)] for x in range(4)]
        costMatrix[0][0] = 0
        costMatrix[1][0] = 0.5
        costMatrix[2][0] = 0.75
        costMatrix[3][0] = 0.75
        costMatrix[0][1] = 1
        costMatrix[0][2] = 1
        costMatrix[0][3] = 1

        print costMatrix
        anntr.getAnnotationCost('/Users/jyothi/Documents/Research/jvdofs/rcv1v2/prjfiles/pickleFiles/docRank.2000.p','',costMatrix)
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])