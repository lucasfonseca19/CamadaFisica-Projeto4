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
from empacotador import empacotador
import settings
# Class
class RX(object):
  
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024
        self.timer1      = 0
        self.timer2      = 0


    def setTimer1(self):
        self.timer1 = 0
    
    def setTimer2(self):
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

    def getNData(self, size):
        #Fazer um while que dura ate quando buffer for menor que tamanho
        #timer1 e timer2 sao iniciados no loop cont<=NumdePacotes
        #Se exceder timer2,retorna uma lista vazia para o valor de t3 e no aplicacaoServer fazer com que essa condicao pare o loop
        #e seja enviado msgt6
        #Se exceder timer1,retorna uma lista [4] para o valor de t3 e no aplicativoServer fazer com que essa condicao envie uma msg tipo4 porem
        #nao acrescente valor ao cont,forcando um reenvio do client 
        
        while(self.getBufferLen() < size):
            
            agora = time.time()
            if self.timer1 != 0 and self.timer2 != 0:#ainda esta no HS
                if agora - self.timer2 > 20:
                    #timeout, envia menssagem tipo 5
                    return [1]
                if agora - self.timer1 > 2:
                    #envia msg tipo 6
                    return [2]
            time.sleep(0.1)

        return(self.getBuffer(size))
        

    def clearBuffer(self):
        self.buffer = b""
