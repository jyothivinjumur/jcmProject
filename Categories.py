__author__ = 'jyothi'


import os
class CategoryStat:
    def __init__(self):
        self.C13={}
        self.C15={}
        self.C151={}
        self.C152={}
        self.C17={}
        self.C18={}
        self.C181={}
        self.C21={}
        self.C24={}
        self.C31={}
        self.CCAT={}
        self.E12={}
        self.E21={}
        self.E212={}
        self.ECAT={}
        self.GCAT={}
        self.GCRIM={}
        self.GDIP={}
        self.GPOL={}
        self.GSPO={}
        self.GVIO={}
        self.M11={}
        self.M12={}
        self.M13={}
        self.M131={}
        self.M132={}
        self.M14={}
        self.M141={}
        self.MCAT={}

    def readFile(self,path,fN):
        f = open(path, 'rb')
        lines=f.readlines()
        f.close()

        if (fN.strip('.txt') == "rcv1_C13"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C13[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_C15"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C15[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_C151"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C151[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_C152"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C152[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_C17"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C17[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_C18"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C18[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_C181"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C181[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_C21"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C21[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_C24"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C24[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_C31"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.C31[ctr]=int(l.strip("\n"))

        elif (fN.strip('.txt') == "rcv1_CCAT"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.CCAT[ctr]=int(l.strip("\n"))
        elif (fN.strip('.txt') == "rcv1_GCAT"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.GCAT[ctr]=int(l.strip("\n"))
        elif (fN.strip('.txt') == "rcv1_MCAT"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.MCAT[ctr]=int(l.strip("\n"))
        elif (fN.strip('.txt') == "rcv1_ECAT"):
            ctr=0
            for l in lines:
                ctr=ctr+1
                self.ECAT[ctr]=int(l.strip("\n"))




    def getIntersectingPairs(self):
        intersectionCount=0
        cat2Only=0
        cat1Only=0
        for i in range(1,804405):
            if self.CCAT[i]==1 and self.ECAT[i]==1:
                intersectionCount=intersectionCount+1
            if self.CCAT[i]==-1 and self.ECAT[i]==1:
                cat2Only=cat2Only+1
            if self.CCAT[i]==1 and self.ECAT[i]==-1:
                cat1Only=cat1Only+1

        print "(CCAT,ECAT)"
        print "Intersection= ",intersectionCount
        print "CCAT Only= ",cat1Only
        print "ECAT Only= ",cat2Only
        other=804414-(intersectionCount+cat2Only+cat2Only)
        total=other+(intersectionCount+cat2Only+cat2Only)
        print "Neither= ",other
        print total











if __name__ == "__main__":
    c=CategoryStat()
    for root, subdirs, files in os.walk("/Users/jyothi/Documents/Research/jvdofs/rcv1v2/datFiles"):
        for f in files:
            c.readFile('/Users/jyothi/Documents/Research/jvdofs/rcv1v2/datFiles/'+f,f)

    c.getIntersectingPairs()