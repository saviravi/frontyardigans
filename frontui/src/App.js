import React from "react";
import Chatbot from "react-chatbot-kit";
import 'react-chatbot-kit/build/main.css'

import config from './Config.js';
import MessageParser from './MessageParser.js';
import ActionProvider from './ActionProvider.js';

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
