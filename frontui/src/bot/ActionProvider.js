// in ActionProvider.jsx
import React from 'react';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {
  const handleMessage = (data) => {
    /*
      Takes the response from Rasa and outputs a message box.
      Called by Message Parser
    */
    const botMessage = data.map(d => createChatBotMessage(d.text));

    // TODO: check if allow photos

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
