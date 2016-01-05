__author__ = 'jyothi'


import math
import cPickle

class Phase1:
    def __init__(self):
        self.lam_r=5.0 # this is the cost value for Lambda_r = $5 per document
        self.lam_p=10.0 # this is the cost value for Lambda_p = $10 per document
        self.costMatrix=[[0 for x in range(3)] for x in range(3)]
        self.costMatrix[0][0] = 0    # lamda(PP)
        self.costMatrix[0][1] = 1.0  # lamda(PL)
        self.costMatrix[0][2] = 1.0  # lamda(PW)
        self.costMatrix[1][0] = 0.1  # lamda(LP)
        self.costMatrix[1][1] = 0    # lamda(LL)
        self.costMatrix[1][2] = 0.5  # lamda(LW)
        self.costMatrix[2][0] = 0.5  # lamda(WP)
        self.costMatrix[2][1] = 0.1  # lamda(WL)
        self.costMatrix[2][2] = 0    # lamda(WW)


    def getProbaility_cP(self,docid,rTup,pTup):
        """
        cP is the class of the responsive non-privileged documents, that should be Produced
        to the requesting party
        """
        return float(rTup[0] * (1.0 - pTup[0]))


    def getProbaility_cL(self,docid,rTup,pTup):
        """
        cL is the class of the responsive privileged documents, that should be filed into the
        privilege Log
        """
        return float(rTup[0] * pTup[0])

    def getProbaility_cW(self,docid,rTup,pTup):
        """
        cW is the class of the non-responsive documents, that should be Withheld by the producing party
        """
        return float((1.0-rTup[0]))


    def rMinimization(self,workDir,rInsDPL,pInsDPL,trainCount):
        #Equation 1
        respInsDPL=cPickle.load(open(rInsDPL,'rb'))
        privInsDPL=cPickle.load(open(pInsDPL,'rb'))
        cP={}
        cL={}
        cW={}
        docIDS=respInsDPL.keys()
        for docid,tupVal in respInsDPL.iteritems():
            cPVal=self.getProbaility_cP(docid,respInsDPL[docid],privInsDPL[docid])
            cLVal=self.getProbaility_cL(docid,respInsDPL[docid],privInsDPL[docid])
            cWVal=self.getProbaility_cW(docid,respInsDPL[docid],privInsDPL[docid])
            cP[docid]=cPVal
            cL[docid]=cLVal
            cW[docid]=cWVal

        #cP[0]=0.1 ;cP[1]=0.2 ;cL[0]=0.01 ;cL[1]=0.9 ; cW[0]=0.005 ;cW[1]=0.001

        cPickle.dump(cP,open(workDir+"/pickleFiles/docid-cP-probValue.dictionary."+str(trainCount)+".p", "wb"))
        cPickle.dump(cL,open(workDir+"/pickleFiles/docid-cL-probValue.dictionary."+str(trainCount)+".p", "wb"))
        cPickle.dump(cW,open(workDir+"/pickleFiles/docid-cW-probValue.dictionary."+str(trainCount)+".p", "wb"))

        risk_D_P={}
        risk_D_L={}
        risk_D_W={}

        for did in docIDS:
            hP_did=0.0
            hL_did=0.0
            hW_did=0.0
            i=0# i=0 ==> P
            for j in range(0,3): #0==>P, 1==>L, 2==>W
                if j==0:
                    hP_did=hP_did+self.costMatrix[i][j]* cP[did]
                elif j==1:
                    hP_did=hP_did+self.costMatrix[i][j]* cL[did]
                else:
                    hP_did=hP_did+self.costMatrix[i][j]* cW[did]
            i=1 # i=1 ==> L
            for j in range(0,3): #0==>P, 1==>L, 2==>W
                if j==0:
                    hL_did=hL_did+self.costMatrix[i][j]* cP[did]
                elif j==1:
                    hL_did=hL_did+self.costMatrix[i][j]* cL[did]
                else:
                    hL_did=hL_did+self.costMatrix[i][j]* cW[did]
            i=2 # i=2 ==> W
            for j in range(0,3): #0==>P, 1==>L, 2==>W
                if j==0:
                    hW_did=hW_did+self.costMatrix[i][j]* cP[did]
                elif j==1:
                    hW_did=hW_did+self.costMatrix[i][j]* cL[did]
                else:
                    hW_did=hW_did+self.costMatrix[i][j]* cW[did]


            frMC=min(hP_did,hL_did,hW_did)
            if frMC==hP_did:
                risk_D_P[did]=hP_did
            elif frMC==hL_did:
                risk_D_L[did]=hL_did
            else:
                risk_D_W[did]=hW_did

        print "Total number of Documents to be Produced: ",len(risk_D_P)
        print "Total number of Documents to be Logged: ",len(risk_D_L)
        print "Total number of Documents to be Withdrawn: ",len(risk_D_W)

        cPickle.dump(risk_D_P,open(workDir+"/pickleFiles/docid-D_P-risk.dictionary."+str(trainCount)+".p", "wb"))
        cPickle.dump(risk_D_L,open(workDir+"/pickleFiles/docid-D_L-risk.dictionary."+str(trainCount)+".p", "wb"))
        cPickle.dump(risk_D_W,open(workDir+"/pickleFiles/docid-D_W-risk.dictionary."+str(trainCount)+".p", "wb"))


    def ComputeDelta_or(self,cpfile,clfile,cwfile,DELTAOP):
        """ Equation 14 Components """
        cP=cPickle.load(open(cpfile,'rb'))
        cL=cPickle.load(open(clfile,'rb'))
        cW=cPickle.load(open(cwfile,'rb'))
        docIDS=cP.keys()
        delor_P={}
        delor_L={}
        delor_W={}
        #Confirm the if condition
        for did in docIDS:
            if DELTAOP.__contains__(did):
                if DELTAOP[did] <0:
                    delor_P[did]=self.getDeltaor_P(cP[did],cL[did],cW[did],1)
                    delor_L[did]=self.getDeltaor_L(cP[did],cL[did],cW[did],1)
                    delor_W[did]=self.getDeltaor_W(cP[did],cL[did],cW[did],1)
                else:
                    delor_P[did]=self.getDeltaor_P(cP[did],cL[did],cW[did],0)
                    delor_L[did]=self.getDeltaor_L(cP[did],cL[did],cW[did],0)
                    delor_W[did]=self.getDeltaor_W(cP[did],cL[did],cW[did],0)
            else:
                delor_P[did]=self.getDeltaor_P(cP[did],cL[did],cW[did],0)
                delor_L[did]=self.getDeltaor_L(cP[did],cL[did],cW[did],0)
                delor_W[did]=self.getDeltaor_W(cP[did],cL[did],cW[did],0)

        return(delor_P,delor_L,delor_W)


    def getDeltaor_P(self,prb_cP,prb_cL,prb_cW,dopValue):
        """ (lamda_r * P(cP|d)) + (lamda_r * P(cL|d)) + ((lamda_WW - lamda_PW + lamda_r - lamda_p [if dop_pValue==1])*P(cW|d)) """
        value= float((self.lam_r * prb_cP) + (self.lam_r * prb_cL) + ((self.costMatrix[2][2] - self.costMatrix[0][2] + self.lam_r - (self.lam_p * dopValue)) * prb_cW ))
        return value


    def getDeltaor_L(self,prb_cP,prb_cL,prb_cW,dopValue):
        """(lamda_r * P(cP|d)) + (lamda_r * P(cL|d))+ ( (lamda_WW - lamda_LW + lamda_r - lamda_p [if dop_lValue==1])*P(cW|d)) """
        value=float((self.lam_r * prb_cP) + (self.lam_r * prb_cL) + ((self.costMatrix[2][2] - self.costMatrix[1][2] + self.lam_r - (self.lam_p * dopValue)) * prb_cW ))
        return value

    def getDeltaor_W(self,prb_cP,prb_cL,prb_cW,dopValue):
        """ (((lamda_PP - lamda_WP + lamda_r + lamda_p[if dop_lValue==1])*P(cP|d))+((lamda_LL - lamda_WL + lamda_r + lamda_p[if dop_lValue==1])*P(cL|d))+(lamda_r * P(cW|P))) """
        value = float(((self.costMatrix[0][0] - self.costMatrix[2][0] + self.lam_r + (self.lam_p * dopValue)) * prb_cP) + ((self.costMatrix[1][1] - self.costMatrix[2][1] + self.lam_r + (self.lam_p * dopValue)) * prb_cL) + (self.lam_r * prb_cW))
        return value

    def ComputeDeltas(self,cpfile,clfile,cwfile,trainCount,workDir,cDPfile,cDLfile):
        cDP=cPickle.load(open(cDPfile,'rb'))
        cDL=cPickle.load(open(cDLfile,'rb'))

        dop_P,dop_L=self.ComputeDelta_op(cpfile,clfile,cwfile)
        # Equation 15
        DELTAOP={}
        dids=dop_P.keys()

        for d in dids:
            if cDP.__contains__(d):
                DELTAOP[d]=dop_P[d]
            elif cDL.__contains__(d):
                DELTAOP[d]=dop_L[d]

        dor_P,dor_L,dor_W=self.ComputeDelta_or(cpfile,clfile,cwfile,DELTAOP)

        # Equation 10
        DELTAOR={}
        for did in dids:
            if cDP.__contains__(did):
                DELTAOR[did]=dor_P[did]
            elif cDL.__contains__(did):
                DELTAOR[did]=dor_L[did]
            else:
                DELTAOR[did]=dor_W[did]

        cPickle.dump(DELTAOP,open(workDir+"/pickleFiles/DELTAOP.dictionary."+str(trainCount)+".p", "wb"))
        cPickle.dump(DELTAOR,open(workDir+"/pickleFiles/DELTAOR.dictionary."+str(trainCount)+".p", "wb"))

    def ComputeDelta_op(self,cpfile,clfile,cwfile):
        cP=cPickle.load(open(cpfile,'rb'))
        cL=cPickle.load(open(clfile,'rb'))
        cW=cPickle.load(open(cwfile,'rb'))

        #Equation 9 Components
        delop_P={}
        delop_L={}

        #if delop_P.__contains__()
        docIDS=cP.keys()
        for did in docIDS:
            delop_P[did]=self.getDeltaop_P(cP[did],cL[did],cW[did])
            delop_L[did]=self.getDeltaop_L(cP[did],cL[did],cW[did])

        return (delop_P,delop_L)



    def getDeltaop_P(self,prb_cP,prb_cL,prb_cW):
        """ v= ((lamda_p * P(cP|d)) + ((lamda_LL -lamda_PL + lamda_r)*P(cL|d)) + ((lamda_WW -lamda_PW + lamda_r)*P(cW|d)) """
        value=float((self.lam_p * prb_cP) + ((self.costMatrix[1][1] - self.costMatrix[0][1] +self.lam_r) * prb_cL) + ((self.costMatrix[2][2] - self.costMatrix[0][2] +self.lam_r) * prb_cW))
        return value

    def getDeltaop_L(self,prb_cP,prb_cL,prb_cW):
        """ v= ((lamda_PP - lamda_LP + lamda_r) * P(cP|d)) + (lamda_p *P(cL|d)) + ((lamda_WW -lamda_LW + lamda_r)*P(cW|d)) """
        value=float(((self.costMatrix[0][0] - self.costMatrix[1][0] + self.lam_r) * prb_cP )  +(self.lam_p * prb_cL) + ((self.costMatrix[2][2] - self.costMatrix[1][2] +self.lam_r) * prb_cW))
        return value




