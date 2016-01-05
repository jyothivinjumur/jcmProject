__author__ = 'jyothi'

import itertools
import cPickle

class HumanAnnotator:
    def __init__(self):
        """
        """
        self.lamda_Responsive=2.0 # cost of annotating a single document for responsiveness = $2 per document ($60 per hour; 30 docs labeled per hour)
        self.lamda_Privilege=5.0  # cost of annotating a single document for privilege = $5 per document      ($150 per hour; 30 docs labeled per hour)


    def getRPOSCorrectionCost(self,costMatrix, dstat):
        """
        Equation 10 In JointCostProposal
        """
        deltaRPOS=0.0

        val=self.lamda_Responsive+(costMatrix[1][3] ) # get even Priv Probabilities here.

        return deltaRPOS

    def getRNEGCorrectionCost(self,costMatrix, dstat):
        """
        Equation 11 In JointCostProposal
        """
        deltaRNEG=0.0

        return deltaRNEG


    def getAnnotationCost(self,rankedFile, docStatTupleFile,costMatrix):
        #rankedDocList=cPickle.load(open(rankedFile,'rb'))
        #docStatTuple=cPickle.load(open(docStatTupleFile,'rb'))
        rankedDocList=[(130613, 1.3837831539306467e-06), (1092071, 1.3837831539306467e-06), (763188, 1.3837831539441656e-06), (1249710, 1.3837831539441656e-06), (289239, 1.3837831539456284e-06), (1059928, 1.3837831539456284e-06), (68237, 1.383783153957112e-06), (1383586, 1.383783153957112e-06), (575265, 1.3837831540326458e-06), (1396894, 1.3837831540326458e-06)]
        docStatTuple={}
        docStatTuple[130613]=(0.9,1.89,1)
        docStatTuple[1092071]=(0.1,-0.79,1)
        docStatTuple[763188]=(0.5,-0.09,0)
        docStatTuple[1249710]=(0.6,0.69,0)
        docStatTuple[289239]=(0.2,-0.19,1)
        docStatTuple[1059928]=(0.8,1.9,1)
        docStatTuple[68237]=(0.4,-0.9,1)
        docStatTuple[1383586]=(0.34,-0.79,0)
        docStatTuple[575265]=(0.51,1.9,0)
        docStatTuple[1396894]=(0.25,-0.9,1)

        delRPOS={}
        delRNEG={}

        for (rLK,rLV) in rankedDocList:
            if((docStatTuple[rLK][0] > 0.5) and (docStatTuple[rLK][2] == 1)):
                print "NO Change in Annotation. True Positive", rLK
            elif ((docStatTuple[rLK][0] < 0.5) and (docStatTuple[rLK][2] == 1)):
                print "False Negative Correction Cost Function", rLK
                delRNEG[rLK]=self.getRNEGCorrectionCost(costMatrix,docStatTuple[rLK])
                print delRNEG[rLK]
            elif ((docStatTuple[rLK][0] > 0.5) and (docStatTuple[rLK][2] == 0)):
                print "False Positive Correction Cost Function", rLK
                delRPOS[rLK]=self.getRPOSCorrectionCost(costMatrix,docStatTuple[rLK])
                print delRPOS[rLK]
            elif ((docStatTuple[rLK][0] < 0.5) and (docStatTuple[rLK][2] == 0)):
                print "NO Change in Annotation. True Negative", rLK






