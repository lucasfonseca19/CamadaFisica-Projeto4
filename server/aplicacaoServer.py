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

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        server = enlace('COM4')


        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        server.enable()

        # --------------------- HANDSHAKE --------------------- #
        handshakepkg,_nrx = server.getData(14)
        print(handshakepkg)
        server.sendData(handshakepkg)
        print('handshake resposta enviado')

        #---------------------RECEBENDO IMAGEM---------------------#
        IMAGEM = b""
        first_head, nRx = server.getData(10)
        print(first_head[2])
        size_payload = first_head[2]
        numero_de_pacotes = first_head[1]
        # Caso a imagem seja menor que o payload de um pacote, então não precisaremos
        # entrar na lógica de ‘loop’ de recebimento de pacotes.
        if size_payload < 114:
            msgAndEOP, nRx = server.getData(size_payload+4)
            
            IMAGEM += msgAndEOP
            #salvar em um arquivo
        else:
            # Caso a imagem seja maior que o payload de um pacote, então precisaremos
            # entrar na lógica de ‘loop’ de recebimento de pacotes.
            # Salva o payload do primeiro pacote em uma variável que será usada para
            # concatenar os demais payloads, resultando em uma imagem completa.
            primeiro_payload, nRx = server.getData(size_payload)
            IMAGEM += primeiro_payload
            # Iremos agora pegar mais 4 ‘bytes’ para saber e verificar se são o EOP.
            primeiro_EOP, nRx = server.getData(4)
            if primeiro_EOP == b'\xEE\x23\x4C\xA9':
                print("primeiro enviado")
            else:
                print("Envio incorreto")
                sys.exit()
            # Agora iremos receber os demais pacotes.
            pacote_atual = 2
            pacote_anterior = 1
            for i in range(2,numero_de_pacotes):
                head, nRx = server.getData(10)
                tamanho_payload = head[2]
                pacote_atual = head[0]
                print(pacote_atual)
                try:
                    payload, nRx = server.getData(tamanho_payload)
                except:
                    print("tamanho do payload errado")
                    
                IMAGEM += payload
                EOP, nRx = server.getData(4)
                # Iremos agora verificar se o numero do pacote atual é igual 1 mais o numero do pacote anterior.
                # Se não for, então houve um erro.
                if pacote_atual != pacote_anterior+1:
                    print("Erro no envio")
                    sys.exit()

                pacote_anterior = pacote_atual
                if EOP != b'\xEE\x23\x4C\xA9':
                    print("EOP incorreto e tamanho do payload incorreto")
                    sys.exit()

                server.sendData(handshakepkg)
            
            print(IMAGEM)

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
