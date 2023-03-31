import React from "react";
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./about.css";
// import defaultAvatarMale from "../images/person-male.png";
// import defaultAvatarFemale from "../images/person-female.png";

const About = () => {
    return(
        <div className="about-page">
            <div className="about-title">
                <h1>About Us</h1>
            </div>
            <div className="contributor-container">
                <Card style={{ width: '18rem' }}>
                    <Card.Img className="contributor-image" variant="top" src="https://static.licdn.com/sc/h/244xhbkr7g40x6bsu4gi6q4ry" />
                    <Card.Body>
                        <Card.Title>Stanley Vernier</Card.Title>
                        <Card.Text>
                            Instructor of the course<br/>
                            <a href="mailto: vernier.13@osu.edu">vernier.13@osu.edu</a>
                        </Card.Text>
                        <Button variant="primary" href="https://www.linkedin.com/in/stanvernier" target="_blank" rel="noopener noreferrer">LinkedIn</Button>
                    </Card.Body>
                </Card>
                <Card style={{ width: '18rem' }}>
                    <Card.Img className="contributor-image" variant="top" src="https://avatars.githubusercontent.com/u/60449560?v=4" />
                    <Card.Body>
                        <Card.Title>Chris Cosma</Card.Title>
                        <Card.Text>
                            Description of Chris Cosma<br/>
                            <a href="mailto: cosma.5@osu.edu">cosma.5@osu.edu</a>
                        </Card.Text>
                        <Button variant="primary" href="https://github.com/chriscosma" target="_blank" rel="noopener noreferrer">GitHub</Button>
                    </Card.Body>
                </Card>
                <Card style={{ width: '18rem' }}>
                    <Card.Img className="contributor-image" variant="top" src="https://avatars.githubusercontent.com/u/55661271?v=4" />
                    <Card.Body>
                        <Card.Title>Shivani Jayasaal</Card.Title>
                        <Card.Text>
                            Description of Shivani Jayasaal<br/>
                            <a href="mailto: jayasaal.2@osu.edu">jayasaal.2@osu.edu</a>
                        </Card.Text>
                        <Button variant="primary" href="https://github.com/jayasaal2" target="_blank" rel="noopener noreferrer">GitHub</Button>
                    </Card.Body>
                </Card>
                <Card style={{ width: '18rem' }}>
                    <Card.Img className="contributor-image" variant="top" src="https://avatars.githubusercontent.com/u/90643595?v=4" />
                    <Card.Body>
                        <Card.Title>Kevin Le</Card.Title>
                        <Card.Text>
                            Description of Kevin Le<br/>
                            <a href="mailto: le.542@osu.edu">le.542@osu.edu</a>
                        </Card.Text>
                        <Button variant="primary" href="https://github.com/le542" target="_blank" rel="noopener noreferrer">GitHub</Button>
                    </Card.Body>
                </Card>
                <Card style={{ width: '18rem' }}>
                    <Card.Img className="contributor-image" variant="top" src="https://avatars.githubusercontent.com/u/25752015?v=4" />
                    <Card.Body>
                        <Card.Title>Jason Moore</Card.Title>
                        <Card.Text>
                            Description of Jason Moore<br/>
                            <a href="mailto: moore.4000@osu.edu">moore.4000@osu.edu</a>
                        </Card.Text>
                        <Button variant="primary" href="https://github.com/Jason-DM" target="_blank" rel="noopener noreferrer">GitHub</Button>
                    </Card.Body>
                </Card>
                <Card style={{ width: '18rem' }}>
                    <Card.Img className="contributor-image" variant="top" src="https://avatars.githubusercontent.com/u/45365011?v=4" />
                    <Card.Body>
                        <Card.Title>Savitha Ravi</Card.Title>
                        <Card.Text>
                            Description of Savitha Ravi<br/>
                            <a href="mailto: ravi.98@osu.edu">ravi.98@osu.edu</a>
                        </Card.Text>
                        <Button variant="primary" href="https://github.com/saviravi" target="_blank" rel="noopener noreferrer">GitHub</Button>
                    </Card.Body>
                </Card>
                <Card style={{ width: '18rem' }}>
                    <Card.Img className="contributor-image" variant="top" src="https://avatars.githubusercontent.com/u/34878168?v=4" />
                    <Card.Body>
                        <Card.Title>Jacob Urick</Card.Title>
                        <Card.Text>
                            Description of Jacob Urick<br/>
                            <a href="mailto: urick.9@osu.edu">urick.9@osu.edu</a>
                        </Card.Text>
                        <Button variant="primary" href="https://github.com/jacurick19" target="_blank" rel="noopener noreferrer">GitHub</Button>
                    </Card.Body>
                </Card>
                <Card style={{ width: '18rem' }}>
                    <Card.Img className="contributor-image" variant="top" src="https://avatars.githubusercontent.com/u/112275918?v=4" />
                    <Card.Body>
                        <Card.Title>Keyang Zhang</Card.Title>
                        <Card.Text>
                            Description of Keyang Zhang<br/>
                            <a href="mailto: zhang.10448@osu.edu">zhang.10448@osu.edu</a>
                        </Card.Text>
                        <Button variant="primary" href="https://github.com/Mutsuki0110" target="_blank" rel="noopener noreferrer">GitHub</Button>
                    </Card.Body>
                </Card>
            </div>
        </div>
    );
}

export default About;
