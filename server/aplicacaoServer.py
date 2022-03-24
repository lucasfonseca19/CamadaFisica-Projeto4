#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

import sys
from enlaceServer import *
import time
import numpy as np

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

"""
    Função que empacota os dados de entrada em datagramas.
    Arquitetura:
    Head (10 bytes):
        -h0 → tipo de mensagem
        -h1 → livre
        -h2 → livre
        -h3 → número total de pacotes do arquivo
        -h4 → número do pacote sendo enviado
        -h5 → Se tipo == Handshake, id do arquivo
              Se tipo == dados, tamanho do payload
        -h6 → pacote solicitado para recomeço quando há erro no envio
        -h7 → último pacote recebido com sucesso
        -h8 e h9 → CRC, ou Cyclic Redundancy Check
    Payload(entre 0 e 114 bytes)
    EOP (4 bytes):
        0xAA 0xBB 0xCC 0xDD
"""

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        server = enlace('COM4')


        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        server.enable()
        IMAGEM = b''
        Ocioso = True
        id_server=b'\xaa'
        
        msgtipo2 = b'\x02\x00\x00\x01\x01'+id_server+b'\x00\x00\x00\x00'+ b'\xAA\xBB\xCC\xDD'
        numPckg = msgtipo2[3]
        while Ocioso:
            Hs,nRx=server.getData(14)
            if Hs[0] == 1:
                #tipo de mensagem recebido e 1
                if Hs[5] == int.from_bytes(id_server,byteorder='little'):
                    #se mensagem e para o server certo
                    Ocioso=False

            time.sleep(1)
            print("recebeu msg errada")
        
        if Ocioso==False:
            server.sendData(msgtipo2)
            cont = 1
        

        while cont<=numPckg:
            numDoPckg=cont
            timer1 = 0
            timer2 = 0
            msgT3Head,nRx = server.getData(10)
            if msgT3Head[0] != 3:
                while timer2 < 20:
                    time.sleep(1)
                    timer2+=1
                    #IMPLEMENTAR
                    #Quando msgrecebida nao for t3
            tamanhopayload = msgT3Head[5]
            numDoPckgAtual = msgT3Head[4]
            
            payload,nRx = server.getData(tamanhopayload)
            sEOP,nRx = server.getData(4)

            if sEOP != b'\xAA\xBB\xCC\xDD' or numDoPckgAtual != numDoPckg:
                print("Mensagem deu ruim e vai ser enviado msg t6")
                #IMPLEMENTAR MSG T6

            msgtipo4 = b''
            server.sendData(msgtipo4)
            cont+=1
                






        f = open("imagem.jpg", "wb")
        f.write(IMAGEM)
        f.close()


        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        server.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        server.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
