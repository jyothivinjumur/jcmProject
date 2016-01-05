
import sys
from fpaCTS import cm


def main(argv):
    try:
        gcm=cm()
        rcm={}
        for i in range(1,11):
            #tfn='/Users/jyothi/Documents/Research/jvdofs/rcv1v2/prjfiles/workdir/testfiter'+str(i)+'.dat'
            #pfn='/Users/jyothi/Documents/Research/jvdofs/rcv1v2/prjfiles/workdir/predsiter'+str(i)+'.dat'
            workDir=argv[0]
            tfn=argv[1]+str(i)+'.dat'
            pfn=argv[2]+str(i)+'.dat'
            rcm[i]=gcm.getCM(tfn,pfn)
        thetaEstLL=gcm.estimateLowerLimit(workDir,rcm,804414,argv[3])
        print thetaEstLL
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])

