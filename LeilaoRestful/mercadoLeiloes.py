from __future__ import print_function
import Pyro5.api
import Pyro5.server
from leiloes import leilao
from datetime import datetime
import time
import base64
from apscheduler.schedulers.background import BackgroundScheduler
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

# Mercado de Leilões


class mercadoLeiloes(object):
    __listaClientes = {}
    __listaLeiloes = {}

    def __init__(self):
        self.__listaLeiloes = {}
        self.__registros = {}

    def atualizarLista(self):
        for leilao in self.__listaLeiloes.keys():
            self.__listaLeiloes[leilao].atualizarTempo()
            if (self.__listaLeiloes[leilao].acabou == 1 and 
                self.__listaLeiloes[leilao].mandouMensagemTermino == 0):
                mensagem = "O leilão de " + leilao + " acabou. O ganhador foi " + \
                    self.__listaLeiloes[leilao].nomeComprador + \
                    " pelo preço de " + self.__listaLeiloes[leilao].valorAtual
                for nomeInteressado in self.__listaLeiloes[leilao].listaInteressados.keys():
                    user = Pyro5.api.Proxy(
                        self.__listaLeiloes[leilao].listaInteressados[nomeInteressado])
                    user.notificacao(mensagem)
                self.__listaLeiloes[leilao].mandouMensagemTermino = 1


    def criarLeilao(self,
                    nomeProduto,
                    descriçãoProduto,
                    preçoBase,
                    limiteTempo,
                    uri,
                    nome):
        if nomeProduto in self.__listaLeiloes:
            raise ValueError('Já existe leilão com mesmo nome')

        print("Cliente " + nome + " tentou criar leilão de " + nomeProduto)

        self.__listaLeiloes[nomeProduto] = leilao(
            nomeProduto, descriçãoProduto, preçoBase, limiteTempo, uri)
        self.__listaLeiloes[nomeProduto].listaInteressados[nome] = uri
        mensagem = "Novo leilão de " + nomeProduto
        for nomeInteressado in self.__listaClientes.keys():
            user = Pyro5.api.Proxy(self.__listaClientes[nomeInteressado])
            user.notificacao(mensagem)

    def listarLeiloes(self):
        listaLeiloesRetorno = {}
        for leilao in self.__listaLeiloes:
            print(leilao)
        for leilao in self.__listaLeiloes.keys():
            if (self.__listaLeiloes[leilao].acabou != 1):
                listaLeiloesRetorno[leilao] = self.__listaLeiloes[leilao].getNomeProduto(
                )
            print(leilao)
        return listaLeiloesRetorno

    @Pyro5.server.expose
    def darLance(self,
                 valorLance,
                 nomeProduto,
                 uri,
                 nome
                 ):

        print("Cliente " + nome + " tentou dar lance de " +
              valorLance + " em " + nomeProduto)
        mensagem = nome + " deu lance de " + valorLance + " em " + nomeProduto
        for leilao in self.__listaLeiloes.keys():
            if (leilao == nomeProduto):
                if (valorLance > self.__listaLeiloes[leilao].valorAtual and self.__listaLeiloes[leilao].acabou == 0):
                    self.__listaLeiloes[leilao].valorAtual = valorLance
                    self.__listaLeiloes[leilao].nomeComprador = nome
                    self.__listaLeiloes[leilao].listaInteressados[nome] = uri
                    for nomeInteressado in self.__listaLeiloes[leilao].listaInteressados.keys():
                        user = Pyro5.api.Proxy(
                            self.__listaLeiloes[leilao].listaInteressados[nomeInteressado])
                        user.notificacao(mensagem)
                    return 1
                else:
                    if self.__listaLeiloes[leilao].acabou == 0:
                        return 0
                    else:
                        return 2
        return 3
        # só retornar para a pessoa

    def registrarCliente(self, nome, uriCliente):
        print("Tentou Registrar Cliente " + nome)
        if nome in self.__listaClientes:
            raise ValueError('Já cliente com esse nome')
        print("Registrou cliente" + nome)
        mensagem = "Registro do cliente " + nome
        self.__listaClientes[nome] = uriCliente
        user = Pyro5.api.Proxy(self.__listaClientes[nome])
        user.notificacao(mensagem)
