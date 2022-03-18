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
#   python -m serial.tools.list_ports

serialName = "COM8"


def main():
    try:
        client = enlace(serialName)


        client.enable()

        # Estrutura datagrama:
        # |      HEAD      |     PAYLOAD   | EOP |
        # ▭▭▭▭▭▭▭▭▭▭ ... ▭▭▭ ... ▭▭▭▭
        #
        # LIMITE DE ENVIO: 128 BYTES
        # HEAD(10 BYTES) + PAYLOAD(0 - 114 BYTES) + EOP(2 BYTES))
        # HEAD:
        #      Número de pacote e o numero de pacotes totais
        # DONE:
        # Implementar Handshake
        #   - Envio de uma mensagem para o servidor
        #   - Recebimento de uma mensagem do servidor dentro de 5 segundos
        #   - caso não receba, imprimir "Servidor Inativo.Tenta Novamente?S/N"
        #   - caso o usuário responda "S", reenvie a mensagem de handshake
        #   - caso o usuário responda "N", finalize a conexão
        #   - caso o client receba uma mensagem do servidor, imprima "Conexão estabelecida"
                                        #| IM do head                 |#EOD
        pkg_hand_shake = b"\x01\x01\x00\xAA\xDD\xFF\xFF\xFF\xAA\xDD\xEE\x23\x4C\xA9"

        # ------------------------- Enviando Handshake ------------------------ #
        while True:
            client.sendData(pkg_hand_shake)
            time.sleep(0.1)
            print("Handshake enviado")
            resposta, nRx = client.getData(14)

            if resposta == pkg_hand_shake:
                print("Handshake recebido")
                break
            elif resposta == False:
                entrada = input("Servidor Inativo. Tenta Novamente? S/N\n")
                if entrada == "N":
                    print("Tchau")
                    sys.exit(0)

        # ------------------------- Mandando imagem ------------------------ #
        lista_de_pacotes = empacotador("pixel.png")
        for i in range(len(lista_de_pacotes)):
            client.sendData(lista_de_pacotes[i])
            time.sleep(0.1)
            resposta, Nrx = client.getData(14)
            print("Pacote {} enviado".format(i+1))
            if resposta == None:
                print("Erro no envio do pacote:", i+1)
                sys.exit(0)

        print("Imagem enviada")



        #TODO:
        # Checagem constante do recebimento da mensagem para prosseguir com o envio da seguinte
        #TODO:

        client.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        client.disable()


if __name__ == "__main__":
    main()
