# Team Frontyardigans - Travis Recommendation Bot

[![Netlify Status](https://api.netlify.com/api/v1/badges/d501e335-73f3-4642-aeb3-a744a23ec626/deploy-status)](https://app.netlify.com/sites/frontyardigans-travis/deploys)  
CSE 5914 Project  
Please follow the instructions below to run the project.

## Installing Dependencies

1. Set up a virtual environment, then run ```make install-deps``` to install dependencies
2. Run ```pip install -r requirements.txt``` to install the dependencies in your virtual environment  
3. Run ```npm install``` in ```frontui``` directory for frontend dependencies

## To train Rasa model

1. In the ```rasa``` directory, run ```python3 -m rasa train```

## Start Using Travis Bot

If you wish to use the Netlify service, please follow the steps below. If not, please skip to the next section.  

You need to open 2 separate terminal windows.  

1. Open a terminal window, enter the ```rasa``` directory and run: ```python3 -m rasa run --enable-api --cors="*"```
2. Open another terminal window, enter the ```rasa``` directory and run: ```python3 -m rasa run actions```
3. Visit ```https://frontyardigans-travis.netlify.app/``` and start chatting with Travis!

## Start Using Travis Bot Locally

Alternatively, you can start chatting without using the Netlify service. In this case, the whole project will be running entirely locally in your machine.  

You need to open 3 separate terminal windows.  

1. Open a terminal window, enter the ```rasa``` directory and run: ```python3 -m rasa run --enable-api --cors="*"```
2. Open a second terminal window, enter the ```rasa``` directory and run: ```python3 -m rasa run actions```
3. Open a third terminal window, enter the ```frontui``` directory and run: ```npm start```

In your browser, visit ```localhost:3000``` if the webpage did not pop up automatically.

## Note about API Keys

You will have to supply your own API keys for Yelp Fusion, Bonsai, and Duffel.  
Store them as environment variables: ```DUFFEL_TOK, BONSAI_URL, YELP_FUSION_TOKEN```.  
In the root directory of the project, create a file called ```.env``` and store your API keys in the following format:  
```DUFFEL_TOK=[your_duffel_token]```  
```BONSAI_URL=[your_bonsai_url]```  
```YELP_FUSION_TOKEN=[your_yelp_fusion_token]```
