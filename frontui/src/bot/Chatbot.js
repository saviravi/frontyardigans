import React, { useState } from 'react';
import Chatbot from "react-chatbot-kit";
import 'react-chatbot-kit/build/main.css';
import config from './config.js';
import MessageParser from './MessageParser.js';
import ActionProvider from './ActionProvider.js';

const TravisBot = () => {
  const [showBot, toggleBot] = useState(false);

  const saveMessages = (messages, HTMLString) => {
    localStorage.setItem('chat_messages', JSON.stringify(messages));
  };

  const loadMessages = () => {
    const messages = JSON.parse(localStorage.getItem('chat_messages'));
    return messages;
  };

  return (
    <div>
      {showBot && (
        <Chatbot
          config={config}
          actionProvider={ActionProvider}
          messageHistory={loadMessages()}
          messageParser={MessageParser}
          saveMessages={saveMessages}
        />
      )}
      <button onClick={() => toggleBot((prev) => !prev)}>Bot</button>
    </div>
  );
};

export default TravisBot;
