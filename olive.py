import json

import httpx
from bs4 import BeautifulSoup


def get_animal_details(url):
    # 1. Fetch the page
    with httpx.Client(follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()

    # 2. Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Shelterluv embeds often store data in a 'window.shelterluvData'
    # or similar JavaScript object. If that's not available,
    # we can scrape the specific labels and values.

    tag = soup.find("iframe-animal")
    animal = tag.get(":animal")
    return json.loads(animal)


# Usage
animal_id = "HBCA-A-83583"
url = f"https://www.shelterluv.com/embed/animal/{animal_id}"
data = get_animal_details(url)

print(json.dumps(data, indent=2))
