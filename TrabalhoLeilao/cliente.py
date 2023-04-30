import Pyro5.api
import logging
import threading
import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Telas.menu import telaLogin, telaMenu, telaCadastrar, telaListar, telaLance

class cliente():
    nome = ""
    key = ""
    uriCliente = ""

    def __init__(self):
        #abrir tela login
        event, values = telaLogin().read(close=True)
        self.nome = values['usuario']
        key = RSA.generate(2048)
        self.key = key
        print(self.nome)

    def pedeCriar(self, uriCliente):
        self.uriCliente = uriCliente

    def encrypt(self, msg):
        hash = SHA256.new(msg.encode('utf-8'))
        signature = pkcs1_15.new(self.key).sign(hash)
        return signature  



class CallbackHandler(object):
    @Pyro5.api.expose
    @Pyro5.api.callback
    def notificacao(self, acontecimento):
        print(acontecimento)


if __name__ == '__main__':
    clienteInstancia = cliente()
    daemon = Pyro5.api.Daemon()
    uriCliente = daemon.register(clienteInstancia)
    clienteInstancia.pedeCriar(uriCliente)
    callback = CallbackHandler()
    daemon.register(callback)

    servidorNomes = Pyro5.api.locate_ns()
    uriMercadoLeiloes = servidorNomes.lookup("Mercado de Leiloes")
    servidorMercadoLeiloes = Pyro5.api.Proxy(uriMercadoLeiloes)
    servidorMercadoLeiloes.registrarCliente(
        clienteInstancia.nome, clienteInstancia.uriCliente, clienteInstancia.key.publickey().export_key().decode('utf-8'))
    while (1):
        print("As opções do servidor são:\n")
        print("1 - Criar leilão\n")
        print("2 - Listar leilões\n")
        print("3 - Dar lance em um leilão\n")
        #abrir tela menu
        event, values = telaMenu().read(close=True)

        opcao = event
        if opcao == 'Cadastrar':
            nomeProduto = input("Qual o nome do produto?")
            descriçãoProduto = input("Qual a descrição do produto?")
            preçoBase = input("Qual o preço mínimo ?")
            limiteTempo = int(input(
                "Em quantos segundos deve expirar?"))
            servidorMercadoLeiloes.criarLeilao(nomeProduto, 
                                               descriçãoProduto, 
                                               preçoBase, 
                                               limiteTempo, 
                                               clienteInstancia.uriCliente, 
                                               clienteInstancia.nome,
                                               clienteInstancia.encrypt(clienteInstancia.uriCliente))
                
        if opcao == 'Listar':
            lista = servidorMercadoLeiloes.listarLeiloes()
            for name in lista:
                print("  %s " % (name))
        if opcao == 'Lance':
            nomeProduto = input("Qual o nome do produto em leilão?")
            valorLance = input("Qual o valor do seu lance?")
            resultadoLance = servidorMercadoLeiloes.darLance(valorLance,
                                                             nomeProduto,
                                                             clienteInstancia.uriCliente, 
                                                             clienteInstancia.nome,
                                                             clienteInstancia.encrypt(clienteInstancia.uriCliente))
            if (resultadoLance == 1):
                print("Lance Aceito")
            if (resultadoLance == 0):
                print("Lance Negado")
            if (resultadoLance == 2):
                print("Não existe Leilao com esse nome")
