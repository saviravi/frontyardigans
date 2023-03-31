import React from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './navbar/Navbar';
import TravisBot from "./bot/Chatbot";
import Highlights from "./pages/highlights";
import About from './pages/about';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

function App() {
  return(
    <Router>
      <Navbar sticky="top" />
      <Routes>
        <Route path='/' element={<TravisBot />} />
        <Route path='/home' element={<TravisBot />} />
        <Route path='/highlights' element={<Highlights />} />
        <Route path='/about' element={<About />} />
      </Routes>
    </Router>
  );
}

export default App;
