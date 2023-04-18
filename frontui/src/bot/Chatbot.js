import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Offcanvas from 'react-bootstrap/Offcanvas';
import Geocode from "react-geocode";
import Chatbot from "react-chatbot-kit";
import 'react-chatbot-kit/build/main.css';
import config from './config.js';
import MessageParser from './MessageParser.js';
import ActionProvider from './ActionProvider.js';
import { createChatBotMessage } from 'react-chatbot-kit';
import axios from 'axios';
import Modal from 'react-bootstrap/Modal';
import {Text} from 'react-native';
import {EditText} from 'react-edit-text';
import toast, { Toaster } from 'react-hot-toast';

const TravisBot = () => {
  const [showBot, toggleBot] = useState(true);
  const [itineraries, setItineraries] = useState([]);
  const [showItinerary, toggleItinerary] = useState(false);
  const [itineraryIndex, setItineraryIndex] = useState(0);
  const [itineraryTitle, setItineraryTitle] = useState("");
  const [itineraryText, setItinerary] = useState("");
  const [showDeleteConfirmation, toggleDeleteConfirmation] = useState(false);

  const clearHistory = () => {
    axios.post('http://localhost:5005/webhooks/rest/webhook', {
        sender: "User",
        message: "/clear_slots"
        }).then(() => {
          console.log("Slots cleared");
        }).finally(() => {
          window.localStorage.removeItem('messageHistory'); 
          window.location.reload(false);
        });
  };

  const loadMessages = () => {
    const messages = window.localStorage.getItem('messageHistory');
    const initialButtons = [
      {
        title: "Hello!", 
        payload: "/greet"
      }, {
        title: "Are you a bot?", 
        payload: "/bot_challenge"
      }, {
        title: "I want to travel!",
        payload: "/ask_me_anything"
      }
    ];
    return messages ? JSON.parse(messages) : [createChatBotMessage(`Hello there, I'm Travis! Send me anything to get started.`, {
      widget: 'buttonWidget',
      payload: initialButtons
  })] ;
  };

  // Geolocation component
  const [lat, setLat] = useState(null);
  const [lon, setLon] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const geolocationAPI = navigator.geolocation;

  const getUserCoordinates = () => {
    if (!geolocationAPI) {
      setErrorMsg("Geolocation is not supported by your browser.")
      errorMsg && (
        <p className="error"> {errorMsg} </p>
      )
    } else {
      geolocationAPI.getCurrentPosition((position) => {
        const { coords } = position;
        setLat(coords.latitude);
        setLon(coords.longitude);
      }, (errorMsg) => {
        setErrorMsg("Something went wrong getting your position!")
        errorMsg && (
          <p className="error"> {errorMsg} </p>
        )
      })
    }
  }

  getUserCoordinates()

  // Offcanvas component
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  // Geocode component
  const [city, setCity] = useState(null);
  const [state, setState] = useState(null);
  const [country, setCountry] = useState(null);
  const [address, setAddress] = useState(null);
  Geocode.setApiKey("AIzaSyCLoKbJHEtxGv6vtRmAJRnJqIv9RCS-TiU")
  Geocode.setLanguage("en")
  //Geocode.setRegion("us")
  Geocode.setLocationType("ROOFTOP")
  Geocode.enableDebug()
  // Get formatted address, city, state, country from latitude & longitude when
  // Geocode.setLocationType("ROOFTOP") enabled
  // the below parser will work for most of the countries
  Geocode.fromLatLng(lat, lon).then(
    (response) => {
      const address = response.results[0].formatted_address;
      let city, state, country;
      for (let i = 0; i < response.results[0].address_components.length; i++) {
        for (let j = 0; j < response.results[0].address_components[i].types.length; j++) {
          switch (response.results[0].address_components[i].types[j]) {
            case "locality":
              city = response.results[0].address_components[i].long_name;
              break;
            case "administrative_area_level_1":
              state = response.results[0].address_components[i].long_name;
              break;
            case "country":
              country = response.results[0].address_components[i].long_name;
              break;
            default:
              break;
          }
        }
      }
      console.log(city, state, country);
      setCity(city);
      setState(state);
      setCountry(country);
      console.log(address);
      setAddress(address);
    },
    (error) => {
      console.error(error);
    }
  );

  useEffect(() => {
    if (show) {
      const fetchedList = JSON.parse(window.localStorage.getItem('itinerary'));
      setItineraries(fetchedList && Array.isArray(fetchedList) ? fetchedList : []);
    } 
  },[show]);

  const viewItinerary = (key, title, text) => {
    setItinerary(text)
    setItineraryTitle(title);
    setItineraryIndex(key);
    toggleItinerary(true);
  }

  const saveItineraryChanges = () => {
    let itin = itineraries;
    itin[itineraryIndex] = {"title": itineraryTitle, "text": itineraryText};
    setItineraries(itin);
    window.localStorage.setItem('itinerary', JSON.stringify(itin));
    toggleItinerary(false);
  }

  const saveItineraryDelete = () => {
    let itin = itineraries;
    itin.splice(itineraryIndex, 1);
    setItineraries(itin);
    window.localStorage.setItem('itinerary', JSON.stringify(itin));
    toggleItinerary(false);
    toast.success('Itinerary deleted.', {
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

  const deleteAllItineraries = () => {
    setItineraries([]);
    window.localStorage.removeItem('itinerary');
    toast.success('All itineraries deleted.', {
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
    toggleDeleteConfirmation(false);
  }

  return (
    <div className="bot-page-container">
        <div className='bot-page-button-container'>
          <Button id="bot-page-button" variant="primary" onClick={() => toggleBot((prev) => !prev)}>Show / Hide Bot</Button>
          <Button id="bot-page-button" variant="info" onClick={handleShow}>Information</Button>
          <Button id="bot-page-button" variant="danger" onClick={clearHistory}>Start Over</Button>
        </div>
        <div className='bot-page-offcanvas'>
          <Offcanvas show={show} onHide={handleClose}>
            <Offcanvas.Header closeButton>
              <Offcanvas.Title>Information</Offcanvas.Title>
            </Offcanvas.Header>
            <Offcanvas.Body>
              <div className="information-container">
                <div className="location-container">
                  <p id="location">
                    <b>Address:</b><br/> {address}<br/>
                    <b>City:</b> {city}, {state}, {country}<br/>
                    <b>Latitude:</b> {lat}<br/>
                    <b>Longitude:</b> {lon}
                  </p>
                </div>
              </div>
              <div className="itineraries-container">
                {itineraries.map((name, index) => {
                  return <Button id="bot-page-button" key={index + 1} variant="secondary" onClick={() => viewItinerary(index, name.title, name.text)}>
                    {name.title}
                    </Button>})}
                      {itineraries.length > 0 && <Button id="bot-page-button" key={0} variant="danger" onClick={() => toggleDeleteConfirmation(true)}>
                      Delete All
                    </Button>}
              </div>
            </Offcanvas.Body>
          </Offcanvas>
        </div>
        {showBot && (
        <Chatbot
            config={config}
            messageParser={MessageParser}
            actionProvider={ActionProvider}
            messageHistory={loadMessages()}
        />)}
        <Toaster
        position="bottom-right"
        reverseOrder={false}
        />
        <Modal
        show={showItinerary}
        onHide={saveItineraryChanges}
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
            {itineraryText}
          </Text>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" onClick={saveItineraryDelete}>Delete</Button>
          <Button variant="secondary" onClick={saveItineraryChanges}>Close</Button>
        </Modal.Footer>
      </Modal>
      <Modal show={showDeleteConfirmation} onHide={() => toggleDeleteConfirmation(false)} dialogClassName="modal-90w" >
        <Modal.Header closeButton>
          <Modal.Title>Delete All</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <p>Are you sure you want to delete all?</p>
          <p>This action cannot be undone.</p>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={() => toggleDeleteConfirmation(false)}>No</Button>
          <Button variant="danger" onClick={deleteAllItineraries}>Yes</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default TravisBot;
