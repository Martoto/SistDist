from typing import Any
from time import gmtime, strftime


class leilao:
    nomeProduto = ""
    descriçãoProduto = ""
    preçoBase = 0
    limiteTempo = 999999
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
        self.mandouMensagemTermino = 0

    def getNomeProduto(self):
        return self.nomeProduto

    def atualizarTempo(self):
        self.limiteTempo = self.limiteTempo-1
        if (self.limiteTempo <= 0):
            self.acabou = 1
        else:
            self.acabou = 0
        return
