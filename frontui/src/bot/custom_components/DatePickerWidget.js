import React, { useState } from "react";
import DatePicker from "react-datepicker";
import axios from 'axios';
import { createClientMessage, createChatBotMessage } from "react-chatbot-kit";
import moment from 'moment'

import "react-datepicker/dist/react-datepicker.css";

const DatePickerWidget = (props) => {
  const [date, setDate] = useState();

  const handler = () => {
    const message = (props.payload.includes("start")? "Start on " : "End on ") 
      + moment(date).format("MM/DD/YYYY");
    props.setState((prev) => ({
      ...prev,
      messages: [...prev.messages, createClientMessage(message)],
    }));
    if (props.actions.allowedNewMessage()) {
      axios.post('http://localhost:5005/webhooks/rest/webhook', {
        sender: "User",
        message: message
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
        }
      );
    } else {
      props.setState((prev) => ({
        ...prev,
        messages: [...prev.messages, createChatBotMessage("Please wait!")],
      }));
    }
  }

  return (
      <div className="datepicker-container" >
          <DatePicker className="option-button" placeholderText="MM/DD/YYYY" selected={date} onChange={(d) => setDate(d)} />
          <button onClick={handler} className="option-button">
                {" GO "}
          </button>
      </div>
  );

  
};

export default DatePickerWidget