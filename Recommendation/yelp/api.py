from typing import Union
from dotenv import load_dotenv
import os
from urllib.parse import urlencode
import requests
from dataclasses import dataclass, asdict
from .categories import YelpCategory, UnknownYelpCategory
from .parsed_categories import parse_alias

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

@dataclass
class YelpResult():
    id: str
    name: str
    image_url: str
    is_closed: bool
    url: str
    review_count: int
    categories: list[Union[UnknownYelpCategory, YelpCategory]]
    rating: float
    price: int
    latitude: float
    longitude: float
    city_name: str

    def jsonify(self) -> dict:
        return asdict(self)

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

def _json_business_to_result(business: dict) -> YelpResult:
    categories = []

    return YelpResult(
                id=business["id"],
                name=business["name"],
                image_url=business["image_url"],
                is_closed=business["is_closed"],
                url=business["url"],
                categories=list(map(parse_alias, [c["alias"] for c in business["categories"]])),
                review_count=business["review_count"],
                rating=business["rating"],
                price=len(business["price"]),
                latitude=business["coordinates"]["latitude"],
                longitude=business["coordinates"]["longitude"],
                city_name=business["location"]["city"]
            )

def get_businesses_by_location_name(location: str, radius=8050, price: Union[int, str]="1,2,3,4", limit=50, categories="") -> list[YelpResult]:
    """
    Searches Yelp Fusion API for businesses by location name, e.g. "NYC".
    Returns JSON of business details or raises YelpAPIException.
    """
    response = _send_yelp_request(YELP_BUSINESS_SEARCH_URL, locals())
    if response.status_code == 200:
        api_results = response.json()
        return list(map(_json_business_to_result, api_results["businesses"]))
    else:
        raise YelpAPIException(str(response.content))

def get_businesses_by_lat_long(latitude: float, longitude: float, radius=8050, price: Union[int, str]="1,2,3,4", limit=50, categories="") -> list[YelpResult]:
    """
    Searches Yelp Fusion API for businesses by latitude and longitude.
    Returns JSON of business details or raises YelpAPIException.
    """
    response = _send_yelp_request(YELP_BUSINESS_SEARCH_URL, locals())
    if response.status_code == 200:
        api_results = response.json()
        return list(map(_json_business_to_result, api_results["businesses"]))
    else:
        raise YelpAPIException(str(response.content))