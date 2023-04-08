import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Chatbot from "react-chatbot-kit";
import 'react-chatbot-kit/build/main.css';
import config from './config.js';
import MessageParser from './MessageParser.js';
import ActionProvider from './ActionProvider.js';
import { createChatBotMessage } from 'react-chatbot-kit';

const TravisBot = () => {
  const [showBot, toggleBot] = useState(true);

  const clearHistory = () => {
    window.localStorage.removeItem('messageHistory'); 
    window.location.reload(false);
  };

  const loadMessages = () => {
    const messages = window.localStorage.getItem('messageHistory');
    const initialButtons = [
      {
        title: "Hello!", 
        payload: "/greet"
      }, {
        title: "Are you a bot?", 
        payload: "/bot_challenge"
      }, {
        title: "I want to travel!",
        payload: "/ask_me_anything"
      }
    ];
    return messages ? JSON.parse(messages) : [createChatBotMessage(`Hello there, I'm Travis! Send me anything to get started.`, {
      widget: 'buttonWidget',
      payload: initialButtons
  })] ;
  };

  // Geolocation component
  const [lat, setLat] = useState(null);
  const [lon, setLon] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const geolocationAPI = navigator.geolocation;

  const getUserCoordinates = () => {
    if (!geolocationAPI) {
      setErrorMsg("Geolocation is not supported by your browser.")
      errorMsg && (
        <p className="error"> {errorMsg} </p>
      )
    } else {
      geolocationAPI.getCurrentPosition((position) => {
        const { coords } = position;
        setLat(coords.latitude);
        setLon(coords.longitude);
      }, (errorMsg) => {
        setErrorMsg("Something went wrong getting your position!")
        errorMsg && (
          <p className="error"> {errorMsg} </p>
        )
      })
    }
  }

  getUserCoordinates()

  // Offcanvas component
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <div>
        <div className='bot-page-button-container'>
          <Button id="bot-page-button" variant="primary" onClick={() => toggleBot((prev) => !prev)}>Show / Hide Bot</Button>
          <Button id="bot-page-button" variant="info" onClick={handleShow}>Information</Button>
          <Button id="bot-page-button" variant="danger" onClick={clearHistory}>Start Over</Button>
        </div>
        <div className='bot-page-offcanvas'>
          <Offcanvas show={show} onHide={handleClose}>
            <Offcanvas.Header closeButton>
              <Offcanvas.Title>Information</Offcanvas.Title>
            </Offcanvas.Header>
            <Offcanvas.Body>
              <div className="location-container">
                <p id="location">
                  <b>Latitude:</b> {lat}
                  <b> Longitude:</b> {lon}
                </p>
              </div>
            </Offcanvas.Body>
          </Offcanvas>
        </div>
        {showBot && (
        <Chatbot
            config={config}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
            messageHistory={loadMessages()}
        />)}
    </div>
  );
};

export default TravisBot;
