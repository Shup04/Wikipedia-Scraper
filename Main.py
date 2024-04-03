import requests
from bs4 import BeautifulSoup
import json
#from openai import OpenAI
from GPTSummarize import generateGPTResponse

# Fetch content from the URL
URL = "https://en.wikipedia.org/wiki/List_of_freshwater_aquarium_fish_species"
response = requests.get(URL)
response.raise_for_status() # cause error if request fails

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

fish_data_list = []
tables = soup.find_all('table', class_='sortable')

global unique_index

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

# For scraping description if there is a secondary page
def scrape_description(second_url):
    second_response = requests.get(second_url)
    page_soup = BeautifulSoup(second_response.content, 'html.parser')
    # Locate the specific div by its class
    specific_div = page_soup.find('div', class_='mw-content-ltr mw-parser-output')


    # If the div is found, grab all text (should be the same for all pages)
    if specific_div:
        all_paragraph_text = " ".join(paragraph.text.strip() for paragraph in specific_div.find_all('p'))
        print(all_paragraph_text)
        return(generateGPTResponse(all_paragraph_text))
    else:
        print("Specific div not found.")

def appendPlaties():
  fish_data_list.append({
              "id": unique_index,
              "name": "Southern platy",
              "scientific_name": "Xiphophorus maculatus",
              "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Xiphophorus_maculatus.jpg/175px-Xiphophorus_maculatus.jpg",
              "size": "6 cm (2.4 in)",
              "remarks": "",
              "tank_size": "",
              "temperature": "",
              "pH": "",
              "group": "Livebearers & Killifish",
              "subgroup": "Platies & Swordtails",
              "link": "https://en.wikipedia.org/wiki/Southern_platyfish",
              "description": ""
          })
  unique_index += 1
  fish_data_list.append({
              "id": unique_index,
              "name": "Southern platy",
              "scientific_name": "Xiphophorus variatus",
              "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Papagaienplaty.jpg/175px-Papagaienplaty.jpg",
              "size": "6 cm (2.4 in)",
              "remarks": "",
              "tank_size": "",
              "temperature": "",
              "pH": "",
              "group": "Livebearers & Killifish",
              "subgroup": "Platies & Swordtails",
              "link": "https://en.wikipedia.org/wiki/Variable_platyfish",
              "description": ""
          })
  unique_index += 1
  fish_data_list.append({
              "id": unique_index,
              "name": "Green swordtail",
              "scientific_name": "Xiphophorus hellerii",
              "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Xiphophorus_helleri_03.jpg/175px-Xiphophorus_helleri_03.jpg",
              "size": "15 cm (5.9 in)",
              "remarks": "",
              "tank_size": "",
              "temperature": "",
              "pH": "",
              "group": "Livebearers & Killifish",
              "subgroup": "Platies & Swordtails",
              "link": "https://en.wikipedia.org/wiki/Green_swordtail",
              "description": ""
          })
  unique_index += 1

# Scrapes whichever table is passed to it
def scrape(table, group, subgroup, start_index):
    
    unique_index = start_index
    
    if subgroup == "Platies & Swordtails":
      appendPlaties()

    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        if len(cells) == 8:  # Ensure there are enough cells

            # Grab image URL if it exists
            image_cell = cells[2].find('img')
            image_url = f"https:{image_cell['src']}" if image_cell else ""

            # Grab the description from the hyperlink
            link_cell = cells[1].find('a', href=True)
            description_url = f"https://en.wikipedia.org{link_cell['href']}" if link_cell else ""

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
                "subgroup": subgroup,
                "link": description_url,
                "description": ""
            })
            unique_index += 1

table_index = 0  # Initialize table_index before the loop

for group, subgroups in groups_with_subgroups.items():
    for subgroup in subgroups:
        # Check if table_index exceeds the number of tables to prevent IndexError
        # print(f"Processing subgroup: {subgroup}")
        scrape(tables[table_index], group, subgroup, len(fish_data_list))
        table_index += 1  # Increment table_index after each scrape call
        # print(f"Finished processing {subgroup}, current fish count: {len(fish_data_list)}")


with open('fish_data_links.json', 'w', encoding='utf-8') as f:
    json.dump(fish_data_list, f, ensure_ascii=False, indent=4)
