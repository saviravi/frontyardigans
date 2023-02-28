import React from "react";
import Chatbot from "react-chatbot-kit";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-chatbot-kit/build/main.css'
import './App.css'

import config from './bot/config.js';
import MessageParser from './bot/MessageParser.js';
import ActionProvider from './bot/ActionProvider.js';

const BotFrontend = () => {
  return (
    <div>
      <Chatbot
        config={config}
        messageParser={MessageParser}
        actionProvider={ActionProvider}
      />
    </div>
  );
};

export default BotFrontend;
