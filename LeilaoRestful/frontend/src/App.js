import React, { useEffect, useState } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './App.css';
import Login from './Login';
import Layout from './Layout';
import NoPage from './NoPage';
import CriarLeilao from './CriarLeilao';
import DarLance from './DarLance';
function App() {
  const [token, setToken] = useState();


  if(!token) {
    return <Login setToken={setToken} />
  }
  
  return (
    <div className="wrapper">
      <h1>Application</h1>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<CriarLeilao />} />
            <Route path="darlance" element={<DarLance />} />
            <Route path="*" element={<NoPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;