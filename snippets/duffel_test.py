import os
from duffel_api import Duffel


client = Duffel(access_token=os.environ.get("DUFFEL_TOK"))

offer_requests = client.offer_requests.list()
for offer_request in offer_requests:
    print(offer_request.id)
    print(offer_request.passengers)

