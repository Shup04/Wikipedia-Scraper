import requests
from bs4 import BeautifulSoup
import json

# Fetch content from the URL
URL = "https://en.wikipedia.org/wiki/List_of_freshwater_aquarium_fish_species"
page = requests.get(URL)

# Check if the request was successful
if page.status_code == 200:
    html_content = page.text
else:
    print("Failed to retrieve the page")
    html_content = ""

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

fish_list = []

# Assuming each fish is in a table row (`tr`), but you'll need to adjust selectors based on the actual structure
for row in soup.find_all('tr'):
    fish_data = {}

    # Extract fish name, assuming it's in the first `td`
    name_cell = row.find('td')
    if name_cell:
        fish_data['name'] = name_cell.text.strip()

    # Extract image URL, assuming images are direct children of `td` elements
    image = row.find('img')
    if image and 'src' in image.attrs:
        fish_data['image_url'] = f"https:{image['src']}"

    # Only add to the list if we have a name
    if fish_data:
        fish_list.append(fish_data)

# Print the list to see if data extraction is working
for fish in fish_list:
    print(fish)

# Saving the data to a JSON file
with open('fish_data.json', 'w', encoding='utf-8') as f:
    json.dump(fish_list, f, ensure_ascii=False, indent=4)

