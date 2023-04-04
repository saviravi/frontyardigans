import Chatbot from "react-chatbot-kit";
import 'react-chatbot-kit/build/main.css'
import config from './config.js';
import MessageParser from './MessageParser.js';
import ActionProvider from './ActionProvider.js';
import { createChatBotMessage } from 'react-chatbot-kit';
// import {useState} from 'react';

const TravisBot = () => {

  const clearHistory = () => {
    window.localStorage.removeItem('messageHistory'); 
    window.location.reload(false);
  };

  const loadMessages = () => {
    const messages = window.localStorage.getItem('messageHistory')
    /* TODO maybe add a try-catch for json parse syntax error to be safe */
    return messages ? JSON.parse(messages) : [createChatBotMessage(`Hello there, I'm Travis! Send me anything to get started.`)] ;
  };

  return (
    <div>
        <button onClick={clearHistory}>Reset Chat</button>
        <Chatbot
            config={config}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
            messageHistory={loadMessages()}
        />
    </div>
  );
};

export default TravisBot;
