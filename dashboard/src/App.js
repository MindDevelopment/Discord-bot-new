import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './home';
import Login from './login';
import Commands from './commands';
import Console from './console';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/commands" element={<Commands />} />
        <Route path="/console" element={<Console />} />
      </Routes>
    </Router>
  );
}

export default App;
