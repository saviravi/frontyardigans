import React from 'react';
import axios from 'axios';

const MessageParser = ({ children, actions }) => {

  /*
    Sends post request to rasa with user input as payload.
  */
  const parse = (message) => {
    if (actions.allowedNewMessage()) {
      if (/^(0[1-9]|1[012])\/(0[1-9]|[12][0-9]|3[01])\/(19|20)\d\d$/.test(message) 
        && window.localStorage.getItem('messageHistory')) {
        const history = JSON.parse(window.localStorage.getItem('messageHistory'))
        message = history[history.length - 1].message.includes('start') ? "Start on " + message : "End on " + message;
      }
      axios.post('http://localhost:5005/webhooks/rest/webhook', {
        sender: "User", 
        message: message
      }).then(response => {
        actions.handleMessage(response.data);
      }).catch(error => {
        console.log(error)
      });
    } else {
      actions.addChatbotMessage("Just one sec! Busy doing something");
    }
  };

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          parse: parse,
          actions,
        });
      })}
    </div>
  );
};

export default MessageParser;
