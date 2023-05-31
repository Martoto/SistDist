import React, { useState } from 'react';


async function postLeilao(credentials) {
    return fetch('http://localhost:5000/flask/leilao', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json())
   }

export default function CriarLeilao(token) {
  const [produto, setProduto] = useState();
  const [preco, setPreco] = useState();
  const [tempo, setTempo] = useState();


  const handleSubmit = async e => {  
    e.preventDefault();
    const ret = await postLeilao({
      produto, preco, tempo
    });
  }  


  return new Promise((resolve, reject) => {
    rl.question("Digite o nome do dono: ", (nomeDono) => {
        rl.question("Digite o nome do produto: ", (nomeProduto) => {
            rl.question("Digite a descrição do produto: ", (descricao) => {
                rl.question("Digite o preço base: ", (precoBase) => {
                    rl.question("Digite o limite de tempo (em segundos): ", (limiteTempo) => {
                        const novoLeilao = {
                            nomeDono: nomeDono,
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
});
}


