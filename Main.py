import requests
from bs4 import BeautifulSoup
import json

# Fetch content from the URL
URL = "https://en.wikipedia.org/wiki/List_of_freshwater_aquarium_fish_species"
page = requests.get(URL)

# Parse the HTML content
soup = BeautifulSoup(page.content, 'html.parser')

fish_data_list = []
tables = soup.find_all('table', class_='sortable')
tbodies = [table.find('tbody') for table in tables]

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
    print(f"Scraping {group}: {subgroup}")
    print(tbody)
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
                #"ph": cells[7].text.strip(),
                "group": group,
                "subgroup": subgroup
                # Add more fields as needed
            })

# Checking the lengths of each subgroup to ensure alignment
print("Catfish subgroups:", len(groups_with_subgroups["Catfish"]))
print("Characins & Other Characiformes subgroups:", len(groups_with_subgroups["Characins & Other Characiformes"]))
print("Cichlids subgroups:", len(groups_with_subgroups["Cichlids"]))
print("Cyprinids subgroups:", len(groups_with_subgroups["Cyprinids"]))
print("Loaches & Related Cypriniformes subgroups:", len(groups_with_subgroups["Loaches & Related Cypriniformes"]))
print("Livebearers & Killifish subgroups:", len(groups_with_subgroups["Livebearers & Killifish"]))
print("Labyrinth Fish subgroups:", len(groups_with_subgroups["Labyrinth Fish"]))
print("Rainbowfish subgroups:", len(groups_with_subgroups["Rainbowfish"]))


Scrape(tbodies[0], "Catfish", "Armored Catfish")
Scrape(tbodies[1], "Catfish", "Armoured Suckermouth Catfish")
Scrape(tbodies[2], "Catfish", "Long-whiskered Catfish")
Scrape(tbodies[3], "Catfish", "Squeakers & Upside-down Catfish")
Scrape(tbodies[4], "Catfish", "Other Catfish")
Scrape(tbodies[5], "Characins & Other Characiformes", "Tetras")
Scrape(tbodies[6], "Characins & Other Characiformes", "Hatchetfish")
Scrape(tbodies[7], "Characins & Other Characiformes", "Pencilfish")
Scrape(tbodies[8], "Characins & Other Characiformes", "Serrasalminae")
Scrape(tbodies[9], "Characins & Other Characiformes", "Other Characins")
Scrape(tbodies[10], "Cichlids", "Lake Malawi Cichlids")
Scrape(tbodies[11], "Cichlids", "Lake Tanganyika Cichlids")
Scrape(tbodies[12], "Cichlids", "Lake Victorio Cichlids")
Scrape(tbodies[13], "Cichlids", "Miscellaneous African Cichlids")
Scrape(tbodies[14], "Cichlids", "Dwarf Cichlids")
Scrape(tbodies[15], "Cichlids", "Central American Cichlids")
Scrape(tbodies[16], "Cichlids", "South American")
Scrape(tbodies[17], "Cichlids", "Other Cichlids")
Scrape(tbodies[18], "Cyprinids", "Barbs")
Scrape(tbodies[19], "Cyprinids", "Other Cyprinids")
Scrape(tbodies[20], "Cyprinids", "Rasboras")
Scrape(tbodies[21], "Cyprinids", "Danios & Other Danionins")
Scrape(tbodies[22], "Cyprinids", "Cold-water Cyprinids")
Scrape(tbodies[23], "Loaches & Related Cypriniformes", "Loaches")
Scrape(tbodies[24], "Livebearers & Killifish", "Guppies & Mollies")
Scrape(tbodies[25], "Livebearers & Killifish", "Platies & Swordtails")
Scrape(tbodies[26], "Livebearers & Killifish", "Other Livebearers")
Scrape(tbodies[27], "Livebearers & Killifish", "Killifish")
Scrape(tbodies[28], "Labyrinth Fish", "Gouramis")
Scrape(tbodies[29], "Labyrinth Fish", "Other Labyrinth Fish")
Scrape(tbodies[30], "Rainbowfish", "Rainbowfish")
Scrape(tbodies[31], "Gobies & Sleepers", "Gobies & Sleepers")
Scrape(tbodies[32], "Sunfish & Relatives", "Sunfish & Relatives")
Scrape(tbodies[33], "Others", "Others")




with open('fish_data.json', 'w', encoding='utf-8') as f:
    json.dump(fish_data_list, f, ensure_ascii=False, indent=4)
