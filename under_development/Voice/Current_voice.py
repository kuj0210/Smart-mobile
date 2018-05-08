from string import ascii_lowercase
import HEAP

class encoding:

    def __init__(self):
        self.heap=None
        self.UnionOfAlphabetFromInput = []
        self.UnionCnt=0
        self.input = ""
        self.inputCNT =0
    def setInput(self,str):
        self.input = str
        self.inputCNT= len(str)-1

    def collectUnionOfAlphabetFromInput(self):
        alpahlist = list(ascii_lowercase)
        cnt = 0
        for i in alpahlist:
            if i in self.input:
                self.UnionOfAlphabetFromInput.append([i])
                cnt+=1
            else:
                continue
        self.UnionCnt=cnt
    def addFrequencyInUnion(self):
        if len(self.UnionOfAlphabetFromInput)==0:
            print("NULL ITEM ERR IN UNION")
            return;
        else:
            for i in range(0,len(self.UnionOfAlphabetFromInput)):
                self.UnionOfAlphabetFromInput[i].append(self.input.count(self.UnionOfAlphabetFromInput[i][0]))

    def encoding(self,h):
        if "left" in h.Heap:
            h.getL().setPath(h.getPath()+"0")
            self.encoding(h.getL())
        if "right" in h.Heap:
            h.getR().setPath(h.getPath()+"0")
            self.encoding(h.getR())

    def SortByGrade(self,h,x,y):
        for index in range(x+1, y-2):
            key = h[index]
            position = index
            while(position>0 and key.getGrade()< h[position].getGrade()):
                h[position] = h[position-1]
                position-=1
            h[position]=key

    def printHEAP(self,h):
        print("PPPPPPPPPPP")
        if "left" in h.Heap:
            print(h.Heap)
            self.printHEAP(h.getL())
        if "right" in h.Heap:
            print(h.Heap)
            self.printHEAP(h.getR())
    def HuffmanCoding(self):
        encode.collectUnionOfAlphabetFromInput()
        encode.addFrequencyInUnion()
        index=0
        index2=0
        self.heap = []
        for index in range(0,self.UnionCnt-2):
            self.heap.append(HEAP.Heap())
            hNode =HEAP.Heap()
            if index < self.UnionCnt:
                hNode.setStrAndGrade(self.UnionOfAlphabetFromInput[index][0],self.UnionOfAlphabetFromInput[index][1])
        self.SortByGrade(self.heap,0,self.UnionCnt)
        print(self.UnionCnt)
        print(index)
        for count in range(0,self.UnionCnt-2):
            h = HEAP.Heap()
            h.setS_L_R(self.heap[index2].getStr()+self.heap[index2+1].getStr(),self.heap[index2],self.heap[index2+1])
            self.heap[index]=h
            index2+=2
            index+=1
            self.SortByGrade(self.heap, index2, index)

        root = self.heap[self.UnionCnt*2-2]
        self.encoding(root)
        self.printHEAP(root)
if __name__ == '__main__':
    encode = encoding()
    encode.setInput("aaaabbbcccccsadfefsdagsdgasdfasdqweq")
    encode.HuffmanCoding()
    print(encode.UnionOfAlphabetFromInput)
