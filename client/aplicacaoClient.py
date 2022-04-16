#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from math import log2

from cv2 import log
from enlaceClient import *
import time
import numpy as np
import random as rd
import sys
from empacotador import empacotadorClient, pacote5
from erro import TimerError
import logmaker
#   python -m serial.tools.list_ports

serialName = "COM3"


def main():
    try:
        client = enlace(serialName)
        # -------------------------- Criação de Objetos Log -------------------------- #
        log1 = logmaker.LogMaker("client", 1)
        log2 = logmaker.LogMaker("client", 2)
        log3 = logmaker.LogMaker("client", 3)
        log4 = logmaker.LogMaker("client", 4)
        log5 = logmaker.LogMaker("client", 5)
        IMAGEM = 'pixel.png'

        all_pkgs = empacotadorClient(IMAGEM)
        client.enable()
        inicia = False
        pacotefive = pacote5()
        while not inicia:
            try:
                print("enviando handshake")
                client.sendData(all_pkgs[0])
                log1.write_line("envio",1,14,"","","")
                #log2.write_line("envio",1,14,"","","")
                #log3.write_line("envio",1,14,"","","")
                #log4.write_line("envio",1,14,"","","")
                #log5.write_line("envio",1,14,"","","")
                # time.sleep(5)
                resposta_t2,nRx = client.getDataHS(14)
                if resposta_t2[0] == 2:
                    #recebeu mensagem t2
                    inicia = True
                    log1.write_line("receb",2,14,"","","")
                    #log2.write_line("envio",2,14,"","","")
                    #log3.write_line("envio",2,14,"","","")
                    #log4.write_line("envio",2,14,"","","")
                    #log5.write_line("envio",2,14,"","","")
                    print("recebeu mensagem t2")
                else:
                    print("recebeu mensagem de tipo errado")
            except RuntimeError as erro:
                print("reenviando Handshake")
                log3.write_ausencia("timeout de handshake")

        cont=1
        numPck = len(all_pkgs)-1
        zerar2=True
        while cont <= numPck:
            try:
                print("enviando pacote")
                client.sendData(all_pkgs[cont])
                a= all_pkgs[cont]
                lista = list(bytes(a))
                
                
                log1.write_line("envio",3,len(lista),cont,numPck,b"\xb9\xb3")
                #log1.write_line("envio",3,len(lista),cont,numPck,b"\xb9\xb3")
                #log2.write_line("envio",3,len(lista),cont,numPck,b"\xb9\xb3")
                #log3.write_line("envio",3,len(lista),cont,numPck,b"\xb9\xb3")
                #log4.write_line("envio",3,len(lista),cont,numPck,b"\xb9\xb3")
                #log5.write_line("envio",3,len(lista),cont,numPck,b"\xb9\xb3")
                client.rx.timer1=time.time()
                if zerar2:
                    client.rx.timer2=time.time()
                    zerar2=False
                print("Buscando resposta do server")
                resposta,nRx = client.getData(14) #msgt4
                print("servidor enviou resposta")
                if resposta[0] == 4:
                    #Recebeu mensagem 4
                    zerar2=True
                    log1.write_line("receb",4,14,"","","")
                    #log3.write_line("receb",4,14,"","","")
                    #log4.write_line("receb",4,14,"","","")
                    #log5.write_line("receb",4,14,"","","")
                    cont+=1
                elif resposta[0]==6:
                    #recebeu mensagem 6
                    log2.write_line("receb",6,14,"","","")
                    zerar2=True
                    cont = resposta[6]
                    print("msgt6")
            except TimerError as erro:
                tipo,mensagem = erro.args
                if tipo==1:
                    client.sendData(all_pkgs[cont])
                    client.rx.timer1 = time.time()
                    zerar2 = False
                    print("reenviando pacote")
                    log5.write_ausencia("Ausência de pacote de dados com reenvio")
                elif tipo==2:
                    log4.write_ausencia("Ausência de resposta de pacote de dados")
                    print("Excedeu o limte de 20 segundos de espera")
                    client.sendData(pacotefive)
                    break

        client.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        client.disable()
        

if __name__ == "__main__":
    main()
