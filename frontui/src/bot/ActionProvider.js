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
        /* This is such a jank way to do this lol prob will break */
        if (d.text.includes("When do you want")) {
          return createChatBotMessage(d.text, {
            widget: 'datePickerWidget'
          });
        }
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

    setState((prev) => {
      const newState = ({
        ...prev,
        messages: [...prev.messages].concat(botMessages),
      });
      /* Workaround for react-chatbot-kit saveMessages bug */
      window.localStorage.setItem('messageHistory', JSON.stringify(newState.messages))
      return newState;
    });
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
