import logmaker as logmaker


log1 = logmaker.LogMaker("client", 1)
log2 = logmaker.LogMaker("client", 2)
log3 = logmaker.LogMaker("client", 3)
log4 = logmaker.LogMaker("client", 4)
log5 = logmaker.LogMaker("client", 5)

log1.write_line("envio",1,14,"","","")
log2.write_line("receb",6,14,"","","")
log3.write_ausencia("timeout de handshake")
log4.write_ausencia("Ausência de resposta de pacote de dados")                    
log5.write_ausencia("Ausência de pacote de dados com reenvio")