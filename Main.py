import requests
from bs4 import BeautifulSoup
import json
from openai import OpenAI

# Fetch content from the URL
URL = "https://en.wikipedia.org/wiki/List_of_freshwater_aquarium_fish_species"
response = requests.get(URL)
response.raise_for_status() # cause error if request fails

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

fish_data_list = []
tables = soup.find_all('table', class_='sortable')

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

# Easier identifier for all items
unique_index = 0

# Scrapes whichever table is passed to it
def scrape(table, group, subgroup, start_index):
    global unique_index
    unique_iindex = start_index
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        if len(cells) > 1:  # Ensure there are enough cells
            image_cell = cells[2].find('img')
            image_url = f"https:{image_cell['src']}" if image_cell else ""
            
            fish_data_list.append({
                "id": unique_index,
                "name": cells[0].text.strip(),
                "scientific_name": cells[1].text.strip(),
                "image": image_url,
                "size": cells[3].text.strip(),
                "remarks": cells[4].text.strip(),
                "tank_size": cells[5].text.strip(),
                "temperature": cells[6].text.strip(),
                "pH": cells[7].text.strip(),
                "group": group,
                "subgroup": subgroup
            })
            unique_index += 1

# Checking the lengths of each subgroup to ensure alignment
# print("Characins & Other Characiformes subgroups:", len(groups_with_subgroups["Characins & Other Characiformes"]))
# print("Cichlids subgroups:", len(groups_with_subgroups["Cichlids"]))
# print("Cyprinids subgroups:", len(groups_with_subgroups["Cyprinids"]))
# print("Loaches & Related Cypriniformes subgroups:", len(groups_with_subgroups["Loaches & Related Cypriniformes"]))
# print("Livebearers & Killifish subgroups:", len(groups_with_subgroups["Livebearers & Killifish"]))
# print("Labyrinth Fish subgroups:", len(groups_with_subgroups["Labyrinth Fish"]))
# print("Rainbowfish subgroups:", len(groups_with_subgroups["Rainbowfish"]))
# print("Catfish subgroups:", len(groups_with_subgroups["Catfish"]))

start_index = 1
for group, subgroups in groups_with_subgroups.items():
    for i, subgroup in enumerate(subgroups):
        scrape(tables[i], group, subgroup, start_index+len(fish_data_list))  # Assuming each table directly corresponds; adjust as necessary




with open('fish_data.json', 'w', encoding='utf-8') as f:
    json.dump(fish_data_list, f, ensure_ascii=False, indent=4)
