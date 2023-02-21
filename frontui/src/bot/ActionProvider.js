// in ActionProvider.jsx
import React from 'react';
import { createCustomMessage } from 'react-chatbot-kit';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const handleMessage = (data) => {
    /*
      Takes the response from Rasa and outputs a message box.
      Called by Message Parser
    */

    /* Widget example */
    // const botMessage = data.map(d => d.text ? createChatBotMessage(d.text) : createChatBotMessage("", {
    //   widget: 'imageWidget',
    //   payload: d.image
    // }));

    const botMessage = data.map(d => d.text ? createChatBotMessage(d.text) : createCustomMessage("", "imageMessage", {
      payload: d.image,
    }));

    setState((prev) => ({
      ...prev,
      messages: [...prev.messages].concat(botMessage),
    }));
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleMessage,
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;
