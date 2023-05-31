const dns = require('node:dns');
const EventSource = require('eventsource');
const fetch = require('node-fetch');

dns.setDefaultResultOrder('ipv4first');


const endpoint = 'http://localhost:8080/stream';

const eventSource = new EventSource(endpoint);
const readline = require('readline');
const { parse } = require('node:path');
var userToken = "";
//lista dos leiloes que o usuario esta inscrito
const listeners = [];


const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

eventSource.addEventListener('publish', function(event) {
    var data = JSON.parse(event.data);
    console.log("The server says " + data.message);
}, false);
eventSource.addEventListener('error', function(event) {
    console.log("Error"+ event)
    alert("Failed to connect to event stream. Is Redis running?");
}, false);

// Função para enviar um novo lance
function darLance() {
    rl.question("Digite o nome do produto: ", (nomeProduto) => {
        rl.question("Digite o valor do lance: ", (valor) => {
            const lance = {
                nomeProduto: nomeProduto,
                valor: parseFloat(valor),
                nomeComprador: userToken
            };

            // Lógica para enviar o lance para a API (usando fetch, por exemplo)
            fetch('http://localhost:8080/leiloes/', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(lance)
            })
                .then(response => response.json())
                .then(listaLeiloes => {
                    console.log("Lance realizado com sucesso!");
                    console.log("===== Lista de Leilões Atualizada =====");
                    console.log(listaLeiloes);
                    console.log("===========================");
                    //inscreve o usuario no leilao
                    if (!listeners.includes(nomeProduto)) {
                        eventSource.addEventListener(nomeProduto, function(event) {
                            var data = JSON.parse(event.data);
                            console.log("NOTIFICACAO PRODUTO " + data.message);
                        }, false);
                        listeners.push(nomeProduto);
                    }
                    // Retornar ao menu principal
                    iniciarCliente();
                })
                .catch(error => {
                    console.log("Erro ao realizar o lance:", error);
                    // Retornar ao menu principal
                    iniciarCliente();
                });
        });
    });
}


function criarLeilao() {
    return new Promise((resolve, reject) => {
        rl.question("Digite o nome do produto: ", (nomeProduto) => {
            rl.question("Digite a descrição do produto: ", (descricao) => {
                rl.question("Digite o preço base: ", (precoBase) => {
                    rl.question("Digite o limite de tempo (em segundos): ", (limiteTempo) => {
                        const novoLeilao = {
                            nomeDono: userToken,
                            nomeProduto: nomeProduto,
                            descricaoProduto: descricao,
                            precoBase: parseFloat(precoBase),
                            limiteTempo: parseInt(limiteTempo),
                            nomeComprador: "Ninguém",
                            valorAtual: 0,
                            acabou: 0
                        };

                        // Lógica para enviar o novo leilão para a API (usando fetch, por exemplo)
                        fetch('http://localhost:8080/leiloes/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(novoLeilao)
                        })
                            .then(response => response.json())
                            .then(listaLeiloes => {
                                console.log("Novo leilão criado com sucesso!");
                                console.log("===== Lista de Leilões Atualizada =====");
                                console.log(listaLeiloes);
                                console.log("===========================");
                            //inscreve o usuario no leilao
                            if (!listeners.includes(nomeProduto)) {
                                eventSource.addEventListener(nomeProduto, function(event) {
                                    var data = JSON.parse(event.data);
                                    console.log("NOTIFICACAO PRODUTO " + data.message);
                                }, false);
                                listeners.push(nomeProduto);
                            }
                                resolve(listaLeiloes);
                            })
                            .catch(error => {
                                console.log("Erro ao criar novo leilão:", error);
                                reject(error);
                            });
                    });
                });
            });
        });
    });
}




function listarLeiloes() {
    // Lógica para obter os leilões da API (usando fetch, por exemplo)
    fetch('http://localhost:8080/leiloes')
        .then(response => response.json())
        .then(leiloes => {
            console.log("===== Lista de Leilões =====");
            leiloes.forEach(leilao => {
                console.log("Nome do Dono:", leilao.nomeDono);
                console.log("Nome do Produto:", leilao.nomeProduto);
                console.log("Descrição do Produto:", leilao.descricaoProduto);
                console.log("Preço Base:", leilao.precoBase);
                console.log("Limite de Tempo:", leilao.limiteTempo);
                console.log("===========================");
            });
        })
        .catch(error => {
            console.log("Erro ao listar os leilões:", error);
        });
}

function exibirMenu() {
    console.log("============================");
    console.log(userToken);
    console.log("1. Listar Leilões");
    console.log("2. Criar Leilão");
    console.log("3. Dar Lance");
    console.log("4. Imprimir menu novamente");
    console.log("0. Sair");
    console.log("===========================");
    console.log("");
}

function processarEscolha(escolha) {
    switch (escolha) {
        case '1':
            listarLeiloes();
            break;
        case '2':
            criarLeilao()
                .then(() => {
                    iniciarCliente();
                })
                .catch((error) => {
                    console.log("Erro ao criar leilão:", error);
                    iniciarCliente();
                });
            break;
        case '3':
            darLance();
            break;
        default:
            console.log("Escolha inválida. Tente novamente.");
            iniciarCliente();
            break;
    }
}

function obterToken() {
    return new Promise((resolve, reject) => {
        rl.question("Digite o seu nome: ", (nome) => {
            // Lógica para obter o token da API (usando fetch, por exemplo)
            fetch('http://localhost:8080/usuarios/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ nome: nome })
            })
                .then(response => response.json())
                .then(token => {
                    console.log("Token obtido com sucesso:", token);
                    resolve(token);
                })
                .catch(error => {
                    console.log("Erro ao obter o token:", error);
                    reject(error);
                });
        });
    });
}

function iniciarCliente() {

    exibirMenu();

    rl.question("Digite sua escolha: ", (escolha) => {
        // Obtém o primeiro caractere da escolha
        const primeiroCaractere = escolha.charAt(0);

        // Chame a função processarEscolha com o primeiro caractere
        processarEscolha(primeiroCaractere);

        if (primeiroCaractere !== '0') {
            iniciarCliente();
        }
    });
}

function main() {
    obterToken()
        .then((token) => {
            userToken = token;

            // Iniciar o cliente
            iniciarCliente();
        })
        .catch((error) => {
            console.log("Erro ao obter o token:", error);
        });
}   

main();