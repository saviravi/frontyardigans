import React from "react";
import { useNavigate } from 'react-router-dom';
//import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';

const Welcome = () => {
    let navigate = useNavigate();

    return(
        <div className="welcome-page-container">
            <div className="welcome-page-banner-container">
                <h1>Travel planning shouldn't be a hassle.</h1>
                <h2>That's why Travis is here to help.</h2>
                <h3>Let Travis help you plan your next trip!</h3>
                <div className="welcome-page-button">
                    <Button variant="primary" onClick={() => {navigate("/bot");}}>Talk with Travis</Button>{' '}
                </div>
            </div>
        </div>
    );
}

export default Welcome;
