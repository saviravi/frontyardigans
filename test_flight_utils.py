# import sys
# # import path

# # directory reach
# # directory = path.path(__file__).abspath()
 
# # setting path
# sys.path.append("../")



# # sys.path.append('..')

import flight_utils

def test_get_flights():
    slices = [
    {
        "origin": "JFK",
        "destination": "CMH",
        "departure_date": "2023-06-21"
    }
    ]
    flights = flight_utils.get_flights(slices, [flight_utils.Passenger.ADULT], flight_utils.Cabin.ECONOMY)
    flight_utils.pretty_print_flight_offers(flights)
    return

if __name__ == "__main__":
    test_get_flights()