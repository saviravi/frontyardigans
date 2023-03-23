import React, { useState } from "react";
import DatePicker from "react-datepicker";
import axios from 'axios';
import { createClientMessage } from "react-chatbot-kit";

import "react-datepicker/dist/react-datepicker.css";

const DatePickerWidget = (props) => {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());

  const handler = () => {
    props.setState((prev) => ({
      ...prev,
      messages: [...prev.messages, createClientMessage(startDate.toDateString() + " to " + endDate.toDateString())],
    }));
    axios.post('http://localhost:5005/webhooks/rest/webhook', {
      sender: "User",
      message: startDate.toDateString() + " to " + endDate.toDateString()
      }).then(response => {
        console.log(props)
        props.actions.handleMessage(response.data);
      }
    );
  }

  return (
      <div className="datepicker-container" >
          <DatePicker className="option-button" selected={startDate} onChange={(date) => setStartDate(date)} />
          <p style={{"margin": "auto"}}> {"to"}</p>
          <DatePicker className="option-button" selected={endDate} onChange={(date) => setEndDate(date)} />
          <button onClick={handler} className="option-button">
                {" GO "}
          </button>
      </div>
  );

  
};

export default DatePickerWidget