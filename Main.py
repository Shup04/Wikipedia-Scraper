import requests
from bs4 import BeautifulSoup
import json

# Fetch content from the URL
URL = "https://en.wikipedia.org/wiki/List_of_freshwater_aquarium_fish_species"
page = requests.get(URL)

# Parse the HTML content
soup = BeautifulSoup(page.content, 'html.parser')

fish_data_list = []
tbodies = soup.find_all('tbody')

# grab the second table
# Table 2 contains Catfish data
tbody = tbodies[1] if len(tbodies) > 1 else None
for row in tbody.find_all('tr'):
    print (row)
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
            "group": "Catfish",
            "subgroup": "Armored Catfish"
            # Add more fields as needed
        })


# grab the third table
# Table 3 contains armored suckermouth Catfish data
tbody = tbodies[2] if len(tbodies) > 1 else None
for row in tbody.find_all('tr'):
    print (row)
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
            "group": "Catfish",
            "subgroup": "Armored SuckerMouth Catfish"
            # Add more fields as needed
        })


# grab 4th table
#contains long wiskered catfish
tbody = tbodies[3] if len(tbodies) > 1 else None
for row in tbody.find_all('tr'):
    print (row)
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
            "group": "Catfish",
            "subgroup": "Long-whiskered Catfish"
            # Add more fields as needed
        })


# grab 5th table
#contains squeakers and upside-down catfish
tbody = tbodies[4] if len(tbodies) > 1 else None
for row in tbody.find_all('tr'):
    print (row)
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
            "group": "Catfish",
            "subgroup": "Squeakers & Upside-down Catfish"
            # Add more fields as needed
        })


# grab 6th table
#contains other catfish
tbody = tbodies[5] if len(tbodies) > 1 else None
for row in tbody.find_all('tr'):
    print (row)
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
            "group": "Catfish",
            "subgroup": "Other Catfish"
            # Add more fields as needed
        })




# Saving the data to a JSON file
with open('fish_data.json', 'w', encoding='utf-8') as f:
    json.dump(fish_data_list, f, ensure_ascii=False, indent=4)
