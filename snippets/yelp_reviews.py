import requests
import json
import sys

# Get command line arguments
# Usage: python yelp_reviews.py Columbus 10
if len(sys.argv) > 2:
    city_name = sys.argv[1]
    try:
        int(sys.argv[2])
        number_to_fetch = sys.argv[2]
    except ValueError:
        number_to_fetch = "5"
else:
        city_name = "Columbus"
        number_to_fetch = "5"

# Reads the API key from a file
def readAPIKey(filename):
    with open(filename, 'r+') as keyFile:
        return keyFile.readline()
API_KEY = readAPIKey("API_KEY.txt").strip()

# Call the Fusion API
url = "https://api.yelp.com/v3/businesses/search?sort_by=best_match&limit=" + number_to_fetch
headers = {"accept": "application/json",
            "Authorization": "Bearer " + API_KEY}
response = requests.get(url, headers=headers, params = {"location": city_name})

# Print all the business names
data = response.json()["businesses"]
for i in range(len(data)):
    print(data[i]["name"])
