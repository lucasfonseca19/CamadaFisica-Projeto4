from logmaker import LogMaker
from empacotador import *
lista_de_pacotes = empacotador(3,0,0)


pacote_anterior = 0
pacote_atual = 0
for i in range(6):
    package = empacotador(3,0,i)
    pacote_anterior = pacote_atual
    pacote_atual+=1
    print(package)
    print("\n   ----------------------")
