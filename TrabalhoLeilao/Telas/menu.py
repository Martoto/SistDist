import PySimpleGUI as sg

# Layout
def telaMenu():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Menu', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Cadastrar', size=(20, 2))],
        [sg.Button('Listar', size=(20, 2))],
        [sg.Button('Sair', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Menu', layout=layout, finalize=True)

def telaCadastrar():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Cadastrar', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Text('Nome', size=(10, 1)), sg.Input(size=(20, 1), key='nome')],
        [sg.Text('Descrição', size=(10, 1)), sg.Input(size=(20, 1), key='descricao')],
        [sg.Text('Preço', size=(10, 1)), sg.Input(size=(20, 1), key='preco')],
        [sg.Text('Tempo', size=(10, 1)), sg.Input(size=(20, 1), key='tempo')],
        [sg.Button('Cadastrar', size=(20, 2))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Cadastrar', layout=layout, finalize=True)

def telaListar():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Listar', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Listar', size=(20, 2))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Listar', layout=layout, finalize=True)

def telaLance():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Lance', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Text('Nome', size=(10, 1)), sg.Input(size=(20, 1), key='nome')],
        [sg.Text('Valor', size=(10, 1)), sg.Input(size=(20, 1), key='valor')],
        [sg.Button('Lance', size=(20, 2))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Lance', layout=layout, finalize=True)

def telaLanceAceito():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Lance Aceito', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Lance Aceito', layout=layout, finalize=True)

def telaLanceNegado():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Lance Negado', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Lance Negado', layout=layout, finalize=True)

def telaLanceInvalido():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Lance Inválido', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Lance Inválido', layout=layout, finalize=True)

def telaLanceTempo():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Tempo Esgotado', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Tempo Esgotado', layout=layout, finalize=True)

def telaLanceValor():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Lance Menor que o valor atual', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Lance Menor que o valor atual', layout=layout, finalize=True)

def telaLanceNome():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Nome não encontrado', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Nome não encontrado', layout=layout, finalize=True)

def telaLanceNomeInvalido():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Nome Inválido', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Nome Inválido', layout=layout, finalize=True)

def telaLanceValorInvalido():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Valor Inválido', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Valor Inválido', layout=layout, finalize=True)

def telaLanceTempoInvalido():
    sg.theme('DarkAmber')
    layout = [
        [sg.Text('Tempo Inválido', size=(10, 1), justification='center', font=("Helvetica", 25))],
        [sg.Button('Voltar', size=(20, 2))]
    ]
    # Janela
    return sg.Window('Tempo Inválido', layout=layout, finalize=True)



