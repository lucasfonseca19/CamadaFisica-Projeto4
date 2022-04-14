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
from empacotador import empacotador

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
        timeout = False
        

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        server.enable()
        
        id_server=b'\xaa'
        
        msgtipo2 = empacotador(2,0,0)
    
        
        IMAGEM = b''
        initial = True

        
            
        pacote_certo = False
        while initial:
            Hs,nRx=server.getData(14)
            if Hs[0] == 1:
                #tipo de mensagem recebido e 1
                print(Hs[5])
                if Hs[5] == int.from_bytes(id_server,byteorder='little'):
                    #se mensagem e para o server certo
                    initial = False
                    
                else:
                    #nao e para mim
                    time.sleep(1)
                    print("recebeu msg errada")
            else:
                #nao e mensagem do tipo 1
                time.sleep(1)
                print("recebeu msg errada")

        numDePacotes = Hs[3]

        if initial==False:
            server.sendData(msgtipo2)
            cont = 1

        reenvio = False 

        while cont<=numDePacotes:
            #Recebe mensagem t3
            msgtipo6 = empacotador(6,cont,cont-1)
            msgtipo5 = empacotador(5,0,0)
            server.rx.timer1 = time.time()

            if not reenvio:
                server.rx.timer2 = time.time()
            
            headert3,nRx = server.getData(10)
            if nRx == 1:
                #Deu timeout quando tentava pegar o header
                if headert3[0] == 1:
                    #timer1 timeout
                    server.sendData(msgtipo6)
                    reenvio = True
                if headert3[0] == 2:
                    #timer2 timeout
                    server.sendData(msgtipo5)
                    print("Erro de timeout mais de 20s")
                    break
            else:
                size_payload = headert3[5] 
                payloadt3, nRx2 = server.getData(size_payload)
                if nRx2 == 1:
                    # deu timeout quando tentava pegar o payload
                    if payloadt3[0] == 1:
                        # timer1 timeout
                        server.sendData(msgtipo6)
                        reenvio = True
                    if payloadt3[0] == 2:
                        # timer2 timeout
                        server.sendData(msgtipo5)
                        print("Erro de timeout mais de 20s")
                        break
                else:
                    eop, nRx3 = server.getData(4)
                    if nRx3 == 1:
                        #deu timeout quando tentava pegar o eop
                        if eop[0] == 1:
                            #timer1 timeout
                            server.sendData(msgtipo6)
                            reenvio = True
                        if eop[0] == 2:
                            #timer2 timeout
                            server.sendData(msgtipo5)
                            print("Erro de timeout mais de 20s")
                            break
                    else:
                        #nao deu timeout em nenhum
                        reenvio = False
                        if headert3[4] == cont:
                            #pacote correto
                            pacote_certo = True

                        if eop==b"\xAA\xBB\xCC\xDD" and pacote_certo:
                            msgtipo4 = empacotador(4,0,cont)
                            cont += 1
                            IMAGEM+=payloadt3
                            server.sendData(msgtipo4)
                        else:
                            if server.rx.getBufferLen()>0:
                                print("tamanho do payload informado esta errado")
                            if not pacote_certo:
                                print("numero do pacote recebido esta fora de ordem")
                            server.rx.clearBuffer()
                            
                            server.sendData(msgtipo6)
        
        if cont == numDePacotes:
            
            f = open("imagem.jpg", "wb")
            f.write(IMAGEM)
            f.close()
            print("Foi enviado Imagem e ja esta no server")


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
