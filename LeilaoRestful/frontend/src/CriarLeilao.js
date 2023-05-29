import React, { useState } from 'react';
import PropTypes from 'prop-types';


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

export default function CriarLeilao({ setToken }) {
  const [produto, setproduto] = useState();

  const handleSubmit = async e => {  
    e.preventDefault();
    const token = await postLeilao({
      produto
    });
  }  


  return(
    <div >
      <h1>Criar leilao</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <p>produto</p>
          <input type="text" onChange={e => setproduto(e.target.value)}/>
        </label>
        <label>
          <p>preço</p>
          <input type="number" onChange={e => setproduto(e.target.value)}/>
        </label>
        <label>
          <p>tempo em segundos</p>
          <input type="number" onChange={e => setproduto(e.target.value)}/>
        </label>
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
    </div>
  )
}

