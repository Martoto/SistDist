from __future__ import print_function
import Pyro5.api
import Pyro5.server
from leiloes import leilao

# Mercado de Leilões


class mercadoLeiloes(object):
    __listaClientes = {}
    __listaLeiloes = {}

    def __init__(self):
        self.__listaLeiloes = {}
        self.__registros = {}

    def atualizarLista(self):
        for leilao in self.__listaLeiloes:
            leilao.atualizarTempo(self)
            if (leilao.acabou == 1):
                # adicionar para mandar notificação para quem é interessado
                print("Acabou o leilão")

    @Pyro5.server.expose
    def criarLeilao(self, nomeProduto, descriçãoProduto, preçoBase, limiteTempo, uri):
        if nomeProduto in self.__listaLeiloes:
            raise ValueError('Já existe leilão com mesmo nome')
        self.__listaLeiloes[nomeProduto] = leilao(
            nomeProduto, descriçãoProduto, preçoBase, limiteTempo, uri)

    @Pyro5.server.expose
    def listarLeiloes(self):
        listaLeiloesRetorno = {}
        for leilao in self.__listaLeiloes.keys():
            listaLeiloesRetorno[leilao] = self.__listaLeiloes[leilao].getNomeProduto(
            )
        return listaLeiloesRetorno

    @Pyro5.server.expose
    def darLance(self, valorLance, nomeProduto, uri, nome):
        for leilao in self.__listaLeiloes.keys():
            if (leilao == nomeProduto):
                if valorLance > self.__listaLeiloes[leilao].valorAtual:
                    self.__listaLeiloes[leilao].valorAtual = valorLance
                    self.__listaLeiloes[leilao].nomeComprador = nome

                    return 1
                else:
                    return 0
        return 2
        # só retornar para a pessoa

    @Pyro5.server.expose
    def registrarCliente(self, nome, uriCliente):
        if nome in self.__listaClientes:
            raise ValueError('Já cliente com esse nome')
        self.__listaClientes[nome] = uriCliente
