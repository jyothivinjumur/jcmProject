__author__ = 'jyothi'

from ModulePhase2 import Phase2
import sys


def main(argv):
    try:
        p2=Phase2()
        wd='/Users/jyothi/Documents/Research/jvdofs/rcv1v2/results/jcmFiles/C17/pickleFiles'#argv[0]
        trainCount=40000#argv[1]
        rJFile='/Users/jyothi/Documents/Research/jvdofs/rcv1v2/datFiles/rcv1_C15.txt'#argv[2]
        p2.run(wd+'/docid-D_P-risk.dictionary.'+str(trainCount)+'.p',wd+'/docid-D_L-risk.dictionary.'+str(trainCount)+'.p',wd+'/docid-D_W-risk.dictionary.'+str(trainCount)+'.p',wd+'/DELTAOR.dictionary.'+str(trainCount)+'.p',rJFile)
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])