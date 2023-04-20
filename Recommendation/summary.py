import requests, re, json

def get_city_info(city_name):
    url = f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={city_name}"

    response = requests.get(url)
    data = response.json()

    page = data['query']['pages']
    page_id = list(page.keys())[0]
    page_content = page[page_id]['extract']
    no_paren = re.sub(r'\(.*?\)', '', page_content)
    no_paren = re.sub(r'[()]', '', no_paren)

    sentences = no_paren.split('.')
    first_three_sentences = '. '.join(sentences[:3]) + "\n\n"

    return first_three_sentences