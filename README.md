# frontyardigans
CSE 5914 Project

# Installing Dependencies
Set up a virtual environment, then run ```make install-deps``` to install dependencies

Run ```pip install -r requirements.txt``` to install the dependencies in a virtual environment
Run ```npm install``` in frontui for frontend dependencies

# To train Rasa model

In the rasa directory, run ```python3 -m rasa train```

# To run frontend with Rasa

open 3 terminals:
1) in rasa: ```python3 -m rasa run --enable-api --cors="*"```
2) in rasa: ```python3 -m rasa run actions```
3) in frontui: ```npm start``` 

Open in localhost:3000 if browser doesn't pop up automatically

# Note about API keys

You will have to supply your own API keys
