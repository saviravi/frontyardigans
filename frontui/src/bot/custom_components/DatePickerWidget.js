import React, { useState } from "react";
import DatePicker from "react-datepicker";
import axios from 'axios';
import { createClientMessage } from "react-chatbot-kit";
import moment from 'moment'

import "react-datepicker/dist/react-datepicker.css";

const DatePickerWidget = (props) => {
  const [date, setDate] = useState(new Date());

  const handler = () => {
    const message = moment(date).format("MM/DD/YYYY");
    props.setState((prev) => ({
      ...prev,
      messages: [...prev.messages, createClientMessage(message)],
    }));
    axios.post('http://localhost:5005/webhooks/rest/webhook', {
      sender: "User",
      message: message
      }).then(response => {
        console.log(props)
        props.actions.handleMessage(response.data);
      }
    );
  }

  return (
      <div className="datepicker-container" >
          <DatePicker className="option-button" selected={date} onChange={(d) => setDate(d)} />
          <button onClick={handler} className="option-button">
                {" GO "}
          </button>
      </div>
  );

  
};

export default DatePickerWidget