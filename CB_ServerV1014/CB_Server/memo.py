import threading

class Memory:
    def __init__(self):
        self.memory = {}
        self.sem_using = threading.Semaphore(1)  # 1명만 쓸것

    def memorization (self,key,val):
        self.sem_using.acquire()
        self.memory[key]= val
        self.sem_using.release()

    def dememorization (self,key):
        self.sem_using.acquire()
        if key in self.memory:
            itme = self.memory[key]
            del(self.memory[key])
        else:
            itme = False
        
        self.sem_using.release()
        return itme

    
