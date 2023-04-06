import React, { useState } from 'react';
import Chatbot from "react-chatbot-kit";
import 'react-chatbot-kit/build/main.css';
import config from './config.js';
import MessageParser from './MessageParser.js';
import ActionProvider from './ActionProvider.js';
import { createChatBotMessage } from 'react-chatbot-kit';
// import {useState} from 'react';

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

  return (
    <div>
        <button onClick={clearHistory}>Reset Chat</button>
        {showBot && (
        <Chatbot
            config={config}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
            messageHistory={loadMessages()}
            />)}
        <button onClick={() => toggleBot((prev) => !prev)}>Bot</button>
    </div>
  );
};

export default TravisBot;
