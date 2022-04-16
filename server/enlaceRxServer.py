#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading
from erro import TimerError

# Class
class RX(object):
  
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024
        self.timer1 = 0
        self.timer2 = 0

    def thread(self): 
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp  
                time.sleep(0.01)

    def threadStart(self):       
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def getIsEmpty(self):
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        return(len(self.buffer))

    def getAllBuffer(self, len):
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNDataHS(self, size):
        start_time = time.time()
        seconds = 20
        while (self.getBufferLen() < size):
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > seconds:
                self.clearBuffer()
                raise RuntimeError
                
            time.sleep(0.05)
            
        return (self.getBuffer(size))

    def getNData(self, size):
        
        while(self.getBufferLen() < size):
            agora = time.time()
            if agora-self.timer1>2:
                #vai ativar erro
                print("Ativa erro 1")
                raise TimerError(timeout=1)
            elif agora - self.timer2>20:
                #vai ativar outro erro
                print("Ativa erro 2")
                raise TimerError(timeout=2)
            time.sleep(0.05)

        return(self.getBuffer(size))

    

    def clearBuffer(self):
        self.buffer = b""


