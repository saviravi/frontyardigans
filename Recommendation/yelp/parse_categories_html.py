from bs4 import BeautifulSoup

html = open('categories.html', 'r')
soup = BeautifulSoup(html, features="lxml")
root_ul = soup.findAll("ul")[0]
li = root_ul.findChildren("li", recursive=False)
ul = root_ul.findChildren("ul", recursive=False)
categories = list(zip(li, ul))

def parse_category(category: str):
    split_cat = category.split(",")
    if ')' in split_cat[0]:
        idx = split_cat[0].index(")")
        s = split_cat[0][idx+1:]
        name = split_cat[0][:idx+1].strip()
        alias = s.split("(")[1].strip()
    else:
        split_cat = category.split("(")
        name = split_cat[0].strip()
        alias = split_cat[1].split(",")[0].strip()

    name = name.replace(" ", "").replace("&", "And").replace("/", "And").replace("-", "").replace("'", "").replace("3", "Three").replace(",", "And").replace("(", "").replace(")", "")

    return name, alias

with open('parsed_categories.py', 'w') as f:
    f.write("from enum import Enum\n")
    f.write("from typing import Union\n\n")


    for li, ul in categories:
        category = li.text.strip()
        cat_name, cat_alias = parse_category(category)
        f.write("class Yelp%sCategory(Enum):\n" % cat_name)
        f.write("\t%s = '%s'\n" % (cat_name, cat_alias))

        subcategories = [li.text.strip() for li in ul.findChildren("li")]
        seen = set()
        for c in subcategories:
            cat_name, cat_alias = parse_category(c)
            if cat_name not in seen:
                seen.add(cat_name)
                f.write("\t%s = '%s'\n" % (cat_name, cat_alias))
            else:
                continue
        f.write("\n\n")
    
    f.write("""
def get_values(enum: Enum):
\treturn [enum(x).value for x in enum]

def parse_alias(alias: str) -> Union[
\tYelpShoppingCategory,
\tYelpNightlifeCategory,
\tYelpHotelsAndTravelCategory,
\tYelpFoodCategory,
\tYelpArtsAndEntertainmentCategory,
\tYelpActiveLifeCategory,
\tYelpRestaurantsCategory
]:
\tif alias in get_values(YelpShoppingCategory):
\t\treturn YelpShoppingCategory(alias)
\telif alias in get_values(YelpRestaurantsCategory):
\t\treturn YelpRestaurantsCategory(alias)
\telif alias in get_values(YelpNightlifeCategory):
\t\treturn YelpNightlifeCategory(alias)
\telif alias in get_values(YelpHotelsAndTravelCategory):
\t\treturn YelpHotelsAndTravelCategory(alias)
\telif alias in get_values(YelpFoodCategory):
\t\treturn YelpFoodCategory(alias)
\telif alias in get_values(YelpArtsAndEntertainmentCategory):
\t\treturn YelpArtsAndEntertainmentCategory(alias)
\telif alias in get_values(YelpActiveLifeCategory):
\t\treturn YelpActiveLifeCategory(alias)
\telse:
\t\treturn None
    """)