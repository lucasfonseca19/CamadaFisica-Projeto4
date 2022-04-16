

import datetime


class LogMaker:
    def __init__(self, user, numero):
        self.user = user
        self.numero = numero
        self.arquivo = open( user+str(numero)+".txt", 'w')
    def write_line(self,estado ,tipo_de_mensagem, tamanho, pacote_enviado,total_de_pacotes,crc):
        date_and_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.arquivo.write(date_and_time+" / "+estado+" / "+ str(tipo_de_mensagem)+" / "+str(tamanho)+" / "+str(pacote_enviado)+" / "+str(total_de_pacotes)+" / "+str(crc)+"\n")
    def write_ausencia(self,mensagem):
        date_and_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.arquivo.write(date_and_time+" / "+mensagem+"\n")
    def get_log_file(self):
        self.arquivo.close()
        return self.arquivo
    