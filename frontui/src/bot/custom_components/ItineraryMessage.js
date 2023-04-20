import React, {useState} from 'react';
import {Text} from 'react-native';
import '../../App.css'
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import axios from 'axios';
import toast, { Toaster } from 'react-hot-toast';
import {EditText} from 'react-edit-text';
import { createClientMessage, createChatBotMessage } from "react-chatbot-kit";

const ItineraryMessage = (props) => {
  const [show, setShow] = useState(false);
  const [itineraryTitle, setItineraryTitle] = useState((props.payload.match(/Destination: (.*)\n$/gm) ?
  props.payload.match(/Destination: (.*)\n$/gm)[0].substring(13, props.payload.match(/Destination: (.*)\n$/gm)[0].length-1)
  :"Untitled") + " Itinerary");
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

  const saveItinerary = () => {
    let itineraries = JSON.parse(window.localStorage.getItem('itinerary'));
    if (itineraries && Array.isArray(itineraries)) {
      itineraries = JSON.stringify(itineraries.concat([{"title": itineraryTitle, "text": props.payload}]))
      window.localStorage.setItem('itinerary', itineraries)
    } else {
      window.localStorage.setItem('itinerary', JSON.stringify([{"title": itineraryTitle, "text": props.payload}]))
    }
    setShow(false);
    toast.success('Itinerary saved.', {
      style: {
        border: '1px solid #6f4394',
        padding: '16px',
        color: '#6f4394',
      },
      iconTheme: {
        primary: '#6f4394',
        secondary: '#FFFAEE',
      },
    });
  }

  return (
    <>
      <div className="react-chatbot-kit-chat-bot-message-container options-container">
        <button key={1} onClick={() => setShow(true)} className="option-button" style={{"fontWeight": "bolder"}}>
          Open Itinerary 
        </button>
        <button key={2} onClick={saveItinerary} className="option-button">
          Quick Save 
        </button>
        <button key={3} onClick={postReset} className="option-button">
          {resetMessage}
        </button>
      </div>
      <Toaster
        position="bottom-right"
        reverseOrder={false}
      />
      <Modal
        show={show}
        onHide={() => setShow(false)}
        dialogClassName="modal-90w"
        aria-labelledby="example-custom-modal-styling-title"
      >
        <Modal.Header closeButton>
          <Modal.Title id="example-custom-modal-styling-title">
            <EditText
                name="title-text-box"
                value={itineraryTitle}
                onChange={(e) => setItineraryTitle(e.target.value)}
              />
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Text>
            {props.payload}
          </Text>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShow(false)}>Close</Button>
          <Button variant="primary" onClick={saveItinerary}>Save</Button>
        </Modal.Footer>
      </Modal>
      </>
  );
};

export default ItineraryMessage;



