import Chatbot from "react-chatbot-kit";
import 'react-chatbot-kit/build/main.css'
import config from './config.js';
import MessageParser from './MessageParser.js';
import ActionProvider from './ActionProvider.js';

const TravisBot = () => {
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

export default TravisBot;
