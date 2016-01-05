__author__ = 'jyothi'

import cPickle
import sys



class Allocate:
    def __init__(self):
        self.Identifiers={} # key=Linenumber , value=Docid
        self.featureLabData={} #key=Docid, value = feature and content


    def readCatfile(self,combinedCatFilePath,dumpPath):
        f=open(combinedCatFilePath,'r')
        fDat = f.readlines()
        f.close()
        fcounter=1
        for catFileline in fDat:
            self.featureLabData[fcounter]=catFileline
            fcounter=fcounter+1
        cPickle.dump(self.featureLabData,open(dumpPath, "wb"))

    def allocateTrain(self,CatPickleFilePath,trainFilePath,tIdsf):
        fcatdat=cPickle.load(open(CatPickleFilePath,'rb'))
        f=open(tIdsf,'r')
        fDat = f.readlines()
        f.close()
        trainIDS=set()
        for fD in fDat:
            ids=fD.split(' ')
            for id in ids:
                trainIDS.add(int(id.strip('\n')))

        writeBuffer = open(trainFilePath,'a')
        for tid in trainIDS:
            if tid:
                writeBuffer.write(fcatdat[tid])
        f.close()

    def allocateTest(self,CatPickleFilePath,testFilePath,testIdsf):
        fcatdat=cPickle.load(open(CatPickleFilePath,'rb'))
        f=open(testIdsf,'r')
        fDat = f.readlines()
        f.close()
        trainIDS=set()
        for fD in fDat:
            ids=fD.split(' ')
            for id in ids:
                trainIDS.add(int(id.strip('\n')))
        writeBuffer = open(testFilePath,'a')
        for tid in trainIDS:
            if tid:
                writeBuffer.write(fcatdat[tid])
        f.close()


def main(argv):
    try:
        allc=Allocate()
        allc.readCatfile(argv[0], argv[1])
        allc.allocateTrain(argv[1],argv[2],argv[3])
        allc.allocateTest(argv[1],argv[4],argv[5])
    except:
        raise

if __name__ == "__main__":
    main(sys.argv[1:])
