#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from enlaceClient import *
import time
import numpy as np
import random as rd
import sys
from empacotador import empacotadorClient, pacote5
from erro import TimerError

#   python -m serial.tools.list_ports

serialName = "COM3"


def main():
    try:
        client = enlace(serialName)
        
        IMAGEM = 'pixel.png'

        all_pkgs = empacotadorClient(IMAGEM)
        client.enable()
        inicia = False
        pacotefive = pacote5()
        while not inicia:
            try:
                print("enviando msgt1 com ident")
                client.sendData(all_pkgs[0])
                # time.sleep(5)
                resposta_t2,nRx = client.getDataHS(14)
                if resposta_t2[0] == 2:
                    #recebeu mensagem t2
                    inicia = True
                    print("recebeu mensagem t2")
                else:
                    print("recebeu mensagem de tipo errado")
            except RuntimeError as erro:
                print(erro)
                print("reenviando Handshake")

        cont=1
        numPck = len(all_pkgs)-1
        zerar2=True
        print("Iniciando LOOP")
        while cont <= numPck:
            try:
                print("enviando pacote")
                client.sendData(all_pkgs[cont])
                print(all_pkgs[cont])
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
                    cont+=1
                elif resposta[0]==6:
                    #recebeu mensagem 6
                    zerar2=True
                    cont = resposta[6]
                    print("msgt6")
            except TimerError as erro:
                tipo,mensagem = erro.args
                if tipo==1:
                    client.sendData(all_pkgs[cont])
                    client.rx.timer1 = time.time()
                    zerar2 = False
                elif tipo==2:
                    print("Timeout timer2")
                    client.sendData(pacotefive)
                    break

        client.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        client.disable()
        

if __name__ == "__main__":
    main()
