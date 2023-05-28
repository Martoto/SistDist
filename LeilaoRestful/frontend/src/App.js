import React, { useEffect, useState } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import './App.css';
import Login from './Login';

import axios from 'axios'

function App() {
  const [getMessage, setGetMessage] = useState({})

  var source = new EventSource("{{ url_for('sse.stream') }}");

    source.addEventListener('publish', function(event) {
        var data = JSON.parse(event.data);
        console.log("The server says " + data.message);
    }, false);
    source.addEventListener('error', function(event) {
        console.log("Error"+ event)
        alert("Failed to connect to event stream. Is Redis running?");
    }, false);

  if(!token) {
    return <Login setToken={setToken} />
  }
  
  return (
    <Switch>
      <Route exact path="/" component={NameForm} />
      <Route path="/:id" component={UserPage} />
    </Switch>
  );
}

export default App;