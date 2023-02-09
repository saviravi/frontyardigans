import unittest
from .api import get_businesses_by_location_name, get_businesses_by_lat_long, YelpAPIException

class TestYelpAPI(unittest.TestCase):
    """
    Tests getting businesses in NYC by city name.
    """
    def test_get_businesses_city_name_NYC(self):
        response = get_businesses_by_location_name("NYC")
        has_katz = False
        for business in response["businesses"]:
            if "Katz" in business["name"]:
                has_katz = True
        
        self.assertTrue(has_katz)
    
    def test_get_businesses_lat_long_NYC(self):
        """
        Tests getting businesses in NYC by latitude and longitude.
        """
        nyc_latitude = 40.7128
        nyc_longitude = -74.0060
        response = get_businesses_by_lat_long(nyc_latitude, nyc_longitude)
        has_katz = False
        for business in response["businesses"]:
            if "Katz" in business["name"]:
                has_katz = True
        
        self.assertTrue(has_katz)

    def test_get_businesses_city_name_empty(self):
        """
        Tests that an empty name raises a YelpAPIException
        """
        with self.assertRaises(YelpAPIException):
            _ = get_businesses_by_location_name("")
