from flask import Flask, jsonify, request, abort
from flask_sse import sse
from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask("Mercado Leilões")
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix="/stream")

listaLeiloes = [
    {
        'nomeDono': "Nome do Dono",
        'nomeProduto': "banana",
        'descricaoProduto': "ana",
        'precoBase': 1,
        'limiteTempo': 999999,
        'nomeComprador': "Ninguém",
        'valorAtual': 0,
        'acabou': 0,
    },
    {
        'nomeDono': "Nome do Dono",
        'nomeProduto': "maca",
        'descricaoProduto': "ana",
        'precoBase': 1,
        'limiteTempo': 5,
        'nomeComprador': "Ninguém",
        'valorAtual': 0,
        'acabou': 0,
    }, ]



def publish_sse_message(message, channel):
    with app.app_context():
        sse.publish({"message":message}, type=channel)


def atualizarLista():
    for produto in listaLeiloes:
        if (int(produto['acabou'] == 0)):
            if ((int(produto['limiteTempo']) <= 0)):
                produto['acabou'] = 1
                mensagem = "Acabou o leilão de {} por {} reais. {} Ganhou.".format(
                    produto['nomeProduto'], produto['valorAtual'], produto['nomeComprador'])
                print(mensagem)
                publish_sse_message(
                    mensagem, channel=str(produto['nomeProduto']))

            else:
                # print(produto['limiteTempo'])
                produto['limiteTempo'] = int(produto['limiteTempo'])-1
                # print(produto['limiteTempo'])
    return "Atualização do Segundo"


@app.route('/leiloes', methods=['GET'])
def listarLeiloes():
    retLeiloes = listaLeiloes
    for l in retLeiloes:
        #remove os leilões que já acabaram
        if (l['acabou'] == 1):
            retLeiloes.remove(l)
    return jsonify(retLeiloes)


@app.route('/leiloes/', methods=['POST'])
def criarLeilao():
    # {
    #    "nomeDono" : "Nome do Dono",
    #    "nomeProduto": "Coisa",
    #    "descricaoProduto": "Descrição",
    #    "preçoBase": 1,
    #    "limiteTempo": 10,
    #    "nomeComprador": "Nome do Comprador",
    #    "valorAtual": 0,
    #    "acabou": 0
    # }
    leilao = request.get_json()
    listaLeiloes.append(leilao)
    mensagem = "Novo leilão criado: {}".format(leilao['nomeProduto'])
    publish_sse_message(mensagem, channel='todosLeiloes')
    return jsonify(listaLeiloes)


@app.route('/leiloes/', methods=['PUT'])
def darLance():
    lance = request.get_json()
    # {
    #   "nomeProduto": "Coisa",
    #    "valor": 1,
    #    "nomeComprador": "Nome do Comprador",
    # }
    leilaoLance = "INEXISTENTE"
    for produto in listaLeiloes:
        if (produto['nomeProduto'] == lance['nomeProduto']):
            leilaoLance = produto
            break
    # Não existe um com esse nome
    if (leilaoLance == "INEXISTENTE"):
        abort(400, "Leilão com esse nome não existe")

    # Leilão já acabou
    if (leilaoLance['acabou'] == 1):
        abort(400, "Leilão já acabou")

    # Se o lance dado for maior que o valor atual
    if (lance['valor'] > leilaoLance['valorAtual']):
        leilaoLance['nomeComprador'] = lance['nomeComprador']
        leilaoLance['valorAtual'] = lance['valor']
    mensagem = "Novo lance de " + \
        str(leilaoLance['valorAtual']) + "reais em " + \
        str(leilaoLance['nomeProduto'])
    publish_sse_message(mensagem, channel=str(leilaoLance['nomeProduto']))
    

    return jsonify(listaLeiloes)

@app.route('/usuarios/', methods=['POST'])
def criarUsuario():
    # {
    #    "nome": "Nome do Usuário",
    # }
    usuario = request.get_json()
    return jsonify(usuario)


if __name__ == '__main__':
    from waitress import serve  
    print("Servidor iniciado")
    scheduler = BackgroundScheduler()
    scheduler.add_job(atualizarLista, 'interval', seconds=1)
    scheduler.start()
    serve(app, host='localhost', port=8080)
    #app.run(port=8080, host='localhost', debug=False)
