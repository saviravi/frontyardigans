import React from 'react';
import { createChatBotMessage } from 'react-chatbot-kit';
import BotAvatar from './BotAvatar';
import UserAvatar from './UserAvatar';
import ImageWidget from './custom_components/ImageWidget';
import ButtonWidget from './custom_components/ButtonWidget';
import ImageMessage from './custom_components/ImageMessage';

const botName = "Frontyadigans recommendation bot";

const config = {
  initialMessages: [createChatBotMessage(`Hello there, I'm ${botName}!`), ],
  botName: botName,
  customComponents: {
    botAvatar: (props) => <BotAvatar {...props} />,
    userAvatar: (props) => <UserAvatar {...props} />,
  },
  widgets: [
    {
      widgetName: "imageWidget",
      widgetFunc: (props) => <ImageWidget {...props} />,
    },
    {
      widgetName: "buttonWidget",
      widgetFunc: (props) => <ButtonWidget {...props} />,
    },
  ],
  customMessages: {
    imageMessage: (props) => <ImageMessage {...props} />,
  },
};

/* Note: imageWidget is not used  but there as an example*/

export default config;
