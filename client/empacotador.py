import numpy as np

def empacotadorClient(imagem):
    '''
        A funcao empacotadorClient vai ser responsavel por criar uma lista de lista
        de bytes que vao ser enviados para server

        h0 – tipo de mensagem
        h1 – livre
        h2 – livre
        h3 – número total de pacotes do arquivo
        h4 – número do pacote sendo enviado
        h5 – se tipo for handshake:id do arquivo
        h5 – se tipo for dados: tamanho do payload
        h6 – pacote solicitado para recomeço quando a erro no envio.
        h7 – último pacote recebido com sucesso.
        h8 – h9 – CRC
        PAYLOAD – variável entre 0 e 114 bytes. Reservado à transmissão dos arquivos.
        EOP – 4 bytes: 0xAA 0xBB 0xCC 0xDD
    '''

    h1=b'\xFA'
    h2=b'\xF6'
    h6 =b'\x00'
    h8=b'\xB9'
    h9=b'\xE3'
    EOP = b'\xAA\xBB\xCC\xDD'
    listofpackages=[]
    #primeiro pacote sera o HandShake
    #Depois os outros
    id_server = b'\xEE'

    with open(imagem,'rb') as f:
        img = f.read()
        tamanho = len(img)
        numero_de_pacotes = tamanho // 114
        restante = tamanho - numero_de_pacotes
        if restante>0:
            numero_de_pacotes+=1
        #append do handshake
        h3 = bytes([numero_de_pacotes])

        headerHS = b'\x01'+h1+h2+h3+b'\x00'+ id_server+h6+b'\x00'+ h8 + h9
        heandshake = headerHS+EOP

        listofpackages.append(np.asarray(heandshake))

        for i in range(numero_de_pacotes):
            payload = img[(i)*114:(i+1)*114]
            h4 = bytes([i+1]) #numero do pacote
            h5 = bytes([len(payload)]) #tamanho do payload
            h7 = bytes([i]) #numero do ultimo pacote enviado
            header = b'\x03'+h1+h2+h3+h4+h5+h6+h7+h8+h9
            package = header+payload+EOP
            listofpackages.append(np.asarray(package))

    return listofpackages

def pacote5():
    header = b'\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    EOP = b'\xAA\xBB\xCC\xDD'
    resposta = header+EOP
    return np.asarray(resposta)

def empacotadorServer(h0,h6,h7):
    '''
        A funcao empacotadorClient vai ser responsavel por criar uma lista de lista
        de bytes que vao ser enviados para server

        h0 – tipo de mensagem
        h1 – livre
        h2 – livre
        h3 – número total de pacotes do arquivo
        h4 – número do pacote sendo enviado
        h5 – se tipo for handshake:id do arquivo
        h5 – se tipo for dados: tamanho do payload
        h6 – pacote solicitado para recomeço quando a erro no envio.
        h7 – último pacote recebido com sucesso.
        h8 – h9 – CRC
        PAYLOAD – variável entre 0 e 114 bytes. Reservado à transmissão dos arquivos.
        EOP – 4 bytes: 0xAA 0xBB 0xCC 0xDD

        h0,h6 e h7 em numeros inteiros
        para t2 h6 e h7 = 0;
        para t4 h6 = 0;
        para t6 h7 = 0;
    '''

    h1=b'\xFA'
    h2=b'\xF6'
    h3 = b'\x00'
    h4 = b'\x00'
    h5 = b'\x00'
    h8=b'\xB9'
    h9=b'\xE3'
    h0_b = bytes([h0])
    h6_b = bytes([h6])
    h7_b = bytes([h7])
    EOP = b'\xAA\xBB\xCC\xDD'

    if h0 == 2:
        #resposta ao heandshake (tipo 2)
        header = h0_b + h1 + h2 + h3 + h4 + h5 + b'\x00' + b'\00' + h8 + h9
        pacote = header + EOP
    elif h0 == 4:
        #resposta ao pacote 3 enviado pelo client
        header = h0_b + h1 + h2 + h3 + h4 + h5 + b'\x00' + h7_b + h8 + h9
        pacote = header + EOP
    elif h0 == 6:
        #resposta quando numero do pacote esperado pelo servidor for o errado
        header = h0_b + h1 + h2 + h3 + h4 + h5 + b'\x00' + h7_b + h8 + h9
        pacote = header + EOP

    return np.asarray(pacote)
    
        