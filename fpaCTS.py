__author__ = 'jyothi'

import math
import cPickle
class cm:

    def getCM(self,tfp,pfp):
        tsIns={}
        predp={}
        f = open(tfp,"r+")
        testIns=f.readlines()
        f.close()
        fp = open(pfp,"r+")
        predProb=fp.readlines()
        fp.close()
        ctr=1
        for ti in testIns:
            tif=ti.split(' ',1)
            tsIns[ctr]=int(tif[0])
            ctr=ctr+1
        ctr=1
        for pp in predProb:
            ppv=float(pp)
            predp[ctr]=ppv
            ctr=ctr+1
        CMT=self.getCMhelper(predp,tsIns)
        return CMT

    def getCMhelper(self,pp,tslab):
        tpcnt=0
        tncnt=0
        fpcnt=0
        fncnt=0
        for k,v in pp.iteritems():
            if v<0 and tslab[k]==-1:
                tncnt=tncnt+1
            elif v<0 and tslab[k]==1:
                fncnt=fncnt+1
            elif v>0 and tslab[k]==-1:
                fpcnt=fpcnt+1
            elif v>0 and tslab[k]==1:
                tpcnt=tpcnt+1
        return (tpcnt,fpcnt,fncnt,tncnt)


    def approximateTheta(self,confMat,N_total):
        theta=-1.0
        val= confMat.values()
        infM_tp= float(sum([tup[0] for tup in val]))
        infM_fp= float(sum([tup[1] for tup in val]))
        infM_fn= float(sum([tup[2] for tup in val]))
        infM_tn= float(sum([tup[3] for tup in val]))

        pe=self.getF1(confMat,N_total)

        if pe==0:
            theta=pe
        else:
            n = {}
            r = {}
            N = {}
            R = {}
            Var_R = {}
            r[1]=infM_tp
            n[1]=infM_tp+infM_fp
            r[0]=infM_fn
            n[0]=infM_fn+infM_tn

            for k,v in r.iteritems():
                N[k]=n[k] * N_total / (n[0] + n[1])
                R[k]=r[k] * N_total / (n[0] + n[1])
                Var_R[k] = math.pow(N[k], 2) * r[k] * (1 - r[k] / n[k]) / math.pow(n[k], 2)

            temp = 2 * R[1] / math.pow(R[1] + R[0] + N[1], 2)
            Var_F1_1 = math.pow(2 / (R[1] + R[0] + N[1]) - temp, 2)
            Var_F1_0 = math.pow(temp, 2)
            Var_F1 = Var_F1_1 * Var_R[1] + Var_F1_0 * Var_R[0]
            theta = pe - 1.645 * math.sqrt(Var_F1)
        return theta

    def estimateLowerLimit(self,workDir,rCM,N,trainCount):
        #cPickle.dump(rCM,open("/Users/jyothi/Documents/Research/jvdofs/rcv1v2/prjfiles/pickleFiles/cMat/cMatrix."+str(trainCount)+".p", "wb"))
        cPickle.dump(rCM,open(workDir+"/pickleFiles/cMatrix."+str(trainCount)+".p", "wb"))
        thetaEstLL=self.approximateTheta(rCM,N)
        return thetaEstLL


    def getF1(self,rcm,infPopDenom):
        val= rcm.values()
        infM_tp= float(sum([tup[0] for tup in val]))/infPopDenom
        infM_fp= float(sum([tup[1] for tup in val]))/infPopDenom
        infM_fn= float(sum([tup[2] for tup in val]))/infPopDenom

        f1=0.0
        if (infM_tp+infM_fn) == 0:
            recall=0.0
            precision=0.0
            f1=0.0
        else:
            recall=float(infM_tp/(infM_tp+infM_fn))
            precision = float(infM_tp/(infM_tp+infM_fp))
            f1=2*float((precision*recall)/(precision+recall))
        return f1


    def getRecall(self,rcm, infPopDenom):
        val= rcm.values()
        infM_tp= float(sum([tup[0] for tup in val]))/infPopDenom
        infM_fp= float(sum([tup[1] for tup in val]))/infPopDenom
        infM_fn= float(sum([tup[2] for tup in val]))/infPopDenom
        infM_tn= float(sum([tup[3] for tup in val]))/infPopDenom

        if (infM_tp+infM_fn) == 0:
            recall=0.0
        else:
            recall=float(infM_tp/(infM_tp+infM_fn))

        precision = float(infM_tp/(infM_tp+infM_fp))
        #print "Precision= ",precision
        return recall






