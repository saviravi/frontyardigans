import React from "react";
import axios from 'axios';
import { createClientMessage, createChatBotMessage } from "react-chatbot-kit";

import "../../App.css";

const ButtonWidget = (props) => {

  /* Widget for button options. */

  const options = props.payload.map((button, index) => {
    return { text: button.title, handler: () => {
      const botMessage = (button.title === "Generate" ? 
        createChatBotMessage("Generating your itinerary. Please wait") : 
        createClientMessage(button.title));
      props.setState((prev) => ({
        ...prev,
        messages: [...prev.messages, botMessage ],
      }));
      if (props.actions.allowedNewMessage()) {
        props.actions.toggleAllowNewMessage(false);
        axios.post('http://localhost:5005/webhooks/rest/webhook', {
        sender: "User",
        message: button.payload
        }).then(response => {
          if (response.data && response.data.length > 0) {
            props.actions.handleMessage(response.data);
          } else {
            axios.post('http://localhost:5005/webhooks/rest/webhook', {
              sender: "User",
              message: "/nlu_fallback"
              }).then(response => {
                props.actions.handleMessage(response.data);
              }
            );
          }
        }).catch(error => {
          console.log(error)
        }).finally(() => {
          props.actions.toggleAllowNewMessage(true);
        });
      } else {
        button.title !== "Generate" && props.setState((prev) => ({
          ...prev,
          messages: [...prev.messages, createChatBotMessage("Please wait...")],
        }));
      }
      
    }, id: index}
  });

  const buttonsMarkup = options.map((option) => (
    <button key={option.id} onClick={option.handler} className="option-button" style={option.text === "Generate" ? {"fontWeight": "bolder"}: {}}>
      {option.text}
    </button>
  ));

  

  return <div className="react-chatbot-kit-chat-bot-message-container options-container">{buttonsMarkup}</div>;
};

export default ButtonWidget;