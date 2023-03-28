import numpy as np
from yelp import YelpResult, YelpFoodCategory, YelpShoppingCategory, YelpRestaurantsCategory, YelpActiveLifeCategory, YelpNightlifeCategory, YelpArtsAndEntertainmentCategory 

def nar(businesses: list[YelpResult]) -> np.ndarray:
    """
    Takes in a list of businesses and calculates the NAR.
    NAR = (number of businesses of category x) / (total number of businesses)
    Returns the NAR vector for the categories in the order: Shopping, Nightlife, Restaurants, Arts and Entertainment, Active Life.
    """
    counts = dict()
    for business in businesses:
        for category in business.categories:
            if category is None:
                continue

            if type(category) not in counts:
                counts[type(category)] = 0
            
            counts[type(category)] += 1
    
    nar = np.zeros((5,))
    nar[0] = counts[YelpShoppingCategory]
    nar[1] = counts[YelpNightlifeCategory]
    nar[2] = counts[YelpRestaurantsCategory]
    nar[3] = counts[YelpArtsAndEntertainmentCategory]
    nar[4] = counts[YelpActiveLifeCategory]

    return nar / np.sum(nar)

def wnar(businesses: list[YelpResult]) -> np.ndarray:
    """
    Takes in a list of businesses and calculates the WNAR.
    WNAR = (sum of star ratings for businesses of category x) / (number of businesses in category x)
    Returns the WNAR vector for the categories in the order: Shopping, Nightlife, Restaurants, Arts and Entertainment, Active Life.
    """
    ratings = dict()
    counts = dict()
    for business in businesses:
        for category in business.categories:
            if category is None:
                continue

            if type(category) not in counts:
                counts[type(category)] = 0
                ratings[type(category)] = 0
            
            counts[type(category)] += 1
            ratings[type(category)] += business.rating
    
    wnar = np.zeros((5,))
    wnar[0] = ratings[YelpShoppingCategory] / counts[YelpShoppingCategory]
    wnar[1] = ratings[YelpNightlifeCategory] / counts[YelpNightlifeCategory]
    wnar[2] = ratings[YelpRestaurantsCategory] / counts[YelpRestaurantsCategory]
    wnar[3] = ratings[YelpArtsAndEntertainmentCategory] / counts[YelpArtsAndEntertainmentCategory]
    wnar[4] = ratings[YelpActiveLifeCategory] / counts[YelpActiveLifeCategory]

    return wnar