__author__ = 'jyothi'

from ModulePhase1 import Phase1
import sys


def main(argv):
    try:
        p1=Phase1()
        wDir= argv[0] # '/Users/jyothi/Documents/Research/jvdofs/rcv1v2/results' #arg[0]
        workDirResponsive=argv[1] # '/Users/jyothi/Documents/Research/jvdofs/rcv1v2/results/C15' #argv[1]
        workDirPrivilege=argv[2] #'/Users/jyothi/Documents/Research/jvdofs/rcv1v2/results/C17'  # argv[2]
        trainCount=argv[3] # 10000#argv[3]
        p1.rMinimization(wDir,workDirResponsive+'/pickleFiles/ds-op-label.tuple.dictionary'+str(trainCount)+'.p',workDirPrivilege+'/pickleFiles/ds-op-label.tuple.dictionary'+str(trainCount)+'.p',trainCount)
        p1.ComputeDeltas(wDir+'/pickleFiles/docid-cP-probValue.dictionary.'+str(trainCount)+'.p',wDir+'/pickleFiles/docid-cL-probValue.dictionary.'+str(trainCount)+'.p',wDir+'/pickleFiles/docid-cW-probValue.dictionary.'+str(trainCount)+'.p',trainCount,wDir,wDir+'/pickleFiles/docid-D_P-risk.dictionary.'+str(trainCount)+'.p',wDir+'/pickleFiles/docid-D_L-risk.dictionary.'+str(trainCount)+'.p')
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])