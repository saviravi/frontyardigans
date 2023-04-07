import React, { useState } from 'react';
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

  return (
    <div>
        <div className='bot-page-button-container'>
          <button id='bot-page-button-show-hide' onClick={() => toggleBot((prev) => !prev)}>Show / Hide Bot</button>
          <button id='bot-page-button-start-over' onClick={clearHistory}>Start Over</button>
        </div>
        {showBot && (
        <Chatbot
            config={config}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
            messageHistory={loadMessages()}
            />)}
        <div className="location-container">
          <p id="location">Your coordinates are: {[lat, lon]}</p>
        </div>
    </div>
  );
};

export default TravisBot;
