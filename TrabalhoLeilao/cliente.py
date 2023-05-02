import Pyro5.api
import logging
import threading
import sys
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import PySimpleGUI as sg
from Telas.menu import telaLogin, telaMenu, telaCadastrar, telaListar, telaLance

class cliente():
    nome = ""
    key = ""
    uriCliente = ""

    def __init__(self):
        #abrir tela login
        self.nome = input("Nome usuário")
        key = RSA.generate(2048)
        self.key = key
        print(self.nome)

    def pedeCriar(self, uriCliente):
        self.uriCliente = uriCliente


    def inicializaDaemon(self, daemon):
        daemon.requestLoop()

    def encrypt(self, msg):
        hash = SHA256.new(msg.encode('utf-8'))
        signature = pkcs1_15.new(self.key).sign(hash)
        return signature  




    @Pyro5.api.expose
    @Pyro5.api.callback
    def notificacao(self, acontecimento):
        print(acontecimento)


if __name__ == '__main__':
    clienteInstancia = cliente()
    daemon = Pyro5.api.Daemon()
    uriCliente = daemon.register(clienteInstancia)
    clienteInstancia.pedeCriar(uriCliente)
    daemonThread = threading.Thread(
        target=clienteInstancia.inicializaDaemon, args=(daemon,), daemon=True)
    daemonThread.start()

    servidorNomes = Pyro5.api.locate_ns()
    uriMercadoLeiloes = servidorNomes.lookup("Mercado de Leiloes")
    servidorMercadoLeiloes = Pyro5.api.Proxy(uriMercadoLeiloes)
    servidorMercadoLeiloes.registrarCliente(
                                           clienteInstancia.nome, 
                                           clienteInstancia.uriCliente, 
                                           clienteInstancia.key.publickey().export_key().decode('utf-8'))
    while (1): 
        input("Press enter to continue")
        print ("*****************************************************************\n")
        print("Bem vindo ao Mercado de Leilões, " + clienteInstancia.nome + "\n")
        print("As opções do servidor são:\n")
        print("1 - Criar leilão\n")
        print("2 - Listar leilões\n")
        print("3 - Dar lance em um leilão\n")
        print ("*****************************************************************\n")

        opcao = input()
        if opcao == '1':
            nomeProduto = input("Qual o nome do produto?")
            descriçãoProduto = input("Qual a descrição do produto?")
            preçoBase = input("Qual o preço mínimo ?")
            limiteTempo = int(input("Em quantos segundos deve expirar?"))
            servidorMercadoLeiloes.criarLeilao(nomeProduto, 
                                            descriçãoProduto, 
                                            preçoBase, 
                                            limiteTempo, 
                                            clienteInstancia.uriCliente, 
                                            clienteInstancia.nome,
                                            clienteInstancia.encrypt(clienteInstancia.nome))

        elif opcao == '2':
            lista = servidorMercadoLeiloes.listarLeiloes()
            print("Numero de leilões: %d" % (len(lista)))
            print("Leilões disponíveis:")
            print("----------------------")
            for name in lista:
                print("  %s " % (name))
                print("----------------------")

        elif opcao == '3':
            nomeProduto = input("Qual o nome do produto em leilão?")
            valorLance = input("Qual o valor do seu lance?")
            resultadoLance = servidorMercadoLeiloes.darLance(valorLance,
                                                            nomeProduto,
                                                            clienteInstancia.uriCliente, 
                                                            clienteInstancia.nome,
                                                            clienteInstancia.encrypt(clienteInstancia.nome))
            if resultadoLance == 1:
                print("Lance Aceito")
            elif resultadoLance == 0:
                print("Lance Negado")
            if (resultadoLance == 2):
                print("Leilão já acabou")
            if (resultadoLance == 3):
                print("Leilão com essa grafia não existe")

