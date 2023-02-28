import React from 'react';
import axios from 'axios';

const MessageParser = ({ children, actions }) => {

  /*
    Sends post request to rasa with user input as payload.
  */
  const parse = (message) => {
    axios.post('http://localhost:5005/webhooks/rest/webhook', {
      sender: "User", 
      message: message
    }).then(response => {
        actions.handleMessage(response.data);
      }
    );
    
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
