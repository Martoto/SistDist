from __future__ import print_function
import Pyro5.api
import Pyro5.server
from leiloes import leilao
from datetime import datetime
import time
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
            if (self.__listaLeiloes[leilao].acabou == 1):
                # adicionar para mandar notificação para quem é interessado
                print("Acabou o leilão de " +
                      self.__listaLeiloes[leilao].getNomeProduto())
# nomeProduto, descriçãoProduto, preçoBase, limiteTempo, limiteDia, clienteInstancia.uriCliente, clienteInstancia.nome

    def decrypt(self, msg, key):
        hash = SHA256.new(msg)
        try:
            pkcs1_15.new(key).verify(hash, signature)
            return True
        except (ValueError, TypeError):
            return False

    @Pyro5.server.expose
    def criarLeilao(self, nomeProduto, descriçãoProduto, preçoBase, limiteTempo, uri, nome):
        if nomeProduto in self.__listaLeiloes:
            raise ValueError('Já existe leilão com mesmo nome')
        self.__listaLeiloes[nomeProduto] = leilao(
            nomeProduto, descriçãoProduto, preçoBase, limiteTempo, uri)
        self.__listaLeiloes[nomeProduto].listaInteressados[nome] = uri

    @Pyro5.server.expose
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
    def darLance(self, valorLance, nomeProduto, uri, nome):
        print("Cliente " + nome + " tentou dar lance de " +
              valorLance + " em " + nomeProduto)
        for leilao in self.__listaLeiloes.keys():
            if (leilao == nomeProduto):
                if valorLance > self.__listaLeiloes[leilao].valorAtual:
                    self.__listaLeiloes[leilao].valorAtual = valorLance
                    self.__listaLeiloes[leilao].nomeComprador = nome
                    self.__listaLeiloes[leilao].listaInteressados[nome] = uri
                    return 1
                else:
                    return 0
        return 2
        # só retornar para a pessoa

    @Pyro5.server.expose
    def registrarCliente(self, nome, uriCliente, pubkey):
        print("Tentou Registrar Cliente " + nome)
        if nome in self.__listaClientes:
            raise ValueError('Já cliente com esse nome')
        print("Registrou cliente" + nome)
        self.__listaClientes[nome] = uriCliente, pubkey
