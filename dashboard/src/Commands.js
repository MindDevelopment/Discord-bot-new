import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import Login from './Login';
import Commands from './Commands';
import Console from './Console';

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
