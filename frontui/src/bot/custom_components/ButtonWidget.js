import React from "react";
import axios from 'axios';
import { createClientMessage } from "react-chatbot-kit";

import "../../App.css";

const ButtonWidget = (props) => {

  /* Widget for button options. */

  const options = props.payload.map((button, index) => {
    return { text: button.title, handler: () => {
      props.setState((prev) => ({
        ...prev,
        messages: [...prev.messages, createClientMessage(button.title)],
      }));
      axios.post('http://localhost:5005/webhooks/rest/webhook', {
        sender: "User",
        message: button.payload
        }).then(response => {
          console.log(props)
          props.actions.handleMessage(response.data);
        }
      );
    }, id: index}
  });

  const buttonsMarkup = options.map((option) => (
    <button key={option.id} onClick={option.handler} className="option-button">
      {option.text}
    </button>
  ));

  

  return <div className="react-chatbot-kit-chat-bot-message-container options-container">{buttonsMarkup}</div>;
};

export default ButtonWidget;