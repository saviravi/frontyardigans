import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './navbar/Navbar';
import Welcome from './pages/welcome';
import TravisBot from "./bot/Chatbot";
import About from './pages/about';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return(
    <div>
      <Router>
        <Navbar sticky="top" />
        <Routes>
          <Route path='/' element={<Welcome />} />
          <Route path='/bot' element={<TravisBot />} />
          <Route path='/about' element={<About />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
