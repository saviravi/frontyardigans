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
    The WNAR is representitive of the quality of businesses in a certain city per category.
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

if __name__ == "__main__":
    from glob import glob
    from pickle import load
    import matplotlib.pyplot as plt

    paths = glob("yelp/business_data/*.pickle")
    nars = []
    wnars = []
    avg_nar = np.zeros((5,))
    avg_wnar = np.zeros((5,))

    for p in paths:
        with open(p, 'rb') as f:
            businesses = load(f)

            city_nar = nar(businesses)
            city_wnar = wnar(businesses)
            nars.append(city_nar)
            wnars.append(city_wnar)
            avg_nar += city_nar
            avg_wnar += city_wnar
    
    avg_nar /= len(paths)
    avg_wnar /= len(paths)

    print("Avg NAR:", avg_nar)
    print("Avg WNAR:", avg_wnar)

    nar_0 = [n[0] for n in nars]
    nar_1 = [n[1] for n in nars]
    nar_2 = [n[2] for n in nars]
    nar_3 = [n[3] for n in nars]
    nar_4 = [n[4] for n in nars]
    fig, axs = plt.subplots(1, 5)
    bins = np.linspace(0, 1, 100)
    axs[0].hist(nar_0, bins)
    axs[0].set_title("Shopping")
    axs[1].hist(nar_1, bins)
    axs[1].set_title("Nightlife")
    axs[2].hist(nar_2, bins)
    axs[2].set_title("Restaurants")
    axs[3].hist(nar_3, bins)
    axs[3].set_title("Arts and Entertainment")
    axs[4].hist(nar_4, bins)
    axs[4].set_title("Active Life")
    plt.show()

    wnar_0 = [n[0] for n in wnars]
    wnar_1 = [n[1] for n in wnars]
    wnar_2 = [n[2] for n in wnars]
    wnar_3 = [n[3] for n in wnars]
    wnar_4 = [n[4] for n in wnars]
    fig, axs = plt.subplots(1, 5)
    bins = np.linspace(0, 4, 100)
    axs[0].hist(wnar_0, bins)
    axs[0].set_title("Shopping")
    axs[1].hist(wnar_1, bins)
    axs[1].set_title("Nightlife")
    axs[2].hist(wnar_2, bins)
    axs[2].set_title("Restaurants")
    axs[3].hist(wnar_3, bins)
    axs[3].set_title("Arts and Entertainment")
    axs[4].hist(wnar_4, bins)
    axs[4].set_title("Active Life")
    plt.show()