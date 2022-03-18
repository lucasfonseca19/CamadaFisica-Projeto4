import numpy as np

def empacotar(dados, tipo_dados):
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
    with open(dados, 'rb') as f:
        dados = f.read()
        tamanho = len(dados)
        num_pacotes = int(np.ceil(tamanho/114))
        restante = tamanho // 114
        if restante > 0:
            num_pacotes += 1
        lista_de_pacotes = []





    if tipo_dados == 1:
        # Handshake de início
        pass
    elif tipo_dados == 2:
        # Handshake de resposta
        pass
    elif tipo_dados == 3:
        # envio de dados
        pass
    elif tipo_dados == 4:
        # confirmação de recebimento de dados
        pass
    elif tipo_dados == 5:
        # mensagem de timeout
        pass
    elif tipo_dados == 6:
        # mensagem de erro
        pass
    else:
        pass
