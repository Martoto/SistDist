from typing import Any


class leilao:
    nomeProduto = ""
    descriçãoProduto = ""
    preçoBase = 0
    limiteTempo = 9999
    nomeComprador = ""
    valorAtual = 0
    acabou = 0
    uriComitante = ""
    listaInteressados = {}

    def __init__(self, nomeProduto, descriçãoProduto, precoBase, limiteTempo, uri):
        self.nomeProduto = nomeProduto
        self.descriçãoProduto = descriçãoProduto
        self.preçoBase = precoBase
        self.limiteTempo = limiteTempo
        self.nomeComprador = None
        self.valorAtual = precoBase
        self.uriComitante = uri

    def darLanceLeilao(self, valorLance, nomeComprador, uri):
        # adicionar uri na lista de interessados
        print("entrou no append")
        self.listaInteressados.append(uri)
        print("passou do append")
        if valorLance > self.valorAtual:
            self.nomeComprador = nomeComprador
            self.valorAtual = valorLance
            print("aceitou o lance")
            return 1
        else:
            print("rejeitou o lance")
            return 0

    def getNomeProduto(self):
        return self.nomeProduto

    def atualizarTempo(self):
        limiteTempo = limiteTempo-1
        if limiteTempo <= 0:
            acabou = 1
        else:
            acabou = 0
        return
