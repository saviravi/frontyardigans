import React, {useState} from 'react';
import {Text} from 'react-native';
import '../../App.css'
import Modal from 'react-bootstrap/Modal';
import axios from 'axios';
import { createClientMessage, createChatBotMessage } from "react-chatbot-kit";

const ItineraryMessage = (props) => {
  const [show, setShow] = useState(false);
  const resetMessage = "I want to start over!";

  const postReset = () => {
      props.setState((prev) => ({
        ...prev,
        messages: [...prev.messages, createClientMessage(resetMessage)],
      }));
      if (props.actions.allowedNewMessage()) {
        props.actions.toggleAllowNewMessage(false);
        axios.post('http://localhost:5005/webhooks/rest/webhook', {
        sender: "User",
        message: "/clear_slots"
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
        props.setState((prev) => ({
          ...prev,
          messages: [...prev.messages, createChatBotMessage("Please wait...")],
        }));
      }
  }

  return (
    <>
      <div className="react-chatbot-kit-chat-bot-message-container options-container">
        <button key={1} onClick={() => setShow(true)} className="option-button" style={{"fontWeight": "bolder"}}>
          Open Itinerary 
        </button>
        <button key={2} onClick={postReset} className="option-button">
          {resetMessage}
        </button>
      </div>

      <Modal
        show={show}
        onHide={() => setShow(false)}
        dialogClassName="modal-90w"
        aria-labelledby="example-custom-modal-styling-title"
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-custom-modal-styling-title">
            Your Customized Itinerary
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Text>
            {props.payload}
          </Text>
        </Modal.Body>
      </Modal>
      </>
  );
};

export default ItineraryMessage;



