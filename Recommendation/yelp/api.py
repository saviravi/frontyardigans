from dotenv import load_dotenv
import os
from urllib.parse import urlencode
import requests

# Load environment variables
load_dotenv()
YELP_FUSION_TOKEN = os.getenv('YELP_FUSION_TOKEN')

# Define Yelp API URL routes
YELP_BUSINESS_SEARCH_URL = "https://api.yelp.com/v3/businesses/search"

class YelpAPIException(Exception):
    """
    Raised when a Yelp API request fails
    """
    pass

def _send_yelp_request(url, params):
    """
    Send a request to the Yelp Fusion API.
    """
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + YELP_FUSION_TOKEN
    }
    url_params = "?" + urlencode(params)
    return requests.get(url + url_params, headers=headers)

def get_businesses(location: str, radius=8050, price=2, limit=50) -> dict:
    """
    Searches Yelp Fusion API for businesses by location name, e.g. "NYC".
    Returns JSON of business details or raises YelpAPIException.
    """
    response = _send_yelp_request(YELP_BUSINESS_SEARCH_URL, locals())
    if response.status_code == 200:
        return response.json()
    else:
        raise YelpAPIException(str(response.content))

def get_businesses(latitude: float, longitude: float, radius=8050, price=2, limit=50) -> dict:
    """
    Searches Yelp Fusion API for businesses by latitude and longitude.
    Returns JSON of business details or raises YelpAPIException.
    """
    response = _send_yelp_request(YELP_BUSINESS_SEARCH_URL, locals())
    if response.status_code == 200:
        return response.json()
    else:
        raise YelpAPIException(str(response.content))