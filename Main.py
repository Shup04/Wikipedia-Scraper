import requests
from bs4 import BeautifulSoup
import json

# Fetch content from the URL
URL = "https://en.wikipedia.org/wiki/List_of_freshwater_aquarium_fish_species"
page = requests.get(URL)

# Parse the HTML content
soup = BeautifulSoup(page.content, 'html.parser')

fish_data_list = []
tempbodies = soup.find_all('tbody')

tbodies = tempbodies[1::2]


groups_with_subgroups = {
    "Catfish": ["Armored Catfish", "Armoured Suckermouth Catfish", "Long-whiskered Catfish", "Squeakers & Upside-down Catfish", "Other Catfish"],
    "Characins & Other Characiformes": ["Tetras", "Hatchetfish", "Pencilfish", "Serrasalminae", "Other Characins"],
    "Cichlids": ["Lake Malawi Cichlids", "Lake Tanganyika Cichlids", "Lake Victorio Cichlids", "Miscellaneous African Cichlids", "Dwarf Cichlids", "Central American Cichlids", "South American", "Other Cichlids"],
    "Cyprinids": ["Barbs", "Other Cyprinids", "Rasboras", "Danios & Other Danionins", "Cold-water Cyprinids"],
    "Loaches & Related Cypriniformes": ["Loaches"],
    "Livebearers & Killifish": ["Guppies & Mollies", "Platies & Swordtails", "Other Livebearers", "Killifish"],
    "Labyrinth Fish": ["Gouramis", "Other Labyrinth Fish"],
    "Rainbowfish": ["Rainbowfish"],
    "Gobies & Sleepers": ["Gobies & Sleepers"],
    "Sunfish & Relatives": ["Sunfish & Relatives"],
    "Others": ["Others"]
}

# Scrapes whichever table is passed to it
def Scrape(tbody, group, subgroup):
    for row in tbody.find_all('tr'):
        cells = row.find_all('td')  # Use 'td' for data cells, assuming 'th' is used for header cells which are not needed here
        if len(cells) > 1:  # Check to ensure there are enough cells for data extraction
            # Check and extract image URL correctly
            image_cell = cells[2].find('img')
            image_url = f"https:{image_cell['src']}" if image_cell and 'src' in image_cell.attrs else ""

            # Append a new dictionary for each fish directly into fish_data_list
            fish_data_list.append({
                "name": cells[0].text.strip(),
                "scientific_name": cells[1].text.strip(),
                "image": image_url,
                "size": cells[3].text.strip(),
                "remarks": cells[4].text.strip(),
                "min_tank_size": cells[5].text.strip(),
                "temperature": cells[6].text.strip(),
                "ph": cells[7].text.strip(),
                "group": group,
                "subgroup": subgroup
                # Add more fields as needed
            })
#34
for i in range(5):
    Scrape(tbodies[i], "Catfish", groups_with_subgroups["Catfish"][i])

with open('fish_data.json', 'w', encoding='utf-8') as f:
    json.dump(fish_data_list, f, ensure_ascii=False, indent=4)
