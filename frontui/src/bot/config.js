import React from 'react';
import { createChatBotMessage } from 'react-chatbot-kit';
import BotAvatar from './BotAvatar';
import UserAvatar from './UserAvatar';

const botName = "Frontyadigans recommendation bot"

const config = {
  initialMessages: [createChatBotMessage(`Hello there, I'm ${botName}!`)],
  botName: botName,
  customComponents: {
    botAvatar: (props) => <BotAvatar {...props}/>,
    userAvatar: (props) => <UserAvatar {...props} />,
  },
};

export default config;
