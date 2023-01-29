import PySimpleGUI as sg

MAX_LINHAS=9

def removerPalavrasQueTemCertaLetra(dicionario, letraProcurada, posicao, mapa):
    removeSoDe1Posicao = False
    for i in range(5):
        if ((mapa[i][1] == 'verde' and mapa[i][0] == letraProcurada) or 
            (mapa[i][1] == 'amarelo' and mapa[i][0] == letraProcurada)):
            removeSoDe1Posicao=True
    if removeSoDe1Posicao == True:
        return [word for word in dicionario if word[posicao] != letraProcurada]
    else:   
        return [word for word in dicionario if letraProcurada not in word]

def manterSoPalavrasQueTemCertaLetraNaPosicaoEspecificada(dicionario, letra, posicao):
    return [word for word in dicionario if letra == word[posicao]]

def manterSoPalavrasQueTemCertaLetraERemoverPalavrasComLetraNaPosicaoErrada(dicionario, letraProcurada, posicao, mapa):
    resultado = []
    for palavra in dicionario:
        mantemPalavra = False
        for i in range(5):
            if not(((mapa[i][1] == 'verde' and mapa[i][0] == letraProcurada) or 
            (mapa[i][1] == 'amarelo' and mapa[i][0] == letraProcurada))):
                if (palavra[i] == letraProcurada and i != posicao):
                    mantemPalavra = True
        if mantemPalavra:
            resultado.append(palavra)
    return resultado

def carregarDicionario():
    with open('palavras-5-letras-maiuscula-sem-acentos-utf8.txt', 'r') as dicionario:
        return [line.rstrip() for line in dicionario]

def construirLinhaDeCamposDigitaveis(numLinha):
    linha = []
    LABEL_PRETO = 'Não existe' 
    LABEL_AMARELO = 'Existe em OUTRA posição'
    LABEL_VERDE = 'Existe NESTA posição'
    for coluna in range(5):
        linha = linha + [sg.Frame('', [
        [sg.In(key="-campo-digitado-" + str(numLinha) + '-' + str(coluna), change_submits=True, size=(3, 1), 
        background_color="DimGray", font=('Arial bold', 32), justification="center", text_color="white")] ,
        [sg.Radio(LABEL_VERDE, background_color='Turquoise', text_color='Black',
            key='-campo-digitado-radio-'+str(numLinha) + '-' + str(coluna)+'-verde', group_id='GRUPO' + str(numLinha) + '-' + str(coluna), default=False, 
            font=('Arial bold', 12))],
        [sg.Radio(LABEL_AMARELO, background_color='Gold', text_color='Black',
            key='-campo-digitado-radio-'+str(numLinha) + '-' + str(coluna)+'-amarelo', group_id='GRUPO' + str(numLinha) + '-' + str(coluna),  default=False, 
            font=('Arial bold', 12))],
        [sg.Radio(LABEL_PRETO, background_color='Black', 
            key='-campo-digitado-radio-'+str(numLinha) + '-' + str(coluna)+'-preto', group_id='GRUPO' + str(numLinha) + '-' + str(coluna),  default=False, 
            font=('Arial bold', 12))],
    ])]
    return linha + [sg.Button('Calcular',  key="-campo-digitado-submit-"+str(numLinha), border_width=0, button_color="DimGray", font=('Arial bold', 24))]

def construirLayout():
    global dicionario

    linhaSuperiorTeclado = "QWERTYUIOP"
    linhaDoMeioTeclado = "ASDFGHJKL"
    linhaInferiorTeclado = "ZXCVBNM"

    input_column = [
        construirLinhaDeCamposDigitaveis(0)
    ]

    teclado = [
        # 1a Linha teclado
        [sg.Text(' ' * 4)] + [sg.Button(c, key='-teclado-'+c, size=(5, 1), border_width=0, button_color="DimGray",
        font=('Arial bold', 24)) for c in linhaSuperiorTeclado],

        # 2a Linha teclado
        [sg.Text(' ' * 11)] + [sg.Button(c, key='-teclado-'+c, size=(5, 1), border_width=0, button_color="DimGray", font=('Arial bold', 24)) 
        for c in linhaDoMeioTeclado] + [sg.Button('⌫', key='back', size=(5, 1),  border_width=0, button_color="DimGray", font=('Arial bold', 24), disabled=True)],

        # 3a Linha teclado
        [sg.Text(' ' * 18)] + [sg.Button(c, key='-teclado-'+c, size=(5, 1), border_width=0, button_color="DimGray", font=('Arial bold', 24)) 
        for c in linhaInferiorTeclado] + [sg.Button('ENTER', key='Enter', size=(6, 1), border_width=0, button_color="DimGray", font=('Arial bold', 24), disabled=True)] 
    ]

    dicionario=carregarDicionario()

    results_column = [
        [sg.Listbox(values=dicionario, enable_events=True, size=(10, 15), key="-lista-de-palavras-lista-", font=('Arial bold', 24), background_color='DimGray', text_color='White')],
        [sg.Text('Possibilidades: ' + str(len(dicionario)), key="-lista-de-palavras-possibilidades-", font=('Arial bold', 16))],
        [sg.Button('Reiniciar', key='-reiniciar-tela-', size=(10, 1),  border_width=0, button_color="DimGray", font=('Arial bold', 24))]
    ]

    return [
        [sg.Column(input_column, element_justification="c", key='-lista-de-inputs-'), sg.Column(results_column)],
        [teclado]
    ]

