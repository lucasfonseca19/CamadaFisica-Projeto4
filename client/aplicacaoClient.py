#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


from ast import Num
from enlaceClient import *
import time
import numpy as np
import random as rd
import sys
from empacotador import *
from logmaker import LogMaker
#   python -m serial.tools.list_ports

serialName = "COM8"


def main():
    try:
        
        log1 = LogMaker("client",1)
        
        # ---------------------------- Estados e Contadores -------------------------- #
        numero_de_pacotes_enviados = 0
        # ------------------------------- Enable Porta ------------------------------- #
        #region
        client = enlace(serialName)
        client.enable()
        #endregion
        # ------------------------- Enviando Handshake ------------------------ #
        #region
        handshake = empacotador(1,0,0)
        handshake_resposta = empacotador(2,0,0)
        print("Hanshake gerado e pronto pro envio")
    
        estado_handshake = True
        while estado_handshake:
            client.sendData(handshake)
            
            time.sleep(5)
            print("Handshake enviado")
            resposta, nRx = client.getData(14)

            if resposta == handshake_resposta:
                print("Handshake de resposta recebido")
                numero_de_pacotes_enviados += 1
                estado_handshake = False
            elif resposta == False:
                print("Reenviando Handshake")
        #endregion
        # # # ------------------------- Mandando imagem ------------------------ #
        
        numero_de_pacotes_da_imagem = handshake[3]
        print("Numero de pacotes da imagem: ", numero_de_pacotes_da_imagem)
        
        
        pacote_anterior = 0
        pacote_atual = 0
        # for i in range(numero_de_pacotes_da_imagem):
        #     empacotador(3,0,i)
        #     pacote_anterior = pacote_atual
        #     pacote_atual+=1
            
       empa
        
        
        
        
        
        
        
        
        for i in range(numero_de_pacotes_da_imagem):
            print("Enviando pacote: ", i+1)
            client.sendData(i)
            log1.write_line('enviando',3,len(i),i[4],numero_de_pacotes_da_imagem,i[8]+i[9])
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            time.sleep(0.1)
            numero_de_pacotes_enviados += 1
            print("Pacote enviado")
            time.sleep(0.1)
            numero_de_pacotes_enviados += 1
            print("Pacote enviado")
        
        # lista_de_pacotes = empacotador("pixel.png")
        # for i in range(len(lista_de_pacotes)):
        #     client.sendData(lista_de_pacotes[i])
        #     time.sleep(0.1)
        #     resposta, Nrx = client.getData(14)
        #     print("Pacote {} enviado".format(i+1))
        #     if resposta == None:
        #         print("Erro no envio do pacote:", i+1)
        #         sys.exit(0)

        # print("Imagem enviada")
        # client.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        # client.disable()


if __name__ == "__main__":
    main()
