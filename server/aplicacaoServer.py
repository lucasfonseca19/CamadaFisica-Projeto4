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
from empacotador import empacotadorServer,pacote5
from erro import TimerError
import logmaker

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM4"                  # Windows(variacao de)

def main():
    
    #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
    #para declarar esse objeto é o nome da porta.
    server = enlace('COM4')
    # -------------------------- Criação de Objetos Log -------------------------- #
    log1 = logmaker.LogMaker("server", 1)
    log2 = logmaker.LogMaker("server", 2)
    log3 = logmaker.LogMaker("server", 3)
    log4 = logmaker.LogMaker("server", 4)
    log5 = logmaker.LogMaker("server", 5)


    # Ativa comunicacao. Inicia os threads e a comunicação seiral
    server.enable()
    ocioso=True
    while ocioso:
        try:
            Hs,nRx = server.getDataHS(14)
            id_server = int.from_bytes(b'\xEE', byteorder='little')
            if Hs[0] == 1 and Hs[5] == id_server:
                #recebeu mensagem t1
                log1.write_line("receb",1,14,"","","")
                ocioso=False
                print("Recebeu mensagem t1 correta do cliente")
                server.rx.clearBuffer()
            else:
                print("Recebeu mensagem do tipo errado ou de destinatario server diferente")
        except RuntimeError as erro:
            print(erro)
            print("Não recebeu nada do cliente")
            log3.write_ausencia("Timeout do HandShake")
            time.sleep(1)

    msgtipo2 = empacotadorServer(h0=2,h6=0,h7=0)
    server.sendData(msgtipo2)
    log1.write_line("envio",2,14,"","","")
    
    cont=1
    numPckg = Hs[3]
    Imagem_recebida = b''
    zerar2=True
    pacotefive = pacote5()
    while cont<=numPckg:
        try:
            server.rx.timer1=time.time()
            if zerar2:
                server.rx.timer2=time.time()
                zerar2=False
            print('Buscando pacote ...')
            header,nRx = server.getData(10)
            n_pckg_recebido = header[4]
            payload_size = header[5]
            payload,nRx = server.getData(payload_size)
            eop,nRx = server.getData(4)
            log1.write_line("receb",3,14+payload_size,cont,numPckg,b"\xb9\xb3")
            if n_pckg_recebido == cont and eop == b'\xAA\xBB\xCC\xDD':
                print("enviando pacote t4")
                zerar2=True
                Imagem_recebida += payload
                pacotet4 = empacotadorServer(h0=4,h6=0,h7=cont)
                server.sendData(pacotet4)
                log1.write_line("envio",4,14,"","","")
                cont+=1
                print("t4 enviado")
            else:
                print("Algo deu errado, enviando pacote t6")
                pacotet6 = empacotadorServer(h0=6,h6=cont,h7=0)
                server.rx.clearBuffer()
                server.sendData(pacotet6)
                log2.write_line("envio",6,14,"","","")
                print("t6 enviado")
                
        except TimerError as erro:
            tipo,mensagem = erro.args
            if tipo==1:
                server.sendData(empacotadorServer(h0=4,h6=0,h7=cont))
                log5.write_ausencia("Ausencia de resposta de pacote de dados com reenvio")
                print("Excedeu o timer de 2s  o tempo de resposta do client")
                zerar2 = False
            elif tipo==2:
                server.sendData(pacotefive)
                log4.write_ausencia("Ausencia de resposta de pacote de dados")
                print("Excedeu o timer de 20s o tempo de resposta do client")
                break
            

    if cont>=numPckg:
        f = open("imagem.jpg", "wb")
        f.write(Imagem_recebida)
        f.close()
        print("Foi enviado Imagem e ja esta no server")

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    server.disable()
        
    # except Exception as erro:
    #     print("ops! :-\\")
    #     print(erro)
    #     server.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