janela = sg.Window("Trapaça term.ooo", construirLayout(), finalize=True)
janela.bind('<BackSpace>', '-backspace-')

while True:
    evento, valores = janela.read()
    #print(evento, valores)
    if evento == sg.WIN_CLOSED:
        break
    elif evento.startswith('-campo-digitado-submit-'):
        num_linha = int(evento.split('-')[4])
        mapa = []
        for posicao in range(5):
            letra = janela['-campo-digitado-'+ str(num_linha) + '-'+str(posicao) ].get()
            verde = janela['-campo-digitado-radio-' + str(num_linha) + '-' + str(posicao) + '-verde'].get()
            amarelo = janela['-campo-digitado-radio-' + str(num_linha) + '-'+str(posicao) + '-amarelo'].get() 
            preto = janela['-campo-digitado-radio-' + str(num_linha) + '-'+str(posicao) + '-preto'].get()
            cor = 'verde' if verde else ('amarelo' if amarelo else 'preto') 
            mapa.append([letra, cor])
        # É preciso percorrer 2x por que pode ser que uma letra apareça preta no inicio da palavra e verde/amarela no final. 
        # Não podemos excluir todas as palavras com aquela letra, senao a palavra que tem a letra na posição correta
        # também é excluída.
        for posicao in range(5):
            if mapa[posicao][1] == 'verde':
                dicionario = manterSoPalavrasQueTemCertaLetraNaPosicaoEspecificada(dicionario, mapa[posicao][0], posicao)
                janela['-teclado-' + mapa[posicao][0]].update(button_color=('White', 'Turquoise'))
                janela['-campo-digitado-' + str(num_linha) + '-' + str(posicao)].update(background_color='Turquoise')
            elif mapa[posicao][1] == 'amarelo':
                dicionario = manterSoPalavrasQueTemCertaLetraERemoverPalavrasComLetraNaPosicaoErrada(dicionario, mapa[posicao][0], posicao, mapa)
                janela['-teclado-' + mapa[posicao][0]].update(button_color=('White', 'Gold'))
                janela['-campo-digitado-' + str(num_linha) + '-' + str(posicao)].update(background_color='Gold')
            elif mapa[posicao][1] == 'preto':
                dicionario = removerPalavrasQueTemCertaLetra(dicionario, mapa[posicao][0], posicao, mapa)
                janela['-teclado-' + mapa[posicao][0]].update(button_color=('LightGray', 'Gray'))
                janela['-campo-digitado-' + str(num_linha) + '-' + str(posicao)].update(background_color='Black')
            janela['-lista-de-palavras-lista-'].update(values=dicionario)
            janela['-lista-de-palavras-possibilidades-'].update('Possibilidades: ' + str(len(dicionario)))
    elif evento.startswith('-campo-digitado-') and janela[evento].get() != '':
        num_linha = int(evento.split('-')[3])
        num_coluna = int(evento.split('-')[4])
        janela[evento].update(janela[evento].get().upper()[0])
        pula_linha = True if num_coluna == 4 and num_linha < MAX_LINHAS-1 else False
        prox_foco_coluna = num_coluna if num_coluna == 4 and num_linha == MAX_LINHAS-1 else 0 if num_coluna == 4 else num_coluna + 1
        prox_foco_linha = num_linha if num_coluna == 4 and num_linha == MAX_LINHAS-1 else num_linha + 1 if num_coluna == 4 else num_linha
        if pula_linha:
            janela.extend_layout(janela['-lista-de-inputs-'], [construirLinhaDeCamposDigitaveis(prox_foco_linha)])
        janela['-campo-digitado-'+ str(prox_foco_linha) + '-'+str(prox_foco_coluna) ].set_focus()
    # Implementar tratamento correto quando for o último input digitável
    elif evento == '-backspace-':
        current_focus = janela.find_element_with_focus()
        if current_focus.key.startswith('-campo-digitado-'):
            num_linha = current_focus.key.split('-')[3]
            num_coluna = int(current_focus.key.split('-')[4])
            janela['-campo-digitado-' + num_linha + '-' + str(max([0, num_coluna-1]))].set_focus()
            janela['-campo-digitado-' + num_linha + '-' + str(max([0, num_coluna-1]))].update('')
    elif evento == '-reiniciar-tela-':
        janela.close()
        janela = sg.Window("Trapaça term.ooo", construirLayout(), finalize=True)
        janela.bind('<BackSpace>', '-backspace-')

janela.close()
