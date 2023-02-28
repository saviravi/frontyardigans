// in ActionProvider.jsx
import React from 'react';
import { createCustomMessage } from 'react-chatbot-kit';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const handleMessage = (data) => {
    /*
      Takes the response from Rasa and outputs a message box.
      Called by Message Parser
    */

    // console.log(data)

    const botMessages = data.map(d => {
      if (d.text) {
        if (d.buttons) {
          return createChatBotMessage(d.text, {
              widget: 'buttonWidget',
              payload: d.buttons
          })
        } else {
          return createChatBotMessage(d.text);
        }
      } else {
        return createCustomMessage("", "imageMessage", {
          payload: d.image,
        })
      }
    });

    setState((prev) => ({
      ...prev,
      messages: [...prev.messages].concat(botMessages),
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
