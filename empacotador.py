import numpy as np
from pyrsistent import b


def empacotador(tipo_dados, pacote_error, ultimo_pacote):
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
    ####### ATENÇÃO:
    ####### SUBSTITUIR dados PELO ENDEREÇO DO ARQUIVO A SER ENVIADO
    with open(dados, 'rb') as f:
        dados = f.read()
        tamanho = len(dados)
        num_pacotes = int(np.ceil(tamanho / 114))
        restante = tamanho // 114
        if restante > 0:
            num_pacotes += 1
    
    head = b""
    eod = b"\xAA\xBB\xCC\xDD"
    payload = b""
    id_server = b"\xaa"
    lista_pacotes = []
    ultimo_pacote_bytes = bytes(ultimo_pacote)
    pacote_error_bytes = bytes(pacote_error)
    
    
    if tipo_dados == 1:
        head = b'\x01\x00\x00'+num_pacotes+'\x01'+id_server+b'\x00\x00\x00\x00'
        pacote = head + payload + eod
        lista_pacotes.append(pacote)
    elif tipo_dados == 2:
        # Handshake de resposta
        head = b'\x02\x00\x00\x01\x01'+id_server+b'\x00\x00\x00\x00'
        pacote = head + payload + eod
        lista_pacotes.append(pacote)
    elif tipo_dados == 3:
        # envio de dados
        for i in range(num_pacotes):
            payload = dados[i*114:(i+1)*114]
            n_do_pacote = bytes(i+1)
            n_de_pacotes = bytes(num_pacotes)
            tamanho_payload = bytes(len(payload))    
            head = b'\x03\x00\x00'+n_de_pacotes+n_do_pacote+tamanho_payload+pacote_error+ultimo_pacote_bytes+b'\x00\x00'
            pacote = head+payload+eod
            lista_pacotes.append(pacote)
    elif tipo_dados == 4:
        # confirmação de recebimento de dados
        head = b'\x04\x00\x00\x01\x01\x00\x00'+ultimo_pacote_bytes+b'\x00\x00'
        pacote = head + payload + eod
        lista_pacotes.append(pacote)
        pass
    elif tipo_dados == 5:
        # mensagem de timeout
        head = b'\x05\x00\x00\x01\x01\x00\x00'+ultimo_pacote_bytes+b'\x00\x00'
        pacote = head + payload + eod
        lista_pacotes.append(pacote)        
    elif tipo_dados == 6:
        # mensagem de erro
        head = b'\x06\x00\x00\x01\x01\x00' + pacote_error_bytes+ultimo_pacote_bytes+ b'\x00\x00'
        pacote = head + payload + eod
        lista_pacotes.append(pacote)
    return lista_pacotes

