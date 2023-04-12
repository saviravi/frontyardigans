import React, { useState } from 'react';
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

const TravisBot = () => {
  const [showBot, toggleBot] = useState(true);

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
    </div>
  );
};

export default TravisBot;
